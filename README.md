# Présentation projet Itineraire-de-Vacances

## Traitement :
- Recupération des fichiers 'https://diffuseur.datatourisme.fr/'
- Alimentation bdd SQL 
- Alimentation bdd Neo4J (coordonnées Lat/Lon)
- Creation cluster
- API pour récup d'un itinéraire / infos POI

## Application Streamlit :

Input :
L'utilisateur choisit 
 - une zone/point de départ : Ville / adresse précise ? TODO à specifier 
 - un ou des centres d'intérêts (champ type) 
 - une durée de sejour en nombre de jours
 - Nombre de points d'intérêts par jour

A étudier / Remarque 
- attention aux restaurants et hotels dans le choix des itinéraires

Output : 
L'algo propose un/des itinéraires 
- itinéraire optimal dans les clusters les plus proche (optimal) du point de départ.
- Doit ressortir un mélange de type de POI

---
# ETAPE 1 - Découverte des sources de données disponibles
cf [notebook de test de recolte de données](https://github.com/Slimanee/Itineraire-de-Vacances/blob/bda166ca69411896138194115fc3ca75501ec5dd/datascientest_itineraire_R%C3%A9colte_des_donn%C3%A9es.ipynb)

## 1- Récupération des données : 

**Source :** https://diffuseur.datatourisme.fr/fr/

> Nous avons tester la récupération d'un fichier unique JSON structuré généré via le site de Data Tourisme et d'un fichier CSV déjà créé sur data.gouv. <br>
A priori le JSON est de meilleur qualité. 

Pour ce projet nous choisissons la **région Auvergne-Rhones-Alpes**.
<br>

> Nous avons testé plusieurs moyens de récupération de fichiers.

> Le site https://diffuseur.datatourisme.fr/fr/ permet d'automatiser les flux, de choisir le format de sortie ainsi que le périmètre que nous voulons analyser

> Tests effectués avec les formats suivants :
- Fichiers json structurés
- Fichiers csv (liens http sur lesquels il faudrait faire du webscrapping pour récupérer les data des POI et un travail sur les longitudes/latitudes)
- Archive zip / fichier json (contient un ensemble de sous dossiers avec un json "entete" permettant d'obtenir le chemin et les data POI.)

> Les données datatourism sont aussi déposées de manière régulière sur le site https://www.data.gouv.fr/ . 
- fichier csv mis à jour quotidiennement

Pour ce projet nous avons fait le choix d'automatiser un flux sur le site https://diffuseur.datatourisme.fr/fr/ au format json qui contient les données nécessaires et nous avons choisi la **région Auvergne-Rhones-Alpes**. 
<br> 

## 2- Trie et nettoyage des données

> Nous avons effectué un premier nettoyage rapide, simple tout en gardant un maximum d'informations pour cette étape. <br>
Nous allons ensuite travailler sur la colonnne "type" des POI, qui nous permettra de relier les POI entre eux et de créer un filtre sur l'application. 

---
# ETAPE 2 - Modèle de données POSTGRES

## 2.1 Dans un premier temps nous avons intégré les données dans postgres selon le schéma suivant

![Diagram](https://github.com/Slimanee/Itineraire-de-Vacances/blob/e91044e6546c32e9fcf0c48a0030e5a5e0369eb0/Doc/Mod%C3%A8le%20donn%C3%A9es%20postgres.drawio.svg)

Cf. volumétrie des tables 
```sql
select count(*) from itineraire_poi;
-- 41310 lignes

select count(*) from itineraire_types;
-- 250893 lignes

select count(*) from classes_types;
-- 431 lignes

```

Le champ **type** du fichier json contient une liste des types de POI.
Ce champ type est le paramètre principal qui pourra servir dans l’interface utilisateur pour filtrer ses centres d’intérêts

## 2.2 Table classes_types
Nous avons construit cette table et ce « level » à partir des liens indiqués dans le fichier csv

https://gitlab.adullact.net/adntourisme/datatourisme/ontology/-/raw/master/Documentation/classes_fr.csv

Au niveau  1,  il y’a 4 grands types de POI : 
- **Product** : un objet touristique qui peut se consommer (ex: une chambre d'hôtel, une pratique d'activité, une visite guidée, ...)
- **Tour** : un itinéraire touristique est un POI qui propose un itinéraire composé d’étapes formant un parcours. 
- **EntertainmentAndEvent** : manifestations, festivals, exposition, ou tout autre évènement ayant un début et une fin
- **PlaceOfInterest** : un lieu ayant un intérêt touristique (ex: un site naturel, un site culturel, un village, un restaurant, ...)

```sql
select level , count(*) from classes_types
group by level
order by level;
```
| level | count   |
|-------|---------|
| 1     | 4       |
| 2     | 29      |
| 3     | 265     |
| 4     | 74      |
| 5     | 3       |
| null  | 56      |





