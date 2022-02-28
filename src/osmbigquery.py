import os
import pandas as pd
import numpy as np
import geopandas as gpd
from sklearn import cluster
from sklearn.preprocessing import LabelEncoder
import pathlib
from google.cloud import bigquery
from google.cloud.bigquery.client import Client
from sklearn.cluster import DBSCAN

 
def get_restaurants_bq(query_string):    
    print()
    bqclient = bigquery.Client()
  #Prepare Data --
    restaurants = (
        bqclient.query(query_string)
        .result()
        .to_dataframe(
            # Optionally, explicitly request to use the BigQuery Storage API. As of
            # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
            # API is used by default.
        )
    )
    attributescode = []
    attributes = ['shop', 'leisure', 'sport','building', 'entrance', 'crossing']
    lb_make = LabelEncoder()
  
  #Prepare Data --
    for atrib in attributes:
        newlabel=str(atrib+"code")
        restaurants[newlabel] = lb_make.fit_transform(restaurants[atrib])
        attributescode.append(newlabel)

   #Cluster --
    restaurants_geo = gpd.GeoDataFrame(restaurants, geometry=gpd.points_from_xy(restaurants.lon, restaurants.lat))
    restaurants_geo.crs = {'init': u'epsg:4326'}
    kmeans5 = cluster.KMeans(n_clusters=5).fit(restaurants_geo[attributescode])
    restaurants_geo['cluster_km2_id'] = kmeans5.labels_
    restaurants_geo['poi_id'] = restaurants_geo["id"]

    kmeans5 = cluster.KMeans(n_clusters=5).fit(restaurants_geo[['lon','lat']])
    restaurants_geo['cluster_km_id'] = kmeans5.labels_
    restaurants_geo['poi_id'] = restaurants_geo["id"]

   #DBSCAN
    COOR = np.array(restaurants_geo[['lon', 'lat']], dtype='float64')
    model = DBSCAN(eps=0.0005, min_samples=5).fit(COOR)
    restaurants_geo['cluster_db_id'] = model.labels_


   #Generate CSV FILE --
    csvheader=["lon","lat","cluster_km_id","cluster_db_id","cluster_km2_id","poi_id"]
    restaurants_csv = restaurants_geo[csvheader]
    filepath = str(pathlib.Path().absolute()) + "/restaurants.csv"
    #filepath.parent.mkdir(parents=True, exist_ok=True) 
    restaurants_csv.to_csv(filepath, index=False)

    return filepath