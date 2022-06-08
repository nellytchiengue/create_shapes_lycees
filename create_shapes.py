'''
Project purpose : 
Create shapefiles of France High Schol (Lycees) with  data gouv and INSEE statistics
The DOM TOM are not included

'''

# from xml.etree.ElementInclude import include
import datetime
# from email.errors import InvalidMultipartContentTransferEncodingDefect
import pandas as pd

import geopandas as gpd
# import pygeos
import pyproj
# from shapely.geometry import Point, Polygon
# from shapely.ops import nearest_points



# display all columns in df
pd.set_option("display.max_columns", None)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# GLOBAL DEFINITION - VARIABLES
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

data_folder =  "data\\"

IRIS_file_name ="iris-geo-2018-frtot.zip" # "reference_IRIS_geo2021.zip"
IRIS_file_path = data_folder + IRIS_file_name
print("IRIS_file_path : " + IRIS_file_path)

communes_file_name ="georef-france-commune.zip" # georef-france-commune.geojson"  # communes-20220101-shp.zip" # "reference_IRIS_geo2021.zip"
communes_file_path = data_folder + communes_file_name
print("communes_file_path : " + communes_file_path)

academies_file_name ="academies-20160209-shp.zip" 
academies_file_path = data_folder + academies_file_name
print("academies_file_path : " + academies_file_path)

etablissements_file_name ="fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.geojson" 
etablissements_file_path = data_folder + etablissements_file_name
print("etablissements_file_path : " + etablissements_file_path)

lycees_file_name ="fr-en-indicateurs-de-resultat-des-lycees-denseignement-general-et-technologique.csv" 
lycees_file_path = data_folder + lycees_file_name
print("lycees_file_path : " + lycees_file_path)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# IMPORT DATA
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

'''  Sources

IRIS
    https://www.data.gouv.fr/fr/datasets/contour-des-iris-insee-tout-en-un/#resources
    ( pris ici  http://www.xavierdupre.fr/app/ensae_projects/helpsphinx/notebooks/donnees_insee.html )


COMMUNES
    https://public.opendatasoft.com/explore/dataset/georef-france-commune
    or
    https://datanova.laposte.fr/explore/dataset/georef-france-commune


COLLEGES / Ecoles / Lycees
    Academie geo data
    https://www.data.gouv.fr/fr/datasets/contours-geographiques-des-academies/

    Lycees geo data
    https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre

    lycee Exams results ( golden source !) 
    https://data.education.gouv.fr/explore/dataset/fr-en-indicateurs-de-resultat-des-lycees-denseignement-general-et-technologique/table/

'''

# IMPORT IRIS
# iris-geo-2018-frtot.zip
print ( "Import IRIS...")
gdf_iris_all = gpd.read_file(IRIS_file_path)
gdf_iris_all
print ( "...Import IRIS... step 1 ok")
gdf_iris = gdf_iris_all
gdf_iris
# gdf_iris.plot(figsize = (24,10))
# gdf_iris["CD_CMN_INSEE_GEO"] = gdf_iris["insee"].astype("str")


# IMPORT Communes
# communes-20220101-shp.zip
print ( "Import Communes...")
gdf_communes_all = gpd.read_file(communes_file_path)
gdf_communes_all
print ( "...Import Communes --> OK")
gdf_communes = gdf_communes_all
gdf_communes
# gdf_communes.plot(figsize = (24,10))

# IMPORT COLLEGES
# Academies
print ( "Import Academies...")
gdf_academies_all = gpd.read_file(academies_file_path)
gdf_academies_all
print ( "...Import academies --> OK ")
gdf_academies = gdf_academies_all
gdf_academies
# gdf_academies.plot(figsize = (24,10))

# IMPORT etablissements geo
# fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.geojson
print ( "Import etablissements...")
gdf_etablissements_all = gpd.read_file(etablissements_file_path)
gdf_etablissements_all
print ( "...Import etablissements --> OK ")
gdf_etablissements = gdf_etablissements_all
gdf_etablissements

# IMPORT lycees Exams
# fr-en-indicateurs-de-resultat-des-lycees-denseignement-general-et-technologique.csv
print ( "Import lycees...")
df_lycees_all = pd.read_csv (lycees_file_path ,sep=';')
df_lycees_all
print ( "...Import lycees --> OK ")
df_lycees = df_lycees_all
df_lycees


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DATA EXPLORATION
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# CRS verification
gdf_iris.info()
gdf_iris.crs # Geographic 2D CRS: EPSG:4326
gdf_etablissements.crs # Geographic 2D CRS: EPSG:4326

# inspect a data value
df_lycees.info()
df_lycees.describe(include = "all")
df_lycees[df_lycees["UAI"].isin(["0010878Z"])]
df_lycees.columns.to_list()

#  a mettre en fonction pour analyser df et gdf
gdf_etablissements.info()
gdf_etablissements.describe(include = "all")
gdf_etablissements["code_commune"].unique()
gdf_etablissements.columns.to_list() 


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CLEAN DATA
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ----------------------------------------------------------------------
# IRIS data

# Delete DOM TOM areas
gdf_iris = gdf_iris[~gdf_iris["INSEE_COM"].str.startswith('97')]
# gdf_iris.plot(figsize = (24,10))
# CRS verification
gdf_iris.crs # Geographic 2D CRS: EPSG:4326


# ----------------------------------------------------------------------
# ETABLISSEMENTS data

# Delete DOM TOM areas
gdf_etablissements = gdf_etablissements[~gdf_etablissements["code_commune"].str.startswith('97')]
gdf_etablissements = gdf_etablissements[gdf_etablissements["geometry"]!=None]
gdf_etablissements


filterd_col_etablissements = [
    'boite_postale_uai',
    'lieu_dit_uai',
    'code_ministere',
    'code_region',
    'libelle_academie',
    'secteur_prive_code_type_contrat',
    'localisation',
    'date_ouverture',
    'code_postal_uai',
    'libelle_ministere',
    'libelle_departement',
    'adresse_uai',
    'code_academie',
    'secteur_prive_libelle_type_contrat',
    'code_commune',
    'nature_uai',
    'etat_etablissement_libe',
    'libelle_commune',
    'code_departement',
    'localite_acheminement_uai',
    'appariement',
    'etat_etablissement',
    'libelle_region',
    'numero_uai',
    'nature_uai_libe',
    'appellation_officielle',
    'epsg',
    'patronyme_uai',
    'denomination_principale',
    'secteur_public_prive_libe',
    'latitude',
    'coordonnee_y',
    'longitude',
    'coordonnee_x',
    'geometry'
 ]

gdf_etablissements = gdf_etablissements[filterd_col_etablissements]
gdf_etablissements 

# ----------------------------------------------------------------------
# LYCEES data
# Delete DOM TOM areas
df_lycees = df_lycees[~df_lycees["Code commune"].str.startswith('97')]
# delete lycee whitout mention
df_lycees = df_lycees.dropna(subset=['Taux de reussite - Gnle', 'Taux de mentions - Gnle'])
# keep only 2021 data
df_lycees = df_lycees[df_lycees["Annee"]==2021]
filtered_col_lycees = ['Etablissement',
                    'Annee',
                    'Ville',
                    'UAI',
                    'Taux de reussite - Gnle',
                    'Valeur ajoutee du taux de réussite - Gnle',
                    'Taux de mentions - Gnle',
                    'Valeur ajoutée du taux de mentions - Gnle'
                ]
df_lycees = df_lycees[filtered_col_lycees]
df_lycees


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  GEO DATAFRAME for SHAPEFILES
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# lycees with points geometry
# join / merge key with lycees data
gdf_etablissements["UAI"] = gdf_etablissements["numero_uai"]
gdf_etablissements = gdf_etablissements.merge(df_lycees, how="inner", on="UAI")
gdf_etablissements
# gdf_etablissements.plot(figsize = (24,10))


# then extend to Communes, departements, academies and regions


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  SHAPES CONSTRUCTION
# 1. Calculation of distances between IRIS and nearest Lycee ( Point from gdf_etablissements geometry)
# 2. Shapefiles  of Communes, departements, academies and regions
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

gdf_iris.crs
gdf_etablissements.crs

# we need to switch the ESPG to Lambert in order to compare distance...I think
gdf_iris_lambert = gdf_iris.to_crs(epsg=27572) # (epsg=27572) # ("EPSG:27572") # Lambert
gdf_etablissements_lambert = gdf_etablissements.to_crs(epsg=27572) # (epsg=27572) # ("EPSG:27572") # Lambert

# Attribution of a lycee for each IRIS78
print ("\n>>> START - Distance calculation and fit to IRIS to nearest points of Lycee - ")
print( datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# gdf_IRIS_merged_nearest = gdf_iris.sjoin_nearest(gdf_etablissements, distance_col="distances", how= "left") # prend tous les IRIS
gdf_IRIS_merged_nearest = gdf_iris_lambert.sjoin_nearest(gdf_etablissements_lambert, distance_col="distances", how= "left") # prend tous les IRIS

# display(gdf_IRIS_merged_nearest)
# gdf_IRIS_merged_nearest.tail()
print ("\n>>> END - Distance calculation " )
print( datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

gdf_IRIS_merged_nearest
gdf_IRIS_merged_nearest.crs

# gdf_IRIS_merged_nearest.plot(figsize = (24,10))

#  --------------------------------------------------------------------------------------
#  Dissolve polygons for ech level and creation of Shapefiles
#  --------------------------------------------------------------------------------------
# remettre au format geo lat long avant export file shp
gdf_IRIS_merged_nearest_WGS84 = gdf_IRIS_merged_nearest.to_crs(pyproj.CRS.from_epsg(4326))
gdf_IRIS_merged_nearest_WGS84

# remove Invalid geometry
gdf_IRIS_merged_nearest_WGS84 = gdf_IRIS_merged_nearest_WGS84[gdf_IRIS_merged_nearest_WGS84.is_valid]
# gdf_IRIS_merged_nearest_WGS84[~gdf_IRIS_merged_nearest_WGS84.is_valid]
gdf_IRIS_merged_nearest_WGS84

gdf_IRIS_merged_nearest_WGS84.columns


#  --------------------------------------------------------------------------------------
#  polygons with same NOM_COM = villes
cols_COM = ['Annee'
            # ,'UAI'	
            # ,'CODE_IRIS'
            # ,'NOM_IRIS'
            # ,'Etablissement'	
            ,'code_commune'
            ,'INSEE_COM'
            ,'NOM_COM'	
            ,'Ville'	
            ,'libelle_commune'
            # ,'code_departement'
            # ,'libelle_departement'
            ,'libelle_academie'
            ,'code_region'
            ,'libelle_region'
            ,'Taux de reussite - Gnle'
            ,'Valeur ajoutee du taux de réussite - Gnle'
            ,'Taux de mentions - Gnle'
            ,'Valeur ajoutée du taux de mentions - Gnle'
            , 'geometry'
            , 'distances'
    ]


gdf_IRIS_merged_nearest_WGS84[cols_COM ]
gdf_IRIS_COM  = gdf_IRIS_merged_nearest_WGS84[cols_COM].dissolve(by='INSEE_COM')
gdf_IRIS_COM 
# gdf_IRIS_lycees.tail()
gdf_IRIS_COM.plot(figsize = (36,15))

# create shapefile
gdf_IRIS_COM .to_file('outputs\shp\IRIS_communes.shp')  


#  --------------------------------------------------------------------------------------
#  Polygons with same UAI = lycee
cols_lycees = ['Annee'
            ,'UAI'	
            ,'Etablissement'	
            ,'libelle_academie'
            ,'code_commune'
            ,'INSEE_COM'
            ,'NOM_COM'	
            ,'Ville'	
            ,'libelle_commune'
            ,'code_departement'
            ,'libelle_departement'
            ,'code_region'
            ,'libelle_region'
            ,'CODE_IRIS'
            ,'NOM_IRIS'
            ,'Taux de reussite - Gnle'
            ,'Valeur ajoutee du taux de réussite - Gnle'
            ,'Taux de mentions - Gnle'
            ,'Valeur ajoutée du taux de mentions - Gnle'
            , 'geometry'
            , 'distances'
    ]


gdf_IRIS_merged_nearest_WGS84[cols_lycees]
gdf_IRIS_lycees = gdf_IRIS_merged_nearest_WGS84[cols_lycees].dissolve(by='UAI')
gdf_IRIS_lycees
# gdf_IRIS_lycees.tail()
gdf_IRIS_lycees.plot(figsize = (36,15))

# create shapefile
gdf_IRIS_lycees.to_file('outputs\shp\IRIS_lycees.shp')  



#  --------------------------------------------------------------------------------------
#  polygons with same departement
cols_departement = ['Annee'
            # ,'UAI'	
            # ,'CODE_IRIS'
            # ,'NOM_IRIS'
            # ,'Etablissement'	
            # ,'code_commune'
            # ,'INSEE_COM'
            # ,'NOM_COM'	
            # ,'Ville'	
            # ,'libelle_commune'
            ,'code_departement'
            ,'libelle_departement'
            ,'libelle_academie'
            ,'code_region'
            ,'libelle_region'
            ,'Taux de reussite - Gnle'
            ,'Valeur ajoutee du taux de réussite - Gnle'
            ,'Taux de mentions - Gnle'
            ,'Valeur ajoutée du taux de mentions - Gnle'
            , 'geometry'
            , 'distances'
    ]


gdf_IRIS_merged_nearest_WGS84[cols_departement ]
gdf_IRIS_departement = gdf_IRIS_merged_nearest_WGS84[cols_departement].dissolve(by='code_departement')
gdf_IRIS_departement
# gdf_IRIS_lycees.tail()
gdf_IRIS_departement.plot(figsize = (36,15))

# create shapefile
gdf_IRIS_departement .to_file('outputs\shp\IRIS_departements.shp')  

#  --------------------------------------------------------------------------------------
#  polygons with same academie
cols_academies = ['Annee'
            # ,'UAI'	
            # ,'CODE_IRIS'
            # ,'NOM_IRIS'
            # ,'Etablissement'	
            # ,'code_commune'
            # ,'INSEE_COM'
            # ,'NOM_COM'	
            # ,'Ville'	
            # ,'libelle_commune'
            # ,'code_departement'
            # ,'libelle_departement'
            ,'libelle_academie'
            ,'code_region'
            ,'libelle_region'
            ,'Taux de reussite - Gnle'
            ,'Valeur ajoutee du taux de réussite - Gnle'
            ,'Taux de mentions - Gnle'
            ,'Valeur ajoutée du taux de mentions - Gnle'
            , 'geometry'
            , 'distances'
    ]


gdf_IRIS_merged_nearest_WGS84[cols_academies ]
gdf_IRIS_academies  = gdf_IRIS_merged_nearest_WGS84[cols_academies].dissolve(by='libelle_academie')
gdf_IRIS_academies 
# gdf_IRIS_lycees.tail()
gdf_IRIS_academies.plot(figsize = (36,15))

# create shapefile
gdf_IRIS_academies .to_file('outputs\shp\IRIS_academies.shp')  


#  --------------------------------------------------------------------------------------
#  polygon with same region
cols_regions = ['Annee'
            # ,'UAI'	
            # ,'CODE_IRIS'
            # ,'NOM_IRIS'
            # ,'Etablissement'	
            # ,'code_commune'
            # ,'INSEE_COM'
            # ,'NOM_COM'	
            # ,'Ville'	
            # ,'libelle_commune'
            # ,'code_departement'
            # ,'libelle_departement'
            # ,'libelle_academie'
            ,'code_region'
            ,'libelle_region'
            ,'Taux de reussite - Gnle'
            ,'Valeur ajoutee du taux de réussite - Gnle'
            ,'Taux de mentions - Gnle'
            ,'Valeur ajoutée du taux de mentions - Gnle'
            , 'geometry'
            , 'distances'
    ]


gdf_IRIS_merged_nearest_WGS84[cols_regions]
gdf_IRIS_regions = gdf_IRIS_merged_nearest_WGS84[cols_regions].dissolve(by='code_region')
gdf_IRIS_regions
# gdf_IRIS_lycees.tail()
gdf_IRIS_regions.plot(figsize = (36,15))

# create shapefile
gdf_IRIS_regions.to_file('outputs\shp\IRIS_regions.shp')  





