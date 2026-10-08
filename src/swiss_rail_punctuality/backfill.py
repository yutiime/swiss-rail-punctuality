import sys
from datetime import date, timedelta

from download import download_day
from transform import to_parquet


def backfill(start: str, end: str) -> None:
    day = date.fromisoformat(start)
    last = date.fromisoformat(end)
    ok, failed = 0, []

    while day <= last:
        d = day.isoformat()
        print(d, flush=True)

        try:
            csv_path = download_day(d)
            to_parquet(d)
            csv_path.unlink()
            ok += 1
        except Exception as e: # noqa: BLE001 - un backfill continue malgré l'échec d'un jour 
            failed.append((d, e))

        day += timedelta(days=1)

    print(f"\n{ok} jour(s) traité(s)")
    if failed:
        print(f"{len(failed)} échec(s) :")
        for d, e in failed:
            print(f"  {d} : {e}")


if __name__ == "__main__":
    backfill(sys.argv[1], sys.argv[2])
