# Profil des données Ist-Daten 

## Source 
- Site : opentransportdata.swiss, jeu de données "Ist-Daten v2" 
- Un fichier CSV par jour, environ 413 Mo 
- 1 709 145 lignes pour le 20 Septembre 2026 
- Une ligne = le passage d'un véhicule à un arrêt 

## Status des heures réelles 
- REAL : 88,4% -> heure vraiment mesurée 
- PROGNOSE, GESCHAETZT, UNBEKANNT : prévision ou estimation, pas une mesure 
- Décision : on calcule le retard uniquement sur REAL 

## Surprises 
- L'export de l'aperçu du site est tronqué à 1 664 000 lignes (2,6 % de perte), toujours utiliser l'URL directe 
- L'heure prévue n'a pas de secondes, l'heure réelle en a
- Le premier arrêt n'a pas d'arrivée, sauf chez TPG et TL 
- Doublons d'arrêts dans certaines courses 

- Le volume varie fortement selon le jour de la semaine dimanche 20/09 = 1,7 M de lignes, lundi 21/09 = 2,5 M. Un contrôle de volume devra comparer au même jour de la semaine précédente. 
-Le site bloque le User-Agent par défaut de Python (erreur 403). Le script s'identifie avec son propre nom 


