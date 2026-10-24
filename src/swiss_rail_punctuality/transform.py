import sys
from datetime import date
from pathlib import Path

import duckdb

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

# shortcut: fixed floors from Sep–Oct 2026 (~80% of the lowest day seen);
# weekday public holidays will trip the weekday floor. Compare with recent
# same-type days once the history lives in cloud storage.
MIN_ROWS = {"weekday": 2_000_000, "saturday": 1_700_000, "sunday": 1_300_000}


def day_type(day: str) -> str:
    weekday = date.fromisoformat(day).weekday() 
    if weekday == 5: 
        return "saturday"
    if weekday == 6: 
        return "sunday" 
    return "weekday" 


def check_row_count(path: Path, day: str) -> None:
    n = duckdb.sql(f"SELECT count(*) FROM read_parquet('{path}')").fetchone()[0]
    floor = MIN_ROWS[day_type(day)] 
    if n < floor: 
        raise ValueError(f"{day}: {n:,} rows, expected at least {floor:,}") 
    


def to_parquet(day: str) -> Path:
    src = RAW_DIR / f"{day}.csv"
    dest = PROCESSED_DIR / f"{day}.parquet"

    if dest.exists():
        return dest

    if not src.exists():
        raise FileNotFoundError(
            f"CSV missing : {src}. Launch download.py {day}"
        )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    tmp = dest.with_suffix(".parquet.part")

    duckdb.sql(f"""
        COPY (SELECT * FROM read_csv('{src}', quote='"', sample_size=-1))
        TO '{tmp}' (FORMAT PARQUET)
    """)
    try: 
        check_row_count(tmp, day) 
    except ValueError: 
        tmp.unlink() 
        raise

    tmp.rename(dest)

    return dest


if __name__ == "__main__":
    print(to_parquet(sys.argv[1]))

