
#%%
import pandas as pd

df = pd.read_csv( r"C:\Users\csucuogl\Dropbox\Musilaj_Test\Tweets.csv" )
df.head()
# %%

df = df[['link','loc','lat','lon','date']]
df['date'] = pd.to_datetime( df['date'])


df.head()

# %%

df.to_json(r'C:\Users\csucuogl\Dropbox\Musilaj_Test\Tweets.json' , orient='records')
# %%
