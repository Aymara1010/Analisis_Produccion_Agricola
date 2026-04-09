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

@st.cache_data() # Datos geograficos
def load_geojson():
    geo =  gpd.read_file("Dataset/india_state.geojson")
    return geo

@st.cache_data() # Dataset limpiado (ver Limpieza.py)
def load_data():
    df_csv = pd.read_csv("Dataset/Agricultura_Filtrado.csv")
    return df_csv

# Almacenar data en variables:

gdf = load_geojson()
df = load_data()

# Titulo de la Página:
st.title("🌱 Análisis de la Producción Agricola en la India (1997-2009)")
st.markdown("¡Bienvenido a nuestro Dashboard! 🎍🎍")
st.markdown("En este panel interactivo analizarás la evolución de la productividad agrícola en la India durante el periodo 1997-2009. A través de esta interfaz, explorarás la relación entre el área destinada al cultivo y el volumen de producción final, identificando los cultivos y regiones con mayor eficiencia productiva")

# FILTROS --------------------------------------------------------------------------------------------------------

with st.sidebar:
    # TITULO
    st.title("🌱 Análisis Producción Agricola en la India (1997-2009)")
    st.header("🔎 Filtros de Búsqueda")
    
    # VARIABLE
    with st.container(border=True):
        var = st.selectbox(
        "📌 Selecciona una Variable",
        options=["Production", "Area", "Yield"]
    )
    # AÑO DE CULTIVO:
    with st.container(border=True): # Barra con dos puntos para formar un intevalo de tiempo
        anio = st.slider(
        "🕐 Seleccionar Años de Cultivo",
        min_value=1997,
        max_value=2009,
        value=(1997,2009)
    )
    # ESTADOS
    with st.container(border=True):
        cultivo = st.multiselect(
            "🌾 Seleccionar Tipos de Cultivos:",
            options=df["Crop_Type"].unique(),
            default=df["Crop_Type"].unique()
            )
        
    # CULTIVOS
    with st.container(border=True):
        estado = st.multiselect(
        "🗾 Selecciona un Estado",
        options=df["State"].unique(),
        default=df["State"].unique()
    )
        
    # TRABAJO FINAL
    st.divider()
    st.markdown("""🌿 Trabajo Final | Computación I 🌿""")
    st.markdown("""🌻 Creado por: 🌻 Asly Caputo y Aymara Andersen """)
    
# APLICAR FILTROS: 
df_filtrado = df[(df["Crop_Year"] >= anio[0]) & (df["Crop_Year"] <= anio[1]) & (df["Crop_Type"].isin(cultivo)) & (df["State"].isin(estado))]

# agrupar df por estado segun la variable seleccionada
estados_agrupados = df_filtrado.groupby("State")[[var]].sum().reset_index()

# Concatenar con datos geometricos
gdf_filtrado = gdf.merge(estados_agrupados, left_on='NAME_1', right_on="State", how='left').drop(columns="State")

# Sacar log y llenar Na para el mapa
gdf_filtrado[f"{var}_log"] = np.log10(gdf_filtrado[var])
gdf_filtrado[f"{var}_log"] = gdf_filtrado[f"{var}_log"].fillna(-666)

# UNIDAD DE MEDIDA:

if var == "Production":
    unid = "ton"
elif var == "Area":
    unid = "hec"
else:
    unid = "ton/hec"
 
# ----------------------------------------------------------------------------------------------------------------

# Mostrar Dataset Original



# Separación de Páginas Principales:

pag1 , pag2, pag3 = st.tabs([
    "🌏 Análisis General",
    "📈 Distribución",
    "🆚 Comparaciones"
])

with pag1: # Análisis General SIN eliminacion de outliers

    metrica1, metrica2, metrica3, metrica4 = st.columns(4)

    # METRCAS ------------------------------------------
    
    def formato(num): # Cambiar de formato números muy grandes
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.2f} Billones" # NOTA: los "_" no afectan el calculo, solo es para llevar un orden visual
        elif num >= 1_000_000:
            return f"{num/1_000_000:.2f} Millones"
        elif num >= 100_000:
            return f"{num/1_000:.2f} Miles"
        else: return f"{num:,.2f}"
        
    with metrica1:
        with st.container(border=True):
            st.metric(
                "🪴 Producción Total (ton)",
                f"{formato(df_filtrado["Production"].sum())}"
            )

    with metrica2:
        with st.container(border=True):
            st.metric(
                "🌾 Área Cultivas Total (hec)",
                f"{formato(df_filtrado["Area"].sum())}",
            )

    with metrica3:
        with st.container(border=True):
            st.metric(
                "🚜 Rendimiento General (ton/hec)",
                f"{formato(df_filtrado["Yield"].mean())}", # El rendimiento es mejor expresarlo con promedios
            )

    with metrica4:
        with st.container(border=True):
            cultivos_agrupados = df_filtrado.groupby("Crop")[var].sum()
            st.metric(
                f"🌽 Cultivo con Mayor {var}",
                str(cultivos_agrupados.idxmax()),
            )
    # -----------------------------------------------------

    # GRAFICAS NIVEL 1 -------------------------------------

    mapa, graficas = st.columns(2)

    with mapa: # MAPA GEOGRAFICO
        with st.container(border=True):
           fig = gf.mapa(gdf_filtrado, var, unid)
           st.plotly_chart(fig, use_container_width=True)
        
        with st.container(border=True):
            line = gf.linea(f"Evolución Temporal de {var}", var, df_filtrado)
            st.plotly_chart(line, use_container_width=True)  

    with graficas:# SECTORES Y DISPERCIÓN
        
        with st.container(border=True):
            st.header("📊 Análisis General")
            st.markdown(f"""
                        En esta sección podemos observar como se distribuye la variable {var} de manera geográfica, temporal y clasificatoria a traves de los siguientes gráficos:
                        * El mapa coroplético identifica la intensidad de {var} a nivel geográfico.
                        * El gráfico de distribución (Boxplot) permite comparar la variabilidad y el rendimiento entre las distintas categorías de cultivos. 
                        * El gráfico de líneas traza la evolución temporal de {var}.
                        * El gráfico de barrar apiladas nos deja observar a fondo la proporción que ocupan cada tipo de cultivo en cada estado seleccionado.
                        """)
            st.markdown("**IMPORTANTE:** para esta sección no se eliminó ningún dato atípico.")

        with st.container(border=True):
            box = gf.boxplot(f"Variabilidad de {var} por Categoría de Cultivo", var, df_filtrado)
            st.plotly_chart(box, use_container_width=True)  
            
    # -------------------------------------------------------------------------

    # GRAFICO NIVEL 2 ---------------------------------------------------------
    with st.container(border=True):
        barras = gf.barras(f"Composición para {var} por Estado y Tipo de Cultivo", var, df_filtrado)
        st.plotly_chart(barras, use_container_width=True)
    #--------------------------------------------------------------------------
    
    # PAGINA 2 (Analisis de la distribución de Variables numericas) ---------------------------------------------------------------------------
    
    with pag2:
        
     df1 = gf.outliers(var, df_filtrado)

     media, mediana, dt, cv = st.columns(4)

     # METRICAS ---------------------------------------------------------------
     with media:
         with st.container(border=True):
             promedio = df1[var].mean()
             st.metric(
                f"📊 Promedio de {var}",
                f"{formato(promedio)} {unid}"
            )
     with mediana:
        with st.container(border=True):
            st.metric(
                f"📈 Mediana de {var}",
                f"{formato(df1[var].median())} {unid}"
            )
     with dt:
         with st.container(border=True):
             desviacion_tipica = df1[var].std()
             st.metric(
                f"📉 Desviación típica para {var}",
                f"{formato(desviacion_tipica)} {unid}"
            )
     with cv:
        with st.container(border=True):
            st.metric(
                f"📍 Outliers eliminados en {var}",
                f"{gf.len_outliers(var, df_filtrado)} registros"
            )
     # ---------------------------------------------------------------------------------

     # GRAFICAS A LA IZQUIERDA ---------------------------------------------------------
     col41, col42 = st.columns(2)

     with col41:
         with st.container(border=True):
             hist = gf.histograma(f"Hitorigrama para {var}", var, df1)
             st.plotly_chart(hist, use_container_width=True)

         with st.container(border=True):
             
             sector = gf.sectores(f"Porcentaje de Tipo de Cultivo en {var}", var, df1)
             st.plotly_chart(sector, use_container_width=True)
     # ----------------------------------------------------------------------------------

     # GRAFICAS A LA DERECHA ------------------------------------------------------------
     with col42:
         
         with st.container(border=True):
             st.header("📌 Analisis de Distribución")
             st.markdown(f"""
                         En esta sección observaremos la distribución y la dispersión individual de cada una de las variables para conocer un poco de su comportamiento:
                         * El historigrama de nos permite visualizar la distribución general de {var}.
                         * El gráfico de barras horizontales nos permite clasificar los mejores y peores cultivos en {var}.
                         * El gráfico de sectores nos permite ver la proporción que ocupa cada tipo de cultivo en la variable {var}.
                         * El gráfico de barra divergente nos permite analizar la desviación de la media de {var} de cada estado con respecto a su media poblacional.
                         """)
             st.markdown("**IMPORTANTE:** para analizar correctamente la distribución de la variable en general, lo mejor es eliminar los datos atipicos.")
            
         with st.container(border=True):
             sub11 , sub12 = st.tabs([
             "Top Mejores",
             "Top Peores"
              ])

             with sub11:
                 top_cultivos1 = gf.top_mejores(f"Top 5 Cultivos con Mayor {var}", var, df1, "Crop")
                 st.plotly_chart(top_cultivos1, use_container_width=True)
             with sub12:
                 top_cultivos2 = gf.top_peores(f"Top 5 Cultivos con Menor {var}", var, df1, "Crop")
                 st.plotly_chart(top_cultivos2, use_container_width=True)

  
      # -----------------------------------------------------------------------------------   

      # GRAFICA DE ABAJO ------------------------------------------------------------------        

        # --------------------------------------------------------------------




with pag3:
    col51, col52, col53 = st.columns(3)
    
    # METRICAS ---------------------------------------------------------------
    with col51:
        with st.container(border=True):
            ds_produccion = gf.outliers("Production", df_filtrado)
            st.metric(
                f"🌱 Desviación típica para Production (ton)",
                formato(ds_produccion["Production"].std())
            )
    with col52:
        with st.container(border=True):
            ds_area = gf.outliers("Area", df_filtrado)
            st.metric(
                f"🌽 Desviación típica para Area (hec)",
                formato(ds_area["Area"].std())
            )
    with col53:
        with st.container(border=True):
            ds_rendimiento = gf.outliers("Yield", df_filtrado)
            st.metric(
                f"🫚 Desviación típica para Yield (ton/hec)",
                formato(ds_rendimiento["Yield"].std())
            )
    # ------------------------------------------------------------------------
    
    col61, col62 = st.columns(2)
    
    # GRAFICOS A LA IZQUIERDA ------------------------------------------------
    with col61:

        with st.container(border=True):
             st.header("📈 Analisis Comparativo")
             st.markdown("""
                         En esta sección se analizará la relación entre las varibles relacionas a la producción del sector agrícola, permitiendo entender no solo cuánto se produce, sino qué tipo de relación tienen a través de los siguientes gráficos:
                         * La matriz de correlación nos permite observar la relacion lineal entre cada una de las varibles, lo que permite identificar su tipo y magnitud de relación.
                         * El gráfico de disperción nos permite analizar que tan dispersos y relacionados estan los datos entre si.
                         * El gráfico de linea permite comparar la evolución temporal de cada una de las variables.
                         """)
             st.markdown("""**IMPORTANTE:** Para visualizar mejor las relaciones se opto por utilizar la escala logaritmica""")
             
        
        with st.container(border=True):
            matriz = gf.matriz(df_filtrado)
            st.plotly_chart(matriz, use_container_width=True)
            
            
                         
    # ------------------------------------------------------------------------
    
    # GRAFICOS A LA DERECHA --------------------------------------------------
    with col62:   
               
        with st.container(border=True):
            linea2 = gf.linea_comparacion(df_filtrado)
            st.plotly_chart(linea2, use_container_width=True)
        
        with st.container(border=True):
            comparacion = st.selectbox(
                " ",
            options=["Production vs Area", "Area vs Yield", "Yield vs Production"]
            )
            
            if comparacion == "Production vs Area":
              var1 = "Production"
              var2 = "Area"
            elif comparacion ==  "Yield vs Production":  
             var1 = "Production"
             var2 = "Yield"
            else:
              var1 = "Yield"
              var2 = "Area"
            
            dispecion = gf.dispercion(f"Gráfico de Disperción de {comparacion} por Tipo de Cultivo",var1, var2, df_filtrado)
            st.plotly_chart(dispecion, use_container_width=True)
    # ------------------------------------------------------------------------