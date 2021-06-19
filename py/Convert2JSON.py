
#%%
import pandas as pd

df = pd.read_csv( r"C:\Users\csucuogl\Dropbox\Musilaj_Test\Tweets.csv" )
df.head()


#%%

import requests

a=[]
for i,r in df.iterrows():
    print( r['link'] )

    params = {
        'omit_script': '1',
        'maxheight':300,
        'limit':1

        }

    links = 'https://publish.twitter.com/oembed?url={}'.format(r['link'])
    resp = requests.get( links , params=params )
    data = resp.json()
    print(data['html'])
    a.append( data['html'] )

    break

#df['embed'] = a

#df

# %%

df = df[['embed','lat','lon','date']]
df['date'] = pd.to_datetime( df['date'])


df.head()

# %%

df.to_json(r'C:\Users\csucuogl\Dropbox\Musilaj_Test\Tweets.json' , orient='records')
# %%
