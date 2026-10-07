from pathlib import Path

import duckdb

PROCESSED = "data/processed/*.parquet"
OUTPUT = Path("output/punctuality.csv")
SEUIL_S = 180

QUERY = f"""
COPY (
    WITH arrivees AS (
        SELECT
            BETRIEBSTAG,
            date_diff('second', strptime(ANKUNFTSZEIT, '%d.%m.%Y %H:%M'), AN_PROGNOSE) AS retard_s
        FROM '{PROCESSED}'
        WHERE upper(PRODUKT_ID) = 'ZUG'
          AND AN_PROGNOSE_STATUS = 'REAL'
          AND ANKUNFTSZEIT IS NOT NULL
          AND NOT FAELLT_AUS_TF
    )
    SELECT
        BETRIEBSTAG,
        count(*) AS total,
        count(*) FILTER (WHERE retard_s <= {SEUIL_S}) AS a_lheure,
        count(*) FILTER (WHERE retard_s <= {SEUIL_S}) * 100.0 / count(*) AS pourcentage
    FROM arrivees
    GROUP BY BETRIEBSTAG
    ORDER BY BETRIEBSTAG
) TO '{OUTPUT}' (HEADER, DELIMITER ',')
"""


def punctuality() -> Path:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True) 
    duckdb.sql(QUERY) 
    return OUTPUT 


if __name__ == "__main__":
    print(punctuality())