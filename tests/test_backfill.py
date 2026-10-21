from swiss_rail_punctuality import backfill as bf


def test_backfill_reports_every_failed_day(monkeypatch, tmp_path): 
    monkeypatch.setattr(bf, "PROCESSED_DIR", tmp_path)  
    
    def fake_download(day): 
        raise ValueError("no file") 

    monkeypatch.setattr(bf, "download_day", fake_download) 
    failed = bf.backfill("2026-01-01", "2026-01-03") 
    assert len(failed) == 3 

def test_backfill_skips_days_already_converted(monkeypatch, tmp_path):
    (tmp_path / "2026-01-01.parquet").touch()
    monkeypatch.setattr(bf, "PROCESSED_DIR", tmp_path)

    calls = []

    def fake_download(day):
        calls.append(day)
        raise ValueError("no file")

    monkeypatch.setattr(bf, "download_day", fake_download)
    bf.backfill("2026-01-01", "2026-01-02")
    assert calls == ["2026-01-02"] 
    