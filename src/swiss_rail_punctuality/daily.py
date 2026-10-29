import sys
from datetime import UTC, date, datetime, timedelta

from swiss_rail_punctuality import storage
from swiss_rail_punctuality.download import download_day
from swiss_rail_punctuality.transform import to_parquet

DAYS_BACK = 7 # a missed or failed run is caught up by the next ones 



def daily(today:date) -> list[tuple[str, Exception]]: 
    failed = [] 
    for n in range(DAYS_BACK, 0, -1): 
        d = (today - timedelta(days=n)).isoformat() 
        if storage.exists(d): 
            continue 
        try: 
            csv_path = download_day(d) 
            storage.upload(to_parquet(d)) 
            csv_path.unlink() 
            print(f"{d}: uploaded", flush=True) 
        except Exception as e: # noqa: BLE001 - one bad day must block the others
            failed.append((d, e)) 
            print(f"{d}: FAILED {e}", flush=True) 
    return failed 


if __name__== "__main__": 
    if daily(datetime.now(UTC).date()):  
        sys.exit(1) 