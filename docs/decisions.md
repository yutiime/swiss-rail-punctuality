# Décisions 

## Téléchargement via la page du jeu de données 
- Choix : le script lit la page HTML du jeu de données pour trouver le lien du fichier de chaque jour. 
- Pourquoi : l'API officielle (CKAN) refuse les requêtes sans clé d'accès (403). 
- Limite : la page ne liste que les jours récents. L'historique demandera l'archive mensuelle. Si la structure de la page change, passer une clé d'API. 
