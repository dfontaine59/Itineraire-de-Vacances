# Itineraire-de-Vacances

## Traitement :
- Recupération des fichiers 'https://diffuseur.datatourisme.fr/'
- Alimentation bdd SQL 
- Alimentation bdd Neo4J (coordonnées Lat/Lon)
- API pour récup d'un itinéraire 

## Application :
L'utilisateur choisit 
- une zone , clique sur des POI, une date et une durée de sejour  > l'algo propose un/des itinéraires 
- une zone/point de départ , un ou des centres d'intérêts (champ type) , choisit une date et une durée > l'algo propose un/des itinéraires

## -> Conclusion :
Input : 
- une adresse de départ 
(option 2 : une adresse d'arrivée) 
- le nombre de POI
- le nombre de km 
- les jours influent sur le nbre de POI

Ajouter des filtres : 
- type de POI
- attention aux restaurants et hotels 


Output : 
- itinéraire optimale dans le cluster le plus proche (optimal) du point de départ.
- Doit ressortir un mélange de type de POI
