import pandas as pd
import geopandas as gpd
import plotly.express as px
import numpy as np

df_csv = pd.read_csv(r"Dataset/Agricultura.csv")
gdf = gpd.read_file(r"Dataset/india_state.geojson")

# FILTRAR DATAFRAME:
df_csv = pd.read_csv(r"Dataset/Agricultura.csv")

df_csv['State'] = df_csv['State'].replace({'Jammu & Kashmir' : 'Jammu and Kashmir', 'Odisha': 'Orissa', 'Uttarakhand': 'Uttaranchal'})

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

print(df["State"].unique())

df.to_csv("Agricultura_F.csv", index=False)

def agrupar_df(variable):
    dataframe = df.groupby(variable)[["Production", "Area", "Yield"]].agg({
        'Production': 'sum',
        'Area': 'sum',
        'Yield': 'sum'}
    )
    return dataframe.reset_index()

# FILTRAR GEODATAFRAME:

gdf = gdf.sort_values(by="NAME_1")

def agrupar_df(variable):
    dataframe = df.groupby(variable)[["Production", "Area", "Yield"]].agg({
        'Production': 'sum',
        'Area': 'sum',
        'Yield': 'sum'}
    )
    return dataframe.reset_index()

state = agrupar_df("State")

# Ver elementos Diferentes
estados = set(df['State'].unique())
estadosgeo = set(gdf["NAME_1"].unique())
print(estados - estadosgeo)

# Reemplazar Elementos
df['State'] = df['State'].replace({'Jammu & Kashmir' : 'Jammu and Kashmir', 'Odisha': 'Orissa', 'Uttarakhand': 'Uttaranchal'})

# Ver Elementos que Coinciden
estados = set(df['State'].unique())
estadosgeo = set(gdf["NAME_1"].unique())
print(estados - estadosgeo)

gdf_final = gdf.merge(state, left_on='NAME_1', right_on=df, how='left')
gdf_final = gdf_final.drop(columns=['State'])

gdf_final['Production_log'] = np.log10(gdf_final['Production'] + 1)
gdf_final['Area_log'] = np.log10(gdf_final['Area'] + 1)
gdf_final['Yield_log'] = np.log10(gdf_final['Yield'] + 1)

gdf_final[['Production_log', 'Area_log', 'Yield_log']] = gdf_final[['Production_log', 'Area_log', 'Yield_log']].fillna(-1)

gdf_final.to_file('India_Filtrado.geojson',driver='GeoJSON' ,index=False)

