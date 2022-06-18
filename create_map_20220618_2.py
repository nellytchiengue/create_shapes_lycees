'''
Project purpose : 
Create shapefiles of France High Schol (Lycees) with  data gouv and INSEE statistics
The DOM TOM are not included

'''

import datetime
import pandas as pd

import geopandas as gpd
import pyproj


import plotly.express as px
import plotly.io as pio
import plotly.offline as offline
from plotly.offline import init_notebook_mode, iplot, plot
from plotly.graph_objs import Scatter, Figure, Layout, Bar
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# display all columns in df
pd.set_option("display.max_columns", None)

#  plot figures in browser
pio.renderers.default = "browser"

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# GLOBAL DEFINITION - VARIABLES
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

shp_folder = "outputs\\shp\\"

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# IMPORT DATA
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#  --------------------------------------------------------------------------------------
# Import academies geo data from shapefiles 
print ( "Loading academies geo ...")
gdf_academies = gpd.read_file(shp_folder + "IRIS_academies.shp")
gdf_academies

#  basic plot
gdf_academies.plot(figsize = (24,10)).axis('off')

# plot with some colors
gdf_academies.plot(column='MENTIONS_R'
                        , cmap='winter'
                        , scheme='quantiles'
                        ,figsize = (24,10)
                        ).axis('off')

gdf_academies.sort_values( by = ["MENTIONS_R"])

#  --------------------------------------------------------------------------------------
#  --------------------------------------------------------------------------------------
# Import geo data from shapefiles 
print ( "Loading lycees geo ...")
geo_df_lycees = gpd.read_file(shp_folder + "IRIS_lycees.shp")
geo_df_lycees
geo_df_lycees.plot(figsize = (24,10)).axis('off')

# plot with some colors
geo_df_lycees.plot(column='MENTIONS_R'
                        , cmap='winter'
                        , scheme='quantiles'
                        ,figsize = (48,20)
                        ).axis('off')

# geo_df_lycees["Annee"].unique

#  data cleaning : keep necessary columns
geo_df_lycees.columns
# ['UAI', 'Annee', 'Etablissem', 'libelle_ac', 'code_commu', 'INSEE_COM',
#        'NOM_COM', 'Ville', 'libelle_co', 'code_depar', 'libelle_de',
#        'code_regio', 'libelle_re', 'CODE_IRIS', 'NOM_IRIS', 'SUCCESS_R',
#        'SUCCESS_R_', 'MENTIONS_R', 'MENTIONS_1', 'distances', 'geometry'
# ]


geo_df_lycees['Academie'] = geo_df_lycees['libelle_ac'] 
geo_df_lycees['High School'] = geo_df_lycees['Etablissem'] 
geo_df_lycees['Sucess Rate'] = geo_df_lycees['SUCCESS_R_'] 
geo_df_lycees['Mention Rate'] = geo_df_lycees['MENTIONS_R'] 
geo_df_lycees['City'] = geo_df_lycees['NOM_COM'] 


#  set index
geo_df_lycees = geo_df_lycees.reset_index().set_index("UAI")

fig = px.choropleth(geo_df_lycees[geo_df_lycees["Annee"]==2021],
                    geojson=geo_df_lycees.geometry,
                    locations=geo_df_lycees.index,
                    color="Mention Rate" #  "Sucess Rate"
                    ,projection="mercator"
                    ,color_continuous_scale = "greens"
                    # ,basemap_visible = "carto-positron"
                    ,hover_data = ['Academie'
                                    ,'High School'
                                    ,'City'
                                    ,'Sucess Rate'
                                ]  
                   )

fig.update_geos(fitbounds="locations", visible=False)


fig.update_traces(marker_line_width=0.5
                    ,marker_line_color = "grey"
                    ,marker_opacity=0.9
                )

fig.show()


#----------------------------------------------------------------
#   ZOOM -  only Paris area
gdf_map2 = geo_df_lycees[geo_df_lycees['libelle_re']== "Ile-de-France"]
#  set index
gdf_map2 = gdf_map2.reset_index().set_index("UAI")

fig2 = px.choropleth(gdf_map2,
                    geojson=gdf_map2.geometry,
                    locations=gdf_map2.index,
                    color="Mention Rate" #  "Sucess Rate"
                    ,projection="mercator"
                    ,color_continuous_scale = "greens"
                    # ,basemap_visible = "carto-positron"
                    ,hover_data = ['Academie'
                                    ,'High School'
                                    ,'City'
                                    ,'Sucess Rate'
                                ]  
                   )
fig2.update_geos(fitbounds="locations", visible=False)
fig2.update_traces(marker_line_width=0.5
                    ,marker_line_color = "grey"
                    ,marker_opacity=0.9
                )

fig2.show()

#  generate fig in interactive HTML
fig2.write_html("outputs\\html\\fig_lycees_paris.html")





#  --------------------------------------------------------------------------------------
#  --------------------------------------------------------------------------------------
# interactive map for academies

gdf_academies.columns
['index', 'libelle_ac', 'Annee', 'code_regio', 'libelle_re', 'SUCCESS_R',
       'SUCCESS_R_', 'MENTIONS_R', 'MENTIONS_1', 'distances', 'geometry',
       'Sucess Rate', 'Mention Rate'
]

#----------------------------------------------------------------
#  set index

gdf_academies['Academie'] = gdf_academies['libelle_ac'] 
# gdf_academies['High School'] = gdf_academies['Etablissem'] 
gdf_academies['Sucess Rate'] = gdf_academies['SUCCESS_R_'] 
gdf_academies['Mention Rate'] = gdf_academies['MENTIONS_R'] 
# gdf_academies['City'] = gdf_academies['NOM_COM'] 

gdf_academies = gdf_academies.reset_index().set_index("Academie")

fig_ac = px.choropleth(gdf_academies[gdf_academies["Annee"]==2021],
                    geojson=gdf_academies.geometry,
                    locations=gdf_academies.index,
                    color="Mention Rate" #  "Sucess Rate"
                    ,projection="mercator"
                    ,color_continuous_scale = "greens"
                    # ,basemap_visible = "carto-positron"
                    # ,hover_data = ['Academie' ,'Sucess Rate' ]  
                    # ,text = gdf_academies["Academie"]
                    # ,opacity=0.5
                   )

fig_ac.update_geos(fitbounds="locations", visible=False)


fig_ac.update_traces(marker_line_width=0.5
                    ,marker_line_color = "grey"
                    ,marker_opacity=0.7
                )

#  --------------------------------------------------------------------
#  ajout des points de centroides sur la carte

#  set CRS to flat surface with Lambert 
gdf_academies = gdf_academies.to_crs(epsg=27572) # (epsg=27572) # ("EPSG:27572") # Lambert

# create new columns for centroid
gdf_academies["CENTROID_Y"] = gdf_academies.centroid.y
gdf_academies["CENTROID_X"] = gdf_academies.centroid.x

#  put back CRS EPSG:27572
# gdf_academies = gdf_academies.to_crs(epsg=4326)  
gdf_academies = gdf_academies.to_crs(pyproj.CRS.from_epsg(4326)) #
# gdf_academies.crs

fig_centroid = px.scatter_geo(  gdf_academies
                        ,lat=gdf_academies.geometry.centroid.y
                        ,lon=gdf_academies.geometry.centroid.x
                        # ,lat=gdf_academies["CENTROID_Y"]
                        # ,lon=gdf_academies["CENTROID_X"]
                        # ,hover_name="Libellé entité"
                        ,text = "libelle_ac" # gdf_academies.geometry # "Academie"
                        ,opacity = 0.9
                        ,projection="mercator"
                    )

# put styles 
fig_centroid.update_traces(mode="text",
                            # mode="markers+text",
                            # textposition="middle left",
                            textfont=dict(size=12,
                            color="grey"),
                            showlegend=False,
                )

# add trace to previous choropleth map
fig_ac.add_trace(fig_centroid.data[0])      



fig_ac.show()
#  generate fig in interactive HTML
# fig_ac.write_html("outputs\\html\\fig_academies_label1.html")
fig_ac.write_html("outputs\\html\\fig_academies.html")

