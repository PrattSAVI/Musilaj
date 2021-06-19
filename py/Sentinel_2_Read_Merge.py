

# This code merges all raster data in a folder.
# Data is from Sentinel Images. 
# Change the Env to one that can run full rasterio !!!!.
#%% DEPENDECIES
#Make sure the prefix is set to Remote Raster Env
import sys
import rasterio
import os
import pandas as pd
print( sys.prefix )

# %% Sentinel Folders

folder_path = r"D:\SAVI\Musilaj_Mapping\RasterData\210402"
folder_list = os.listdir( folder_path )

[i for i in folder_list]

#%% Create a file list for Bands.
# Creates a DF to use for merging

bands = ['B04','B11','B8A']
df = pd.DataFrame(columns=['folder','file','date','band'])

for band in bands:
    for this_file in folder_list:

        path = os.path.join( folder_path , this_file)
        path = os.path.join( path , "GRANULE")
        path = os.path.join( path , os.listdir( path )[0] )
        path = os.path.join( path , "IMG_DATA")
        path = os.path.join( path , "R20m")

        for i in os.listdir( path ):
            if (band in i) :

                date = i.split("_")[1].split("T")[0]
                data = [[path,i,date,band]]

                temp = pd.DataFrame( 
                    columns=['folder','file','date','band'],
                    data = data )
                df = df.append( temp )

df.index = [i for i in range(len(df))]
df['pos'] = [r.split('_')[0] for i,r in df['file'].iteritems()]

df = df[['pos','band','date','file','folder']]

df = df[ ~df['pos'].str.contains("TTL") ] #TTL is projected to N36 better remove it

df


#%% MERGE AND PLOT

import matplotlib.pyplot as plt
import numpy as np
from rasterio.merge import merge
from rasterio.plot import show

def merge_plot( df , band , filename):
    df4 = df.copy()
    display( df4 )

    images=[]

    for i,r in df4.iterrows():
        path = os.path.join( r['folder'] , r['file'] ) 
        dataset = rasterio.open( path )

        images.append( dataset )

    #Merge
    mosaic, out_transform =  merge(images)

    # test -> removing 0 value
    #mosaic = mosaic.astype( np.float32 )
    #mosaic[mosaic==0] = np.nan
    #print( mosaic.dtype )

    #Plot
    plt.figure( figsize = (12,8) )
    show( mosaic , cmap='terrain')

    out_fp = os.path.join( folder_path , filename )

    # Copy the metadata
    out_meta = dataset.meta.copy()

    # Update the metadata
    out_meta.update({"driver": "GTiff",
                    "height": mosaic.shape[1],
                    "width": mosaic.shape[2],
                    "transform": out_transform,
                    "crs": "+proj=utm +zone=35 +ellps=WGS84 +datum=WGS84 +units=m +no_defs ",
                    "dtype" : mosaic.dtype,
                    #"nodata": np.nan
                    }
                    )

    # Write the mosaic raster to disk
    with rasterio.open(out_fp, "w", **out_meta) as dest:
        dest.write(mosaic)

#Filter unique dates and bands and feed into the mergeplot
for b in df['band'].unique().tolist():
    temp1 = df[ df['band'] == b ]
    for t in temp1['date'].unique().tolist():

        temp2 = temp1[ temp1['date'] == t ]
        filename = '{}_{}_Can.tiff'.format(t,b)

        print( filename )
        merge_plot( temp2 , b , filename )

print("Done! Here are the bands")

# %% MERGE BANDS - OPEN
#Go One by one by changing the date at DATE

import os
import fiona
import rasterio.mask

img_path = folder_path # Bu ayni olmayabilir. !!!
date = "20210402" #Define a single date to process!!!!!
allf = os.listdir( img_path )

#Images
allf = [i for i in allf if i.split(".")[1]=="tiff" ]

#date
allf =  [i for i in allf if date in i ]
file_list = [os.path.join(img_path,i) for i in allf]
file_list = [file_list[0],file_list[2],file_list[1]]

file_list

# %% MERGE BANDS - SAVE

# Read metadata of first file
with rasterio.open(file_list[0]) as src0:
    meta = src0.meta

# Update meta to reflect the number of layers
meta.update(count = len(file_list))

tiff_path = os.path.join(img_path,'{}_MergeR.tif'.format(date))
# Read each layer and write it to stack
with rasterio.open( tiff_path, 'w', **meta) as dst:
    for id, layer in enumerate(file_list, start=1):
        with rasterio.open(layer) as src1:
            dst.write_band(id, src1.read(1))

print('Multi-band raster created!')
# %% MERGE BANDS - CLIP

with fiona.open( r"D:\SAVI\Musilaj_Mapping\GIS_Data\Coast_v3.shp" , "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

with rasterio.open( tiff_path ) as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta

out_meta.update({"driver": "GTiff",
                 #"dtype" : mosaic.dtype,
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                "crs": "+proj=utm +zone=35 +ellps=WGS84 +datum=WGS84 +units=m +no_defs ",
                 "transform": out_transform})

plt.figure( figsize = (12,8) )
show( out_image , cmap='terrain')

with rasterio.open( os.path.join(img_path,'{}_ClipR.tif'.format(date)) , "w", **out_meta) as dest:
    dest.write(out_image)

print("Image Transformed and Written!")

# %%
