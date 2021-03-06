#%% VIEW Boundary
import folium 
import sys
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
import pandas as pd

print( sys.prefix )

m = folium.Map([40.5643,29.9145], zoom_start=6)
boundsdata = r"C:\Users\csucuogl\Desktop\test\Istanbul.geojson"
folium.GeoJson(boundsdata).add_to(m)
m

# %% Calculate Footprint
# Start User -> enter Password
from sentinelsat import SentinelAPI
from sentinelsat import geojson_to_wkt
from sentinelsat import read_geojson

user = 'cansucuoglu'
password = '' #sifre_123

api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
footprint = geojson_to_wkt(read_geojson(boundsdata))

print (footprint)

# %% Prepare Products
# See overlapping geometry

products = api.query(footprint,
                     date = ('20210617', '20210619'),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0, 90))

areas = api.to_geodataframe(products)
areas['i'] = [i for i in range(len(areas))]

areas['date'] = pd.to_datetime( areas['generationdate'] )
areas['date2'] = areas['date'].dt.strftime('%m/%d') #convert to month/day


gdf2 = gpd.read_file(boundsdata)
areas[['title','date2']]

#%% Start with some dates.

#All dates on May, check EO Browser to note dates
#dates = ['05/14','05/12','05/09']
dates = ['06/18']

areas = areas[ areas['date2'].isin(dates) ].copy() # Only for these days
areas = areas[ ~areas['title'].str.contains("TTL") ] #Yamuk Projeksiyonlu
areas = areas[ ~areas['title'].str.contains("TTK") ] #Yamuk Projeksiyonlu


print( len(areas))
areas[['title','date2']]

#%% REMOVE THIS CELL
#This is for removing specific tiles, if they have been downloaded

areas = areas[ areas['title'].str.contains("T35TNE|T35TNF") ]

areas


#%% Plot all and Check

for i in dates:

    temp = areas[ areas['date2'] == i ].copy()

    print(i)

    f, ax = plt.subplots(1)
    temp.to_crs(epsg=3857).plot(ax=ax,column='uuid',cmap=None,alpha=0.35)
    temp.to_crs(epsg=3857).apply(lambda x: ax.annotate(text=x.i, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
    gdf2.to_crs(epsg=3857).plot(ax=ax , facecolor='None' , edgecolor='red')
    ctx.add_basemap(ax)
    plt.show()


# %% DOWNLOAD

print( len(areas) )

for i,r in areas.iterrows():
    try:
        api.download( r['uuid'] )
    except:
        print( r['uuid'] )

# %%
