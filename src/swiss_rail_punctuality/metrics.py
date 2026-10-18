from pathlib import Path

import duckdb

PROCESSED = "data/processed/*.parquet"
OUTPUT = Path("output/punctuality.csv")
THRESHOLD_SECONDS = 180

def _query(source: str, output: Path, threshold_seconds: int) -> str:
    return f"""
COPY (
    WITH arrivals AS (
        SELECT
            BETRIEBSTAG,
            date_diff('second', strptime(ANKUNFTSZEIT, '%d.%m.%Y %H:%M'), AN_PROGNOSE) AS delay_seconds
        FROM '{source}'
        WHERE upper(PRODUKT_ID) = 'ZUG'
          AND AN_PROGNOSE_STATUS = 'REAL'
          AND ANKUNFTSZEIT IS NOT NULL
          AND NOT FAELLT_AUS_TF
    )
    SELECT
        BETRIEBSTAG,
        count(*) AS total,
        count(*) FILTER (WHERE delay_seconds <= {threshold_seconds}) AS on_time,
        count(*) FILTER (WHERE delay_seconds <= {threshold_seconds}) * 100.0 / count(*) AS percentage
    FROM arrivals
    GROUP BY BETRIEBSTAG
    ORDER BY BETRIEBSTAG
) TO '{output}' (HEADER, DELIMITER ',')
"""


def punctuality(
        source: str = PROCESSED, 
        output: Path = OUTPUT, 
        threshold_seconds: int = THRESHOLD_SECONDS,
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True) 
    duckdb.sql(_query(source, output, threshold_seconds))
    return output  


if __name__ == "__main__":
    print(punctuality())