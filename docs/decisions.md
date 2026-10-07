# Décisions 

## Téléchargement via la page du jeu de données 
- Choix : le script lit la page HTML du jeu de données pour trouver le lien du fichier de chaque jour. 
- Pourquoi : l'API officielle (CKAN) refuse les requêtes sans clé d'accès (403). 
- Limite : la page ne liste que les jours récents. L'historique demandera l'archive mensuelle. Si la structure de la page change, passer une clé d'API. 



## Comparaison avec le chiffre officiel des CFF

Mon résultat : 93,56 % (septembre 2026, seuil 3 min, tous opérateurs ferroviaires)
Chiffre CFF 2025 : 94,1 % (trafic voyageurs, seuil 3 min) — source : <https://reporting.sbb.ch/fr/ponctualite?=&years=1,4,5,6,7&scroll=0&highlighted=>

Écart de 0,5 point, explicable par quatre différences de méthode :

| Différence | Effet probable |
| --- | --- |
| Périmètre : tous les opérateurs chez moi, CFF seuls chez eux | tire mon chiffre vers le bas |
| Période : un mois contre une année entière | écart possible dans les deux sens |
| Les CFF publient aussi une ponctualité pondérée par le nombre de voyageurs | méthode différente de la mienne |
| Points de mesure : tous les arrêts chez moi, périmètre inconnu chez eux | effet incertain |