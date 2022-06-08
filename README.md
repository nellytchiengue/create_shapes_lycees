# Construction of shapefiles with python  - geopandas  

![image](https://user-images.githubusercontent.com/105495334/172506658-f718452d-0f96-4df1-8d07-384ae0975aa5.png)


Project purpose : 
Create shapefiles of France High Schol (Lycees) with  data gouv and INSEE statistics

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

lycees Exams results ( golden source !) 
https://data.education.gouv.fr/explore/dataset/fr-en-indicateurs-de-resultat-des-lycees-denseignement-general-et-technologique/table/
