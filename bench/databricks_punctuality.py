# Databricks notebook source
import statistics
import time
from datetime import date, timedelta

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.getOrCreate()

spark.conf.set("spark.sql.session.timeZone", "UTC")

BASE = "abfss://processed@swissrailyunus.dfs.core.windows.net"
days = [date(2026, 9, 1) + timedelta(n) for n in range(56)]
paths = [f"{BASE}/{d.isoformat()}.parquet" for d in days]


def spark_rows():
    return (
        spark.read.parquet(*paths)
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
            F.sum((F.col("delay_seconds") <= 180).cast("int")).alias("on_time"),
        )
        .orderBy("BETRIEBSTAG")
        .collect()
    )


times = []
for _ in range(3):
    start = time.perf_counter()
    rows = spark_rows()
    times.append(time.perf_counter() - start)

print(len(rows), sum(r.total for r in rows), sum(r.on_time for r in rows))
print(f"median {statistics.median(times):.2f} s, runs {[round(t, 2) for t in times]}")