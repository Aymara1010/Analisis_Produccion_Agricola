import pandas as pd
import requests
import plotly.express as px
import numpy as np

# Cargar datos necesario
df_csv = pd.read_csv(r"Dataset/Agricultura.csv")

# datos geograficos
url = "https://raw.githubusercontent.com/Aymara1010/ayudenme/main/india_state.geojson"
geo = requests.get(url)
gdf = geo.json()


# FILTRAR DATAFRAME:

def categorizar_cultivos(data):
    categorias = {
    "Cereales y Granos": ["Rice", "Wheat", "Maize", "Barley", "Jowar", "Bajra", "Ragi", "Small millets", "Tapioca", "Sannhamp"],
    "Leguminosas": ["Arhar/Tur", "Gram", "Horse-gram", "Moong(Green Gram)", "Urad", "Cowpea(Lobia)", "Moth", "Khesari", "Masoor", "Peas & beans (Pulses)"],
    "Oleaginosas": ["Groundnut", "Sesamum", "Sunflower", "Soyabean", "Rapeseed &Mustard", "Castor seed", "Linseed", "Safflower", "Niger seed", "other oilseeds", "Oilseeds total"],
    "Especias, Tubérculos y Hortalizas": ["Dry chillies", "Turmeric", "Cardamom", "Coriander", "Garlic", "Ginger", "Black pepper", "Onion", "Potato", "Sweet potato"],
    "Fibras ": ["Cotton(lint)", "Mesta" ],
    "Cultivos Industriales": ["Sugarcane","Tobacco","Guar seed"],
    "Frutales": ["Coconut ","Arecanut","Cashewnut","Banana"]
    }
    for cat, lista in categorias.items():
        data.loc[data["Crop"].isin(lista), "Crop_Type"] = cat
        
    return data

df = df_csv[(df_csv["Season"] == "Whole Year ") & (df_csv["Crop_Year"] < 2010)][["Crop_Year", "State", "Crop", "Production", "Area", "Yield"]]
df = categorizar_cultivos(df)
df = df.sort_values(by="State")


# Extraer estados del geojson
nombres_geo = [f['properties']['NAME_1'] for f in gdf['features']]
df_geo = pd.DataFrame({'State': nombres_geo})

# ver si hay estados faltantes
estados = set(df['State'].unique())
estadosgeo = set(df_geo["State"].unique())
print(estados - estadosgeo)

# cambiar nombre de los estados faltantes
df['State'] = df['State'].replace({'Jammu & Kashmir' : 'Jammu and Kashmir', 'Odisha': 'Orissa', 'Uttarakhand': 'Uttaranchal'})

print(df["State"].unique())

df.to_csv("Dataset/Agricultura_Filtrado.csv", index=False)





