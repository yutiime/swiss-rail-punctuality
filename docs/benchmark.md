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
