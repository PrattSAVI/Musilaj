

#%%
import sys
print( sys.prefix )

# %% OPEN AND MERGE DATA / IMAGE

import rasterio
import os

folder_path = r'C:\Users\csucuogl\Dropbox\Musilaj_Test\210606'
folder_list = os.listdir( folder_path )

print ( folder_list )


#%% Create a file list for Bands.
# Creates a DF to use for merging

import pandas as pd

bands = ['B04','B11','B8A']
df = pd.DataFrame(columns=['folder','file','date','band'])

for band in bands:
    for this_file in folder_list:
        #print ( this_file )
        #print( this_file.split("_")[-1].split("T")[0] )

        path = os.path.join( folder_path , this_file)
        path  = os.path.join( path , this_file+".SAFE" )
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

df

#%% MERGE AND PLOT

import matplotlib.pyplot as plt
import numpy as np

df['pos'] = [r.split('_')[0] for i,r in df['file'].iteritems()]

def merge_plot( df , band , filename):
    df4 = df[ (df['band'] == band ) ]
    display( df4 )

    images=[]

    for i,r in df4.iterrows():
        if i!=6 : #Check this
            path = os.path.join( r['folder'] , r['file'] ) 
            dataset = rasterio.open( path )
            images.append( dataset )

    #Merge
    mosaic, out_transform =  rasterio.merge.merge(images)

    #Plot
    plt.figure( figsize = (12,8) )
    rasterio.plot.show( mosaic , cmap='terrain')

    out_fp = os.path.join( folder_path , filename )

    # Copy the metadata
    out_meta = dataset.meta.copy()

    # Update the metadata
    out_meta.update({"driver": "GTiff",
                    "height": mosaic.shape[1],
                    "width": mosaic.shape[2],
                    "transform": out_transform,
                    "crs": "+proj=utm +zone=35 +ellps=WGS84 +datum=WGS84 +units=m +no_defs "
                    }
                    )

    # Write the mosaic raster to disk
    with rasterio.open(out_fp, "w", **out_meta) as dest:
        dest.write(mosaic)


for b in bands:
    merge_plot( df , b , '210606_{}.tiff'.format(b) )



# %%
