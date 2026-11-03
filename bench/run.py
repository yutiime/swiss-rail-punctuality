import statistics
import tempfile
import time
from pathlib import Path

import duckdb
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from swiss_rail_punctuality.metrics import punctuality

SOURCE = "data/processed/*.parquet"
THRESHOLD_SECONDS = 180
RUNS = 3


def duckdb_rows():
    out = punctuality(source=SOURCE, output=Path(tempfile.gettempdir()) / "bench_duckdb.csv")
    return duckdb.sql(f"SELECT BETRIEBSTAG, total, on_time FROM '{out}' ORDER BY 1").fetchall()


def spark_rows(spark):
    rows = (
        spark.read.parquet(SOURCE)
        .where(
            (F.upper("PRODUKT_ID") == "ZUG")
            & (F.col("AN_PROGNOSE_STATUS") == "REAL")
            & F.col("ANKUNFTSZEIT").isNotNull()
            & ~F.col("FAELLT_AUS_TF")
        )
        .select(
            "BETRIEBSTAG",
            (
                F.unix_timestamp("AN_PROGNOSE")
                - F.unix_timestamp("ANKUNFTSZEIT", "dd.MM.yyyy HH:mm")
            ).alias("delay_seconds"),
        )
        .groupBy("BETRIEBSTAG")
        .agg(
            F.count("*").alias("total"),
            F.sum((F.col("delay_seconds") <= THRESHOLD_SECONDS).cast("int")).alias("on_time"),
        )
        .orderBy("BETRIEBSTAG")
        .collect()
    )
    return [(r.BETRIEBSTAG, r.total, r.on_time) for r in rows]


def timed(fn):
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        result = fn()
        times.append(time.perf_counter() - start)
    return statistics.median(times), result


start = time.perf_counter()
spark = (
    SparkSession.builder.master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
spark_startup = time.perf_counter() - start

duckdb_s, expected = timed(duckdb_rows)
spark_s, got = timed(lambda: spark_rows(spark))
assert got == expected, "Spark and DuckDB disagree"

files = list(Path("data/processed").glob("*.parquet"))
size_gb = sum(f.stat().st_size for f in files) / 1e9
print(f"\n{len(files)} days, {size_gb:.1f} GB of Parquet, same result on both engines\n")
print(f"| Engine | Query (median of {RUNS}) | Startup |")
print("|---|---|---|")
print(f"| DuckDB | {duckdb_s:.2f} s | none |")
print(f"| Spark (local) | {spark_s:.2f} s | {spark_startup:.1f} s |")