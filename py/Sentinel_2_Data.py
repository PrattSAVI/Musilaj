#%% VIEW Boundary
import folium 

m = folium.Map([40.5643,29.9145], zoom_start=6)
boundsdata = r"C:\Users\csucuogl\Desktop\test\Istanbul.geojson"
folium.GeoJson(boundsdata).add_to(m)
m

# %% Calculate Footprint
# Start User
from sentinelsat import SentinelAPI
from sentinelsat import geojson_to_wkt
from sentinelsat import read_geojson

user = 'cansucuoglu' ## change this!
password = 'exploited_123' ## change this!

api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

footprint = geojson_to_wkt(read_geojson(boundsdata))

print (footprint)

# %% Get Boundaries
products = api.query(footprint,
                     date = ('20210523', '20210608'),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0, 20))

# %% See overlapping geometry
import matplotlib.pyplot as plt
import geopandas as gpd

areas = api.to_geodataframe(products)
areas['i'] = [i for i in range(len(areas))]

gdf2 = gpd.read_file(boundsdata)

areas = areas[ areas['i'].isin( [1,3,5,6,7,8,21] ) ]

f, ax = plt.subplots(1)
areas.to_crs(epsg=3857).plot(ax=ax,column='uuid',cmap=None,alpha=0.35)
areas.to_crs(epsg=3857).apply(lambda x: ax.annotate(s=x.i, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
gdf2.to_crs(epsg=3857).plot(ax=ax , facecolor='None' , edgecolor='red')
ctx.add_basemap(ax)
plt.show()
# %% Choose One to Start
import contextily as ctx
print( len( areas ))

# 1 Kapidag
# 3 Guney Dogu Marmara
# 5 Canakkale Korfez
# 6 Istanbul / Izmit
# 7 istanbul
# 8 Kuzey Bati
# 21 Izmit Korfez


single = areas[ areas['i'] == 6 ]
ax = single.to_crs(epsg=3857).plot( alpha = 0.25)
gdf2.to_crs(epsg=3857).plot(ax=ax , facecolor='None' , edgecolor='red')
ctx.add_basemap(ax)
print( single['title'].tolist() )

#%%
import contextily as ctx
print( len( areas ))
areas['i'] = [i for i in range(len(areas))]

# 1 Kapidag
# 3 Guney Dogu Marmara
# 5 Canakkale Korfez
# 6 Istanbul / Izmit
# 7 istanbul
# 8 Kuzey Bati
# 21 Izmit Korfez

all = [1,3,5,6,7,8,21]

for a in all:
    single = areas[ areas['i'] == a ]
    #ax = single.to_crs(epsg=3857).plot( alpha = 0.25)
    #gdf2.to_crs(epsg=3857).plot(ax=ax , facecolor='None' , edgecolor='red')
    #ctx.add_basemap(ax)
    #display( single[['uuid']] )
    api.download( single['uuid'].tolist()[0])



# %%
