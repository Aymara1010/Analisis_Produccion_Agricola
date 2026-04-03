import pandas as pd
import plotly.express as px
import streamlit as st

# Configurar Página:
st.set_page_config(
    page_title="Analisis Producción Agricola",
    page_icon="🌱",
    layout="wide"
    )

# Cargar Datos:
@st.cache_data
def cargar_df():
    df = pd.read_csv(r"Dataset/Agricultura.csv")
    return df

df = cargar_df()

# Titulo de la Página:
st.title("Análisis Producción Agricola en la India (1997-2009)")
st.markdown("Análisis Descriptivo de la Productividad Agrícola en Distintas Regiones de la India Durante el Periodo 1997-2009")

# FILTROS --------------------------------------------------------------------------------------------------------

with st.sidebar:
    # TITULO
    st.title("🌱 Análisis Producción Agricola en la India (1997-2009)")
    st.divider()
    st.header("Filtros de Búsqueda")
    
    # REGIONES
    with st.container(border=True):
        st.write("filtros de región (multiselect)")
    # CULTIVOS
    with st.container(border=True):
        st.write("filtros de Cultivo (multiselect)")
    # TIEMPO
    with st.container(border=True):
        st.write("filtros de Fecha (slidebar)")
    # VARIABLE NUMERICA
    with st.container(border=True):
        st.write("selección de variable (select)")
        
    # TRABAJO FINAL
    st.divider()
    st.markdown("""Trabajo Final Computación I """)
    st.markdown("""Creado por: Asly Caputo y Aymara Andersen """)
# ----------------------------------------------------------------------------------------------------------------

with st.expander("Agricultura.csv"):
    st.dataframe(df.head(5), use_container_width=True)

# Separación de Páginas Principales:

pag1 , pag2, pag3 = st.tabs([
    "🌏 Análisis General",
    "📈 Distribución",
    "🆚 Comparaciones"
])

# PAGINA 1: (Analisis de Variables Cátegoricas)  -----------------------------------------------------------------------------------------

with pag1:

    col11, col12, col13, col14 = st.columns(4)
    
    # METRCAS ------------------------------------------
    with col11:
        with st.container(border=True):
            st.write("""metrica 1
                     (Producción Total)""")
    
    with col12:
        with st.container(border=True):
            st.write("""metrica 2
                     (Area Cultivada Total)""")
    
    with col13:
        with st.container(border=True):
            st.write("""metrica 3
                     (Rendimiento Total)""")
    
    with col14:
        with st.container(border=True):
            st.write("""metrica 4
                     (Top "mejor" Estado)""")
    # -----------------------------------------------------
    
    # GRAFICAS NIVEL 1 -------------------------------------
    
    col21, col22 = st.columns(2)
    
    with col21: # MAPA GEOGRAFICO
        with st.container(border=True):
            st.write("""Grafico de calor
                     (Mapa de la India)""")
    
    with col22: # SECTORES Y DISPERCIÓN
        
        with st.container(border=True):
            st.write("""Grafico boxplot por tipo de cultivo""")
        
        col221, col222 = st.columns(2)
        
        with col221:
            with st.container(border=True):
               st.write("""Grafico de sectores
                        (Para Area cultivada)""")
               
        with col222:
            with st.container(border=True):
               st.write("Interpretación de resultados (resumen)")
    # -------------------------------------------------------------------------
    
    # GRAFICO NIVEL 2 ---------------------------------------------------------
    with st.container(border=True):
        st.write("gráfico de barras (para estado estado y tipo de cultivo)")  
    #--------------------------------------------------------------------------

# PAGINA 2 (Analisis de la distribución de Variables numericas) ---------------------------------------------------------------------------

with pag2:
    
     col31, col32, col33, col34 = st.columns(4)
     
     # METRICAS ---------------------------------------------------------------
     with col31:
         with st.container(border=True):
             st.write("Media")
     with col32:
        with st.container(border=True):
            st.write("Mediana")
     with col33:
         with st.container(border=True):
             st.write("Moda")
     with col34:
        with st.container(border=True):
            st.write("CV %")
     # ---------------------------------------------------------------------------------
     
     # GRAFICAS A LA IZQUIERDA ---------------------------------------------------------
     col41, col42 = st.columns(2)
     
     with col41:
         with st.container(border=True):
             st.write("Historigrama")
             
         with st.container(border=True):
             st.write("Grafico de Lineas")
     # ----------------------------------------------------------------------------------
     
     # GRAFICAS A LA DERECHA ------------------------------------------------------------
     with col42:
         with st.container(border=True):
             sub11 , sub12 = st.tabs([
             "Regiones",
             "Cultivos"
              ])
             
             with sub11:
                 st.write("Barras de Divergencia para Regiones")
             with sub12:
                 st.write("Barras de Divergencia para Cultivos")
                 
         with st.container(border=True):
             st.write("Analisis de Resultados")        
      # -----------------------------------------------------------------------------------   
      
      # GRAFICA DE ABAJO ------------------------------------------------------------------        
     sub21 , sub22 = st.tabs([
             "Top Regiones",
             "Top Cultivos"
              ])         
     
     with sub21:
         col421, col422 = st.columns(2) 
         
         with col421:
             with st.container(border=True):
                 st.write("Top Mejores Regiones")
         with col422:
             with st.container(border=True):
                 st.write("Top Mejores Regiones")
                 
     with sub22:
         col423, col424 = st.columns(2) 
         with col423:
             with st.container(border=True):
                 st.write("Top Mejores Cultivos")
         with col424:
             with st.container(border=True):
                 st.write("Top Mejores Cultivos")
        # --------------------------------------------------------------------
        
# PAGINA 3: (Comparaciones) --------------------------------------------------------------------------------------------------------------------            
         
with pag3:
    col51, col52, col53 = st.columns(3)
    
    # METRICAS ---------------------------------------------------------------
    with col51:
        with st.container(border=True):
            st.write("Desviación Tipica para produccion")
    with col52:
        with st.container(border=True):
            st.write("Desviación Tipica para Area")
    with col53:
        with st.container(border=True):
            st.write("Desviación Tipica para Rendimiento")  
    # ------------------------------------------------------------------------
    
    col61, col62 = st.columns(2)
    
    # GRAFICOS A LA IZQUIERDA ------------------------------------------------
    with col61:
        
        with st.container(border=True):
            st.write("Matriz de Correlación")
            
        with st.container(border=True):
            st.write("Grafico de Lineas")
    # ------------------------------------------------------------------------
    
    # GRAFICOS A LA DERECHA --------------------------------------------------
    with col62:
        
        with st.container(border=True):
            st.write("Grafico de Disperción")
        
        with st.container(border=True):
            st.write("Analisis de resultados")
    # ------------------------------------------------------------------------
                


         
         

             
             
             
         
     
        
        
    
    


