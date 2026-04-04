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

pag1 , pag2, pag3, pag4 = st.tabs([
    "Producción",
    "Área Cultivada",
    "Rendimiento",
    "🆚 Comparaciones"
])

with pag1:
    
    col1, col2, col3, col4 = st.columns(4)
    
    # METRCAS ------------------------------------------
    with col1:
        with st.container(border=True):
            st.write("""metrica 1
                     (Producción Total)""")
    
    with col2:
        with st.container(border=True):
            st.write("""metrica 2
                     (Media)""")
    
    with col3:
        with st.container(border=True):
            st.write("""metrica 3
                     (CV %)""")
    
    with col4:
        with st.container(border=True):
            st.write("""metrica 4
                     (Top "mejor" Estado)""")
    # -----------------------------------------------------
    
    st.header("Analisis General")
    st.divider()
    
    col5, col6 = st.columns(2)
    
    with col5: # MAPA GEOGRAFICO
        with st.container(border=True):
            st.write("""Grafico de calor
                     (Mapa de la India)""")
    
    with col6: # SECTORES Y DISPERCIÓN
        
        with st.container(border=True):
            st.write("""Grafico boxplot por tipo de cultivo""")
        
        col7, col8 = st.columns(2)
        
        with col7:
            with st.container(border=True):
               st.write("""Grafico de sectores
                        (Para Tipo de Cultivo)""")
               
        with col8:
            with st.container(border=True):
               st.write("Interpretación de resultados (resumen)")
    
    
    with st.container(border=True):
        st.write("gráfico de barras (para estado estado y tipo de cultivo)")  
     
   
    st.header("Analisis de Distribucion")
    st.divider()
    
    col9, col10 = st.columns(2)
     
    with col9:
         with st.container(border=True):
             st.write("Historigrama")
             
         with st.container(border=True):
             st.write("Grafico de Lineas")
     # ----------------------------------------------------------------------------------
     
     # GRAFICAS A LA DERECHA ------------------------------------------------------------
    with col10:
         with st.container(border=True):
             sub1 , sub2 = st.tabs([
             "Regiones",
             "Cultivos"
              ])
             
             with sub1:
                 st.write("Barras de Divergencia para Regiones")
             with sub2:
                 st.write("Barras de Divergencia para Cultivos")
                 
         with st.container(border=True):
             st.write("Analisis de Resultados")        
      # -----------------------------------------------------------------------------------   
      
      # GRAFICA DE ABAJO ------------------------------------------------------------------        
    sub3 , sub4 = st.tabs([
             "Top Regiones",
             "Top Cultivos"
              ])         
     
    with sub3:
         col11, col12 = st.columns(2) 
         
         with col11:
             with st.container(border=True):
                 st.write("Top Mejores Regiones")
         with col12:
             with st.container(border=True):
                 st.write("Top Mejores Regiones")
                 
    with sub4:
         col13, col14 = st.columns(2) 
         with col13:
             with st.container(border=True):
                 st.write("Top Mejores Cultivos")
         with col14:
             with st.container(border=True):
                 st.write("Top Mejores Cultivos")
        # --------------------------------------------------------------------

with pag2:
    col21, col22, col23, col24 = st.columns(4)
    
    with col21:
        with st.container(border=True):
            st.write("""metrica 1
                     (Producción Total)""")
    
    with col22:
        with st.container(border=True):
            st.write("""metrica 2
                     (Media)""")
    
    with col23:
        with st.container(border=True):
            st.write("""metrica 3
                     (CV %)""")
    
    with col24:
        with st.container(border=True):
            st.write("""metrica 4
                     (Top "mejor" Estado)""")
   
    st.header("Análisis General")
    st.divider()
    
    col25, col26 = st.columns(2)
    
    with col25: # MAPA GEOGRAFICO
        with st.container(border=True):
            st.write("""Grafico de calor
                     (Mapa de la India)""")
    
    with col26: # SECTORES Y DISPERCIÓN
        
        with st.container(border=True):
            st.write("""Grafico boxplot por tipo de cultivo""")
        
        col27, col28 = st.columns(2)
        
        with col27:
            with st.container(border=True):
               st.write("""Grafico de sectores
                        (Para Area cultivada)""")
               
        with col28:
            with st.container(border=True):
               st.write("Interpretación de resultados (resumen)")
    # -------------------------------------------------------------------------
    
    # GRAFICO NIVEL 2 ---------------------------------------------------------
    with st.container(border=True):
        st.write("gráfico de barras (para estado estado y tipo de cultivo)")  
    #--------------------------------------------------------------------------
    #DISTRIBUCION
    st.header("Análisis de Distribución")
    st.divider()
    # GRAFICAS A LA IZQUIERDA ---------------------------------------------------------
    col29, col210 = st.columns(2)
     
    with col29:
         with st.container(border=True):
             st.write("Historigrama")
             
         with st.container(border=True):
             st.write("Grafico de Lineas")
     # ----------------------------------------------------------------------------------
     
     # GRAFICAS A LA DERECHA ------------------------------------------------------------
    with col210:
         with st.container(border=True):
             sub5 , sub6 = st.tabs([
             "Regiones",
             "Cultivos"
              ])
             
             with sub5:
                 st.write("Barras de Divergencia para Regiones")
             with sub6:
                 st.write("Barras de Divergencia para Cultivos")
                 
         with st.container(border=True):
             st.write("Analisis de Resultados")        
      # -----------------------------------------------------------------------------------   
      
      # GRAFICA DE ABAJO ------------------------------------------------------------------        
    sub7 , sub8 = st.tabs([
             "Top Regiones",
             "Top Cultivos"
              ])         
     
    with sub7:
         col211, col212 = st.columns(2) 
         
         with col211:
             with st.container(border=True):
                 st.write("Top Mejores Regiones")
         with col212:
             with st.container(border=True):
                 st.write("Top Mejores Regiones")
                 
    with sub8:
         col213, col214 = st.columns(2) 
         with col213:
             with st.container(border=True):
                 st.write("Top Mejores Cultivos")
         with col214:
             with st.container(border=True):
                 st.write("Top Mejores Cultivos")
                 
with pag3:
    col31, col32, col33, col34 = st.columns(4)
    
    # METRCAS ------------------------------------------
    with col31:
        with st.container(border=True):
            st.write("""metrica 1
                     (Producción Total)""")
    
    with col32:
        with st.container(border=True):
            st.write("""metrica 2
                     (Media)""")
    
    with col33:
        with st.container(border=True):
            st.write("""metrica 3
                     (CV %)""")
    
    with col34:
        with st.container(border=True):
            st.write("""metrica 4
                     (Top "mejor" Estado)""")
    # -----------------------------------------------------
    #CATEGORIAS
    st.header("Análisis General")
    st.divider()
    # GRAFICAS NIVEL 1 -------------------------------------
    
    col35, col36 = st.columns(2)
    
    with col35: # MAPA GEOGRAFICO
        with st.container(border=True):
            st.write("""Grafico de calor
                     (Mapa de la India)""")
    
    with col36: # SECTORES Y DISPERCIÓN
        
        with st.container(border=True):
            st.write("""Grafico boxplot por tipo de cultivo""")
        
        col37, col38 = st.columns(2)
        
        with col37:
            with st.container(border=True):
               st.write("""Grafico de sectores
                        (Para Area cultivada)""")
               
        with col38:
            with st.container(border=True):
               st.write("Interpretación de resultados (resumen)")
    # -------------------------------------------------------------------------
    
    # GRAFICO NIVEL 2 ---------------------------------------------------------
    with st.container(border=True):
        st.write("gráfico de barras (para estado estado y tipo de cultivo)")  
    #--------------------------------------------------------------------------
    #DISTRIBUCION
    st.header("Análisis de Distribución")
    st.divider()
    # GRAFICAS A LA IZQUIERDA ---------------------------------------------------------
    col39, col310 = st.columns(2)
     
    with col39:
         with st.container(border=True):
             st.write("Historigrama")
             
         with st.container(border=True):
             st.write("Grafico de Lineas")
     # ----------------------------------------------------------------------------------
     
     # GRAFICAS A LA DERECHA ------------------------------------------------------------
    with col310:
         with st.container(border=True):
             sub9 , sub10 = st.tabs([
             "Regiones",
             "Cultivos"
              ])
             
             with sub9:
                 st.write("Barras de Divergencia para Regiones")
             with sub10:
                 st.write("Barras de Divergencia para Cultivos")
                 
         with st.container(border=True):
             st.write("Analisis de Resultados")        
      # -----------------------------------------------------------------------------------   
      
      # GRAFICA DE ABAJO ------------------------------------------------------------------        
    sub11 , sub12 = st.tabs([
             "Top Regiones",
             "Top Cultivos"
              ])         
     
    with sub11:
         col311, col312 = st.columns(2) 
         
         with col311:
             with st.container(border=True):
                 st.write("Top Mejores Regiones")
         with col312:
             with st.container(border=True):
                 st.write("Top Mejores Regiones")
                 
    with sub12:
         col313, col314 = st.columns(2) 
         with col313:
             with st.container(border=True):
                 st.write("Top Mejores Cultivos")
         with col314:
             with st.container(border=True):
                 st.write("Top Mejores Cultivos")

with pag4:
    col41, col42, col43 = st.columns(3)
    
    # METRICAS ---------------------------------------------------------------
    with col41:
        with st.container(border=True):
            st.write("Desviación Tipica para produccion")
    with col42:
        with st.container(border=True):
            st.write("Desviación Tipica para Area")
    with col43:
        with st.container(border=True):
            st.write("Desviación Tipica para Rendimiento")  
    # ------------------------------------------------------------------------
    
    col44, col45 = st.columns(2)
    
    # GRAFICOS A LA IZQUIERDA ------------------------------------------------
    with col44:
        
        with st.container(border=True):
            st.write("Matriz de Correlación")
            
        with st.container(border=True):
            st.write("Grafico de Lineas")
    # ------------------------------------------------------------------------
    
    # GRAFICOS A LA DERECHA --------------------------------------------------
    with col45:
        
        with st.container(border=True):
            st.write("Grafico de Disperción")
        
        with st.container(border=True):
            st.write("Analisis de resultados")
    # ------------------------------------------------------------------------
    