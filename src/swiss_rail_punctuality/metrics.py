from pathlib import Path

import duckdb

PROCESSED = "data/processed/*.parquet"
OUTPUT = Path("output/punctuality.csv")
SEUIL_S = 180

def _query(source: str, output: Path, seuil_s: int) -> str: 
    return f"""
COPY (
    WITH arrivees AS (
        SELECT
            BETRIEBSTAG,
            date_diff('second', strptime(ANKUNFTSZEIT, '%d.%m.%Y %H:%M'), AN_PROGNOSE) AS retard_s
        FROM '{source}'
        WHERE upper(PRODUKT_ID) = 'ZUG'
          AND AN_PROGNOSE_STATUS = 'REAL'
          AND ANKUNFTSZEIT IS NOT NULL
          AND NOT FAELLT_AUS_TF
    )
    SELECT
        BETRIEBSTAG,
        count(*) AS total,
        count(*) FILTER (WHERE retard_s <= {seuil_s}) AS a_lheure,
        count(*) FILTER (WHERE retard_s <= {seuil_s}) * 100.0 / count(*) AS pourcentage
    FROM arrivees
    GROUP BY BETRIEBSTAG
    ORDER BY BETRIEBSTAG
) TO '{output}' (HEADER, DELIMITER ',')
"""


def punctuality(
        source: str = PROCESSED, 
        output: Path = OUTPUT, 
        seuil_s: int = SEUIL_S, 
) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True) 
    duckdb.sql(_query(source, output, seuil_s))  
    return output  


if __name__ == "__main__":
    print(punctuality())