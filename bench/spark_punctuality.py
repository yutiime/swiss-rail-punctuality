import tempfile
import time
from pathlib import Path

import duckdb
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from swiss_rail_punctuality.metrics import punctuality

SOURCE = "data/processed/*.parquet"
THRESHOLD_SECONDS = 180

spark = (
    SparkSession.builder.master("local[*]")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

start = time.perf_counter() 

arrivals = (
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
)

rows = (
    arrivals.groupBy("BETRIEBSTAG")
    .agg(
        F.count("*").alias("total"),
        F.sum((F.col("delay_seconds") <= THRESHOLD_SECONDS).cast("int")).alias("on_time"),
    )
    .orderBy("BETRIEBSTAG")
    .collect()
)

print(f"Spark: {len(rows)} days in {time.perf_counter() - start:.1f} s")

reference = punctuality(output=Path(tempfile.gettempdir()) / "bench_duckdb.csv")
expected = duckdb.sql(
    f"SELECT BETRIEBSTAG, total, on_time FROM '{reference}' ORDER BY 1"
).fetchall()
got = [(r.BETRIEBSTAG, r.total, r.on_time) for r in rows]
assert got == expected, "Spark and DuckDB disagree"
print("Same result as DuckDB")