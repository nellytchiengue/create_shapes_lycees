# Construction of shapefiles with python  - geopandas  

![image](https://user-images.githubusercontent.com/105495334/172506658-f718452d-0f96-4df1-8d07-384ae0975aa5.png)

Project purpose: create shapefiles in Python.
Data input: geographical french data with Data Gouv and INSEE statistics websites.

Steps:
1. create shapefiles of France High School (Lycees)
    -> create_shapes.py
2. create "simples" interactive map based on this shapefile
    -> create_map.py

The DOM TOM are not included

The Inputs are mainly the IRIS polygons and the x, y coordinates of each lycee

The map show above represents the result. Which is area linked to each High school in France.
The rule is : for each IRIS polygon find the nearest lycee then dissolve

Input / Sources

IRIS
https://www.data.gouv.fr/fr/datasets/contour-des-iris-insee-tout-en-un/#resources
    ( from  http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/notebooks/donnees_insee.html )


COMMUNES
https://public.opendatasoft.com/explore/dataset/georef-france-commune
    or
https://datanova.laposte.fr/explore/dataset/georef-france-commune

COLLEGES / Ecoles / Lycees
Academies geo data
https://www.data.gouv.fr/fr/datasets/contours-geographiques-des-academies/

Lycees geo data

https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre

Exams results of lycees

https://data.education.gouv.fr/explore/dataset/fr-en-indicateurs-de-resultat-des-lycees-denseignement-general-et-technologique/table/

Full description in article:
https://medium.com/@nellytchiengue/build-shapefiles-for-custom-map-with-python-and-geopandas-d92f424095f2

