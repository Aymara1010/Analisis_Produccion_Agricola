import pandas as pd
import plotly as px
import matplotlib.pyplot as plt
import seaborn as sb
import streamlit as st
import geopandas as gpd

df_csv = pd.read_csv(r"Dataset\Agricultura.csv")

# Filtrar variables y registros necesarios:
df = df_csv[(df_csv["Season"] == "Whole Year ") & (df_csv["Crop_Year"] < 2010)][["Crop_Year", "State", "Crop", "Production", "Area", "Yield"]]

# Función para recategorizar la variable Crop:
def categorizar_cultivos(data):
    categorias = {
    "Cereales y Granos": ["Rice", "Wheat", "Maize", "Barley", "Jowar", "Bajra", "Ragi", "Small millets", "Tapioca", "Sannhamp"],
    "Leguminosas": ["Arhar/Tur", "Gram", "Horse-gram", "Moong(Green Gram)", "Urad", "Cowpea(Lobia)", "Moth", "Khesari", "Masoor", "Peas & beans (Pulses)"],
    "Oleaginosas": ["Groundnut", "Sesamum", "Sunflower", "Soyabean", "Rapeseed &Mustard", "Castor seed", "Linseed", "Safflower", "Niger seed", "other oilseeds", "Oilseeds total"],
    "Especias, Tubérculos y Hortalizas": ["Dry chillies", "Turmeric", "Cardamom", "Coriander", "Garlic", "Ginger", "Black pepper", "Onion", "Potato", "Sweet potato"],
    "Cultivos Industriales, Fibras y Frutales": ["Coconut ", "Arecanut", "Cashewnut", "Banana", "Sugarcane", "Cotton(lint)", "Mesta", "Tobacco", "Guar seed"]
}
    for cat, lista in categorias.items():
        data.loc[data["Crop"].isin(lista), "Crop_Type"] = cat
        
    return data

# Aplicar función al df principal:
df = categorizar_cultivos(df)

# Buscar valores nulos:
valores_nulos = df.isna().sum()

# Agrupar por varible categorica y de tiempo:
def agrupar_df(variable):
    dataframe = df.groupby(variable)[["Production", "Area", "Yield"]].agg({
        'Production': 'sum',
        'Area': 'sum',
        'Yield': 'sum'}
    )
    return dataframe.reset_index()

crop = categorizar_cultivos(agrupar_df("Crop"))
state = agrupar_df("State")
year = agrupar_df("Crop_Year")

# Valores Atipicos:
def outliers(variable, data):
    Q1 = data[variable].quantile(0.25)
    Q3 = data[variable].quantile(0.75)
    RIQ = Q3 - Q1
    
    Inf = Q1 - (1.5 * RIQ)
    Sup = Q3 + (1.5 * RIQ)
    
    if Inf < 0: Inf = 0
    outliers = len(data[(data[variable] < Inf) | (data[variable] > Sup)])
    
    return outliers

def porcentaje(n, N):
    porcentaje = (n / N) * 100
    return round(porcentaje, 2)

outliers = {
    "Variable": ["Produccion", "Area", "Rendimiento"],
    "Total de Outliers": [outliers("Production", df), outliers("Area", df), outliers("Yield", df)],
    "Total de Datos": [len(df), len(df), len(df)],
    "Porcentaje": [porcentaje(outliers("Production", df), len(df)), porcentaje(outliers("Area", df), len(df)), porcentaje(outliers("Yield", df), len(df))]
}
    
df_Outliers = pd.DataFrame(outliers)

#print(df_Outliers)

# Datos para el mapa

gdf = gpd.read_file(r"Dataset\india_state.geojson")
gdf.plot()
plt.show()


