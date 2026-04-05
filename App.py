import pandas as pd
import numpy as np
import streamlit as st
import geopandas as gpd
import plotly.express as px
import graficos as gf


# Configurar Página:
st.set_page_config(
    page_title="Analisis Producción Agricola",
    page_icon="🌱",
    layout="wide"
    )

# Cargar Datos:
@st.cache_data()
def load_original():
    df_original = pd.read_csv("Dataset/Agricultura.csv")
    return df_original

@st.cache_data()
def load_geojson():
    geo =  gpd.read_file("Dataset/india_state.geojson")
    return geo

@st.cache_data()
def load_data():
    df_csv = pd.read_csv("Dataset/Agricultura_Filtrado.csv")
    return df_csv

df_original = load_original()
gdf = load_geojson()
df = load_data()

# Titulo de la Página:
st.title("Análisis Producción Agricola en la India (1997-2009)")
st.markdown("Análisis Descriptivo de la Productividad Agrícola en Distintas Regiones de la India Durante el Periodo 1997-2009")

# FILTROS --------------------------------------------------------------------------------------------------------

with st.sidebar:
    # TITULO
    st.title("🌱 Análisis Producción Agricola en la India (1997-2009)")
    st.divider()
    st.header("Filtros de Búsqueda")
    
    # VARIABLE
    with st.container(border=True):
        var = st.selectbox(
        "Selecciona una Variable",
        options=["Production", "Area", "Yield"]
    )
    # AÑO DE CULTIVO:
    with st.container(border=True):
        anio = st.slider(
        "Seleccionar Años de Cultivo",
        min_value=1997,
        max_value=2009,
        value=(1997,2009)
    )
    # ESTADOS
    with st.container(border=True):
        cultivo = st.multiselect(
            "Seleccionar Tipos de Cultivos:",
            options=df["Crop_Type"].unique(),
            default=df["Crop_Type"].unique()
            )
        
    # CULTIVOS
    with st.container(border=True):
        estado = st.multiselect(
        "Selecciona un Estado",
        options=df["State"].unique(),
        default=df["State"].unique()
    )
        
    # TRABAJO FINAL
    st.divider()
    st.markdown("""Trabajo Final Computación I """)
    st.markdown("""Creado por: Asly Caputo y Aymara Andersen """)
    
# APLICAR FILTROS: 
df_filtrado = df[(df["Crop_Year"] >= anio[0]) & (df["Crop_Year"] <= anio[1]) & (df["Crop_Type"].isin(cultivo)) & (df["State"].isin(estado))]

# agrupar df por estado segun la variable seleccionada
estados_agrupados = df_filtrado.groupby("State")[[var]].sum().reset_index()

# Concatenar con datos geometricos
gdf_filtrado = gdf.merge(estados_agrupados, left_on='NAME_1', right_on="State", how='left').drop(columns="State")

# Sacar log y llenar Na para el mapa
gdf_filtrado[f"{var}_log"] = np.log10(gdf_filtrado[var])
gdf_filtrado[f"{var}_log"] = gdf_filtrado[f"{var}_log"].fillna(-666)
 
# ----------------------------------------------------------------------------------------------------------------

with st.expander("Agricultura.csv"):
    st.dataframe(df_original)

# Separación de Páginas Principales:

pag1 , pag2, pag3 = st.tabs([
    "🌏 Análisis General",
    "📈 Distribución",
    "🆚 Comparaciones"
])

with pag1:

    metrica1, metrica2, metrica3, metrica4 = st.columns(4)

    # METRCAS ------------------------------------------
    
    def formato(num):
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.2f} Billones"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.2f} Millones"
        elif num >= 100_000:
            return f"{num/1_000:.2f} K"
        else: return f"{num:,.0f}"
        
    with metrica1:
        with st.container(border=True):
            st.metric(
                "Producción Total (ton)",
                f"{formato(df_filtrado["Production"].sum())}"
            )

    with metrica2:
        with st.container(border=True):
            st.metric(
                "Área Cultivas Total (hec)",
                f"{formato(df_filtrado["Area"].sum())}",
            )

    with metrica3:
        with st.container(border=True):
            st.metric(
                "Rendimiento General (ton/hec)",
                f"{formato(df_filtrado["Yield"].sum())}",
            )

    with metrica4:
        with st.container(border=True):
            cultivos_agrupados = df_filtrado.groupby("Crop")[var].sum()
            st.metric(
                f"Cultivo con Mayor {var}",
                str(cultivos_agrupados.idxmax()),
            )
    # -----------------------------------------------------

    # GRAFICAS NIVEL 1 -------------------------------------

    mapa, graficas = st.columns(2)

    with mapa: # MAPA GEOGRAFICO
        with st.container(border=True):
           fig = gf.mapaelcono(gdf_filtrado, var)
           st.plotly_chart(fig, use_container_width=True)
            
        with st.container(border=True):
            st.markdown("""La agricultura ha sido un sector económico de la India que ha ido evolucionando a través del tiempo, siendo actualmente uno de los países con mayor producción agrícola a nivel global, lo que lo hace uno de los sectores económicos más relevantes del país. Sin embargo, la agricultura también es un sector con una alta variabilidad cuando hablamos de rendimiento, dependiendo de factores como el tipo de cultivo sembrado y la zona geográfica en la que se encuentra, por lo que obtener una alta producción requiere de un análisis exhaustivo para obtener los mejores resultados.""")

    with graficas: # SECTORES Y DISPERCIÓN

        with st.container(border=True):
            box = gf.boxplot("Titulo", var, df_filtrado)
            st.plotly_chart(box, use_container_width=True)

        with st.container(border=True):
            sector = gf.sectores("Titulo", var, df_filtrado)
            st.plotly_chart(sector, use_container_width=True)
            
    # -------------------------------------------------------------------------

    # GRAFICO NIVEL 2 ---------------------------------------------------------
    with st.container(border=True):
        barras = gf.barras("Titulo", var, df_filtrado)
        st.plotly_chart(barras, use_container_width=True)
    #--------------------------------------------------------------------------