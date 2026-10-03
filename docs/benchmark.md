# Mesures

## Conversion CSV → Parquet 
| Format | Taille | Lignes |
| --- | --- | --- |
| CSV | 608 Mo | 2 516 573 |
| Parquet | 43 Mo | 2 516 573 |

Facteur de compression : 14x. Estimation pour un an : 220 Go en CSV, 16 Go en Parquet.


# Mesures

## Conversion CSV → Parquet 
| Format | Taille |
| --- | --- |
| CSV | 608 Mo |
| Parquet | 43 Mo |

Facteur 14. Un mois : 18 Go en CSV, 1,2 Go en Parquet.

## Agrégation DuckDB
Comptage par jour sur 29 fichiers Parquet (~71 M de lignes) : **0,1 s** 
