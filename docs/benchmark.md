# Benchmarks


## CSV to Parquet conversion
| Format | Size | Rows |
| --- | --- | --- |
| CSV | 608 MB | 2,516,573 |
| Parquet | 43 MB | 2,516,573 |

Compression ratio: 14x. Estimated annual storage: 220 GB as CSV, 16 GB as Parquet.


# Benchmarks


## CSV to Parquet conversion
| Format | Size |
| --- | --- |
| CSV | 608 MB |
| Parquet | 43 MB |

14x compression. One month: 18 GB as CSV, 1.2 GB as Parquet.


## DuckDB aggregation
Daily count across 29 Parquet files (~71 million rows): **0.1 s**


## DuckDB vs Spark, single machine (2026-11-03)

Same punctuality query on both engines, results checked to be identical day by day.

- Data: 56 days (1 Sep – 26 Oct 2026), 2.4 GB of Parquet, 135630278 rows
- Machine: MacBook Air M2, 8 GB RAM
- Versions: DuckDB 1.5.5, PySpark 4.3.0 in local mode (all cores), Java 21
- Method: median of 3 runs, warm file cache, default settings for both engines

| Engine | Query | Startup | Total |
|---|---|---|---|
| DuckDB | 0.55 s | none | 0.55 s |
| Spark (local) | 3.40 s | 3.5 s | 6.9 s |

On one machine, DuckDB is about 6× faster on the query and 12× faster end to
end. Spark pays for scheduling and coordinating tasks as if it had a cluster,
without one to spread the work over. A first, single Spark run took 8.0 s:
the JVM warms up over the first run, which is why the median of several runs
is used.


## Spark on Databricks (2026-11-16)

Same query in a Databricks notebook, reading the 56 Parquet files directly
from ADLS Gen2 (Switzerland North) through a Unity Catalog external location.
Control totals identical to DuckDB: 56 days, 7,740,622 arrivals,
7,243,066 on time.

- Cluster: single node, Standard_D4ads_v7 (4 cores, 16 GB), Databricks
  Runtime 18 LTS (Spark 4.1), Photon off
- Method: 3 runs in the same session

| Run | Time |
|---|---|
| 1st | 30.7 s |
| 2nd | 6.47 s |
| 3rd | 5.38 s |

The first run reads from ADLS over the network; the next ones most likely
read Databricks' local disk cache. A scheduled daily job would pay the
first-run cost. Starting the cluster took about 5 minutes on top.

## Summary

| Engine | Where | Warm query | Fixed overhead |
|---|---|---|---|
| DuckDB | MacBook Air M2, local disk | **0.55 s** | none |
| Spark local | MacBook Air M2, local disk | 3.40 s | 3.5 s JVM start |
| Spark on Databricks | Azure, 4 cores, ADLS | 6.47 s | ~5 min cluster start, 30.7 s first run |

## Cost

The runs themselves cost about €0.35 (VM and DBUs). The workspace cost far
more while idle: its managed NAT gateway and public IP are billed by the hour
whether a cluster runs or not, about €1 a day (€11.84 over 11 days). The
workspace was deleted after the benchmark.

## Conclusion

At 2.4 GB, a single machine running DuckDB answers in half a second with no
infrastructure and no cost. Spark becomes worth its overhead only once the
data no longer fits on one machine, which this project is far from. 