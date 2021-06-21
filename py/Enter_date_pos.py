
# %%

import os
import pandas as pd

path = r'C:\Users\csucuogl\Documents\GitHub\Musilaj\apis\composite'

files = os.listdir( path )
files = [ i for i in files if i.split('.')[1] == 'geojson']
names = [ i.split('.')[0] for i in files]
print ( names )

# %%

df = pd.DataFrame( columns=['date','name'])

df['date'] = names
df

# %%

def conv_month(date):
    t = date.split("-")
    month = t[1]

    month_dict = {
        "01":"Ocak",
        "02":"Şubat",
        "03":"Mart",
        "04":"Nisan",
        "05":"Mayıs",
        "06":"Haziran",
        "07":"Temmuz",
        "08":"Ağustos",
        "09":"Eylül",
        "10":"Ekim",
        "11":"Kasım",
        "12":"Aralık"
    }

    for word, initial in month_dict.items():
        month = month.replace(word.lower(), initial)

    return "{}-{}-{}".format(t[2],month,t[0])


df['name'] = df['date'].apply( lambda x: conv_month(x) )


df

# %%

df.to_json( r"C:\Users\csucuogl\Documents\GitHub\Musilaj\apis\composite\dates.json" , orient='records' )

# %%
