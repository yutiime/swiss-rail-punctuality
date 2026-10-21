import sys
from datetime import date, timedelta

from swiss_rail_punctuality.download import download_day
from swiss_rail_punctuality.transform import PROCESSED_DIR, to_parquet


def backfill(start: str, end: str) -> list[tuple[str, Exception]]:
    day = date.fromisoformat(start)
    last = date.fromisoformat(end)
    ok, failed = 0, []

    while day <= last:
        d = day.isoformat()
        print(d, flush=True)

        try:
            if not (PROCESSED_DIR / f"{d}.parquet").exists():
                csv_path = download_day(d)
                to_parquet(d)
                csv_path.unlink()
            ok += 1
        except Exception as e: # noqa: BLE001 - continue the backfill even if one day fails
            failed.append((d, e))

        day += timedelta(days=1)

    print(f"\n{ok} day(s) processed")
    if failed:
        print(f"{len(failed)} failure(s):")
        for d, e in failed:
            print(f"  {d}: {e}") 
    return failed 


if __name__ == "__main__":
    failed = backfill(sys.argv[1], sys.argv[2])
    if failed:
        sys.exit(1)
