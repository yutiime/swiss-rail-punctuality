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