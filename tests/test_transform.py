from pathlib import Path

import pytest

from swiss_rail_punctuality import transform as tf

FIXTURE = Path("tests/fixtures/sample.parquet") 


def test_day_type(): 
    assert tf.day_type("2026-10-17") == "saturday" 
    assert tf.day_type("2026-10-18") == "sunday"
    assert tf.day_type("2026-10-19") == "weekday" 


def test_check_row_count_rejects_a_small_day(): 
    with pytest.raises(ValueError): 
        tf.check_row_count(FIXTURE, "2026-09-21") 


def test_check_row_count_accepts_a_normal_day(monkeypatch): 
    monkeypatch.setitem(tf.MIN_ROWS, "weekday", 1000) 
    tf.check_row_count(FIXTURE, "2026-09-21") 


def test_to_parquet_discards_a_day_that_fails_the_check(monkeypatch, tmp_path): 
    monkeypatch.setattr(tf, "RAW_DIR", tmp_path) 
    monkeypatch.setattr(tf, "PROCESSED_DIR", tmp_path) 
    (tmp_path / "2026-09-21.csv").write_text("a\n1\n2\n") 

    with pytest.raises(ValueError): 
        tf.to_parquet("2026-09-21") 

    assert not (tmp_path / "2026-09-21.parquet").exists() 
    assert not (tmp_path / "2026-09-21.parquet.part").exists()  

     
