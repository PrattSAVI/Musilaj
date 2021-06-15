#%% VIEW Boundary
import folium 
import sys
import matplotlib.pyplot as plt
import geopandas as gpd

print( sys.prefix )

m = folium.Map([40.5643,29.9145], zoom_start=6)
boundsdata = r"C:\Users\csucuogl\Desktop\test\Istanbul.geojson"
folium.GeoJson(boundsdata).add_to(m)
m

# %% Calculate Footprint
# Start User
from sentinelsat import SentinelAPI
from sentinelsat import geojson_to_wkt
from sentinelsat import read_geojson

user = 'cansucuoglu'
password = ''#sifre_123

api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
footprint = geojson_to_wkt(read_geojson(boundsdata))

print (footprint)

# %% Prepare Products
# See overlapping geometry

products = api.query(footprint,
                     date = ('20210611', '20210614'),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0, 30))


import contextily as ctx
areas = api.to_geodataframe(products)
areas['i'] = [i for i in range(len(areas))]

gdf2 = gpd.read_file(boundsdata)

f, ax = plt.subplots(1)
areas.to_crs(epsg=3857).plot(ax=ax,column='uuid',cmap=None,alpha=0.35)
areas.to_crs(epsg=3857).apply(lambda x: ax.annotate(s=x.i, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
gdf2.to_crs(epsg=3857).plot(ax=ax , facecolor='None' , edgecolor='red')
ctx.add_basemap(ax)
plt.show()

# %% Choose One to Start
import contextily as ctx
print( len( areas ))

single = areas[ areas['i'] == 9 ]
ax = single.to_crs(epsg=3857).plot( alpha = 0.25)
gdf2.to_crs(epsg=3857).plot(ax=ax , facecolor='None' , edgecolor='red')
ctx.add_basemap(ax)
print( single['title'].tolist() )

#%% Plot one last time

import contextily as ctx
print( len( areas ))

remove = [1,2,3]

single = areas[ ~areas['i'].isin(remove) ]
ax = single.to_crs(epsg=3857).plot( alpha = 0.25)
gdf2.to_crs(epsg=3857).plot(ax=ax , facecolor='None' , edgecolor='red')
single.to_crs(epsg=3857).apply(lambda x: ax.annotate(s=x.i, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
ctx.add_basemap(ax)


#%%
import contextily as ctx
remove = [1,2,3,7]

single = areas[ ~areas['i'].isin(remove) ]
print( len(single) )
for a in single['i'].unique().tolist():
    single = areas[ areas['i'] == a ]
    api.download( single['uuid'].tolist()[0] )



# %%
