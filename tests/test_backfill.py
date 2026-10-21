from swiss_rail_punctuality import backfill as bf


def test_backfill_reports_every_failed_day(monkeypatch): 
    def fake_download(day): 
        raise ValueError("no file") 

    monkeypatch.setattr(bf, "download_day", fake_download) 
    failed = bf.backfill("2026-01-01", "2026-01-03") 
    assert len(failed) == 3 
