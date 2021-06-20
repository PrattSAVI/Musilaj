#%%
import pandas as pd

path = r"C:\Users\csucuogl\Documents\GitHub\Musilaj\apis\dates.txt"

with open( path ) as f:
    output = [s for line in f.readlines() for s in line.split(',')]

output
# %%

df = pd.DataFrame( columns=['date','pos'])
df['date'] = output

df = df.set_index('date')

# %% assign times

df.loc['2021-04-02', 'pos'] = "marmara"
df.loc['2021-04-14', 'pos'] = "izmit"
df.loc['2021-04-22', 'pos'] = "marmara"
df.loc['2021-04-29', 'pos'] = "izmit"
df.loc['2021-05-14', 'pos'] = "izmit"
df.loc['2021-05-17', 'pos'] = "marmara"
df.loc['2021-05-19', 'pos'] = "izmit"
df.loc['2021-05-24', 'pos'] = "izmit"
df.loc['2021-06-06', 'pos'] = "marmara"
df.loc['2021-06-11', 'pos'] = "marmara"
df.loc['2021-06-13', 'pos'] = "izmit"

df
# %%

df.reset_index().to_json( r"C:\Users\csucuogl\Documents\GitHub\Musilaj\apis\dates.json" , orient='records' )
# %%
