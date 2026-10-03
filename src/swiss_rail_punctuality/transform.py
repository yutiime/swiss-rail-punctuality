import sys
from pathlib import Path

import duckdb

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def to_parquet(day: str) -> Path:
    src = RAW_DIR / f"{day}.csv"
    dest = PROCESSED_DIR / f"{day}.parquet"

    if dest.exists():
        return dest

    if not src.exists():
        raise FileNotFoundError(
            f"CSV manquant : {src}. Lance d'abord download.py {day}"
        )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    tmp = dest.with_suffix(".parquet.part")

    duckdb.sql(f"""
        COPY (SELECT * FROM read_csv('{src}', quote='"', sample_size=-1))
        TO '{tmp}' (FORMAT PARQUET)
    """)

    tmp.rename(dest)

    return dest


if __name__ == "__main__":
    print(to_parquet(sys.argv[1]))
