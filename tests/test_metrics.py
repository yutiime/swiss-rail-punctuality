from pathlib import Path

import duckdb

from swiss_rail_punctuality.metrics import punctuality

FIXTURE = "tests/fixtures/sample.parquet"


def test_produces_a_file(tmp_path: Path):
    out = punctuality(source=FIXTURE, output=tmp_path / "r.csv")
    assert out.exists()
    assert out.stat().st_size > 0    


def test_columns_are_consistent(tmp_path: Path):
    out = punctuality(source=FIXTURE, output=tmp_path / "r.csv")
    rows = duckdb.sql(f"SELECT * FROM '{out}'").fetchall()
    # For each row: on_time <= total, and 0 <= percentage <= 100.
    for day, total, on_time, percentage in rows:
        assert on_time <= total
        assert 0 <= percentage <= 100
     


def test_larger_threshold_counts_more_on_time_arrivals(tmp_path: Path):
    # Call punctuality twice, with threshold_seconds=0 and threshold_seconds=3600.
    # The second run should count at least as many on-time arrivals.
    strict = punctuality(source=FIXTURE, output=tmp_path / "strict.csv", threshold_seconds=0)
    large = punctuality(source=FIXTURE, output=tmp_path / "large.csv", threshold_seconds=3600)
    strict_count = duckdb.sql(f"SELECT sum(on_time) FROM '{strict}'").fetchone()[0]
    large_count = duckdb.sql(f"SELECT sum(on_time) FROM '{large}'").fetchone()[0]
    assert large_count >= strict_count
 
      