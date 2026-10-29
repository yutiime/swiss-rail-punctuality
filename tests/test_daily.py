from datetime import date

from swiss_rail_punctuality import daily as dl


def test_daily_checks_the_seven_days_before_today(monkeypatch): 
    asked = [] 

    def fake_exists(day): 
        asked.append(day) 
        return True 

    monkeypatch.setattr(dl.storage, "exists", fake_exists) 
    dl.daily(date(2026, 10, 29)) 
    assert asked == [ 
        "2026-10-22", "2026-10-23", "2026-10-24", "2026-10-25",
        "2026-10-26", "2026-10-27", "2026-10-28",
    ] 

def test_daily_only_processes_days_missing_from_storage(monkeypatch): 
    monkeypatch.setattr(dl.storage, "exists", lambda day: day != "2026-10-27")

    def fake_download(day): 
        raise ValueError("no file") 

    monkeypatch.setattr(dl, "download_day", fake_download) 
    failed = dl.daily(date(2026, 10, 29)) 
    assert [d for d, _ in failed] == ["2026-10-27"] 
