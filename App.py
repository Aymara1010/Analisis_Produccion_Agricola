import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import graficos as gf
import time
import requests


# Configurar Página:
st.set_page_config(
    page_title="Analisis Producción Agricola",
    page_icon="🌱",
    layout="wide"
    )

# Cargar Datos:
@st.cache_data()
def load_geo():
    url = "https://raw.githubusercontent.com/Aymara1010/ayudenme/main/india_state.geojson"
    geo = requests.get(url)
    return geo.json()

@st.cache_data() # Dataset limpiado (ver Limpieza.py)
def load_data():
    df_csv = pd.read_csv("Dataset/Agricultura_Filtrado.csv")
    return df_csv


# Almacenar data en variables:

df = load_data()
gdf = load_geo()

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

resumen_estados = df_filtrado.groupby("State")[[var]].sum().reset_index()

nombres_geo = [f['properties']['NAME_1'] for f in gdf['features']]
df_base = pd.DataFrame({'State': nombres_geo})

df_base['match'] = df_base['State'].astype(str).str.upper().str.strip()
resumen_estados['match'] = resumen_estados['State'].astype(str).str.upper().str.strip()

df_mapa = pd.merge(df_base, resumen_estados.drop(columns=['State']), on="match", how="left").fillna(0)
df_mapa[f"{var}_log"] = np.log10(df_mapa[var] + 1)

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
], on_change="rerun")


if pag1.open:
 with pag1: # Análisis General SIN eliminacion de outliers
     with st.spinner("Preparando el terreno para tu análisis... 📊🚜"):
         time.sleep(10)

     metrica1, metrica2, metrica3, metrica4 = st.columns(4)

    # METRCAS ------------------------------------------
        
     with metrica1:
        with st.container(border=True):
            st.metric(
                "🪴 Producción Total (ton)",
                f"{gf.formato(df_filtrado['Production'].sum())}"
            )

     with metrica2:
        with st.container(border=True):
            st.metric(
                "🌾 Área Cultivas Total (hec)",
                f"{gf.formato(df_filtrado['Area'].sum())}",
            )

     with metrica3:
        with st.container(border=True):
            st.metric(
                "🚜 Rendimiento General (ton/hec)",
                f"{gf.formato(df_filtrado['Yield'].mean())}", # El rendimiento es mejor expresarlo con promedios
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
           fig_mapa = gf.mapa(df_mapa, gdf, var, unid)
           st.plotly_chart(fig_mapa, use_container_width=True)
     
        with st.expander("Ver Analisis Geográfico:"):
         st.markdown("""
                     Según el indicador a evaluar, podemos ver que hay ciertas regiones con mayor concentración
                     de su respectivo indicador, la India es un país de gran tamaño, por lo que sus estados puenden presentar
                     ciertas caracteristicas que permitan que ese indicador cresca o decresca,
                     """)
        
        with st.container(border=True):
            line = gf.linea(f"Evolución Temporal de {var}", var, df_filtrado)
            st.plotly_chart(line, use_container_width=True)  
        
        with st.expander("Ver Analisis Temporal:"):
         st.markdown("""
                     En la India, la agricultura a tenido una evolución constante a nivel general,
                     sin embargo puede tuvo altas y bajas posiblemente a causas climaticas u otros factores 
                     que pudieron afectar alguna de estos indicadores de producción a granescala, a pesar de eso poseen una tendencia positiva en general.
                     """)

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
        
        with st.expander("Ver Analisis Catégorico:"):
         st.markdown("""
                     Podemos agrupar varios cultivos según su especie, al hacer esto podemos observar como se controla un poco
                     la presencia de datos atípicos, esto puede deberse a las carateristicas fisiologias que comparten cada categoria.
                     """)
            
    # -------------------------------------------------------------------------

    # GRAFICO NIVEL 2 ---------------------------------------------------------
    
     with st.container(border=True):
        barras = gf.barras(f"Composición para {var} por Estado y Tipo de Cultivo", var, df_filtrado)
        st.plotly_chart(barras, use_container_width=True)
        
     with st.expander("Ver Tipos de Cultivo por estado:"):
         st.markdown("""
                     Podemos observar que hay una cierta predominancia en algunas categorias. Un país puede
                     dedicarse particularmente en un tipo especifico de cultivo para poder comercializarlo, por lo que tiene a
                     producirse masivamente.
                     """)
    #--------------------------------------------------------------------------
    
    # PAGINA 2 (Analisis de la distribución de Variables numericas) ---------------------------------------------------------------------------
    
if pag2.open:
 with pag2: # Análisis General SIN eliminacion de outliers
     with st.spinner("Sembrando datos y cosechando estadísticas... 🚜🌱"):
         time.sleep(5)
        
     df1 = gf.outliers(var, df_filtrado)

     media, mediana, dt, cv = st.columns(4)

     # METRICAS ---------------------------------------------------------------
     with media:
         with st.container(border=True):
             promedio = df1[var].mean()
             st.metric(
                f"📊 Promedio de {var}",
                f"{gf.formato(promedio)} {unid}"
            )
     with mediana:
        with st.container(border=True):
            st.metric(
                f"📈 Mediana de {var}",
                f"{gf.formato(df1[var].median())} {unid}"
            )
     with dt:
         with st.container(border=True):
             desviacion_tipica = df1[var].std()
             st.metric(
                f"📉 Desviación típica para {var}",
                f"{gf.formato(desviacion_tipica)} {unid}"
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
         
         with st.expander("Ver Analisis de Distribución:"):
          st.markdown("""
                     Podemos Observar una notable asimetria positiva, lo que indica que la mayoria
                     de los cultivos estuvieron entre 0 y 100k, sin embargo lo casos con un gran indicador
                     puede deberse a cultivos que tuvieron unas condiciones externas ideales.
                     """)

         with st.container(border=True):
             top_cultivos1 = gf.top_mejores(f"Top 5 Cultivos con Mayor {var}", var, df1, "Crop")
             st.plotly_chart(top_cultivos1, use_container_width=True)
             
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
             st.markdown("")
             st.markdown("")
             st.markdown("")
             st.markdown("")
             
         with st.container(border=True):
              top_cultivos2 = gf.top_peores(f"Top 5 Cultivos con Menor {var}", var, df1, "Crop")
              st.plotly_chart(top_cultivos2, use_container_width=True)   
        
                 
     with st.expander("Ver Top Cultivos:"):
         st.markdown("""
                     Observar los Cultivos con mejor y menor catidad de un indicador nos permite conocer a fondo
                     a fondo como están conpuestos los extremos de la distribución.
                     """)
  
      # -----------------------------------------------------------------------------------   

      # GRAFICA DE ABAJO ------------------------------------------------------------------        
     with st.container(border=True):
             sector = gf.embudo(titulo=f"Porcentaje de Tipo de Cultivo en {var}", var=var, df=df1)
             st.plotly_chart(sector, use_container_width=True)
        # --------------------------------------------------------------------
        
     with st.expander("Ver Top Cultivos:"):
         st.markdown("""
                     Aquí podemos ver que porcentaje ocupa cata tipo de cultipo en la distribución,
                     podemos ver que siempre hay un cultivo dominante, esto puede deberse a que cierto tipo presenta diversas
                     caracteristicas que disparan este indicador.
                     """)



if pag3.open:
  with pag3: # Análisis General SIN eliminacion de outliers
      with st.spinner("Cargando frutos del análisis... 🍎✨"):
         time.sleep(5)
         
      col51, col52, col53 = st.columns(3)
    
    # METRICAS ---------------------------------------------------------------
      with col51:
        with st.container(border=True):
            ds_produccion = gf.outliers("Production", df_filtrado)
            st.metric(
                f"🌱 Desviación típica para Production (ton)",
                gf.formato(ds_produccion["Production"].std())
            )
      with col52:
        with st.container(border=True):
            ds_area = gf.outliers("Area", df_filtrado)
            st.metric(
                f"🌽 Desviación típica para Area (hec)",
                gf.formato(ds_area["Area"].std())
            )
      with col53:
        with st.container(border=True):
            ds_rendimiento = gf.outliers("Yield", df_filtrado)
            st.metric(
                f"🫚 Desviación típica para Yield (ton/hec)",
                gf.formato(ds_rendimiento["Yield"].std())
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
            
      with st.expander("Ver Relaciones:"):
         st.markdown("""
                     Podemos ver que tanto el área como el rendimiento poseen una relación directa
                     con la producción, sin embargo la relación entre ellas no es muy fuerte.
                     """)
    # ------------------------------------------------------------------------