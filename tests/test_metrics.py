from pathlib import Path

import duckdb

from swiss_rail_punctuality.metrics import punctuality

FIXTURE = "tests/fixtures/sample.parquet"


def test_produit_un_fichier(tmp_path: Path):
    out = punctuality(source=FIXTURE, output=tmp_path / "r.csv")
    assert out.exists()
    assert out.stat().st_size > 0    


def test_colonnes_coherentes(tmp_path: Path):
    out = punctuality(source=FIXTURE, output=tmp_path / "r.csv")
    rows = duckdb.sql(f"SELECT * FROM '{out}'").fetchall()
    # pour chaque ligne : a_lheure <= total, et 0 <= pourcentage <= 100  
    for jour, total, a_lheure, pourcentage in rows: 
        assert a_lheure <= total 
        assert 0 <= pourcentage <= 100  
     


def test_seuil_plus_large_donne_plus_de_ponctuels(tmp_path: Path):
    # appelle punctuality deux fois, seuil_s=0 puis seuil_s=3600
    # le total de a_lheure doit être >= dans le second cas
    strict = punctuality(source= FIXTURE, output= tmp_path / "strict.csv", seuil_s= 0)   
    large = punctuality(source= FIXTURE, output= tmp_path / "large.csv", seuil_s= 3600)
    n_strict = duckdb.sql(f"SELECT sum(a_lheure) FROM '{strict}'").fetchone()[0]
    n_large = duckdb.sql(f"SELECT sum(a_lheure) FROM '{large}'").fetchone()[0]
    assert n_large >= n_strict
 
      