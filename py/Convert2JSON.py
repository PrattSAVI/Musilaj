
#%%
import pandas as pd

df = pd.read_csv( r"C:\Users\csucuogl\Dropbox\Musilaj_Test\Tweets.csv" )
print( "{} adet twit var".format(len(df)) )
df.head()


#%%

import requests

a=[]
for i,r in df.iterrows():
    #print( r['link'] )

    params = {
        'omit_script': '1',
        'maxheight':300,
        'limit':1
        }

    links = 'https://publish.twitter.com/oembed?url={}'.format(r['link'])
    resp = requests.get( links , params=params )
    try:
        data = resp.json()
        a.append( data['html'] )
    except:
        #print (resp.text )
        print( r['link'])
        a.append( None )


df['embed'] = a

df

# %%

df = df[['embed','lat','lon']]
#df['date'] = pd.to_datetime( df['date'])


df.head()

# %%

df.to_json(r'C:\Users\csucuogl\Documents\GitHub\Musilaj\Data\tw\Tweets.json' , orient='records')
# %%
