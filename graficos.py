import pandas as pd
import geopandas as gpd
import plotly.express as px
import numpy as np

# Leer Data
df = pd.read_csv(r'Dataset/Agricultura_Filtrado.csv')
gdf_final = gpd.read_file(r"Dataset/india_state.geojson")

# Paleta de Colores:
paleta_verde = [
    [0, '#707D7D'],   
    [0.0001, '#000F81'], 
    [0.1, '#032221'],     
    [0.2, '#06302B'],     
    [0.3, '#0B453A'],    
    [0.5, '#03624C'], 
    [0.6, '#17876D'],    
    [0.7, '#2FA98C'],    
    [0.8, '#2CC295'],  
    [0.9, '#00DF81'],  
    [1, '#E3EF26'] 
    ]

# MAPA GEOGRAFICO:
def mapaelcono(df, var):
    fig = px.choropleth(
            df,
            geojson=df["geometry"],
            locations=df.index,
            color=f"{var}_log",
            hover_name="NAME_1",
            hover_data={f"{var}_log": False, var: True},
            color_continuous_scale=paleta_verde
            )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin={"r":0, "t":0, "l":0, "b":0}, 
        title={
            'text': var,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': 'white'}
        },

        coloraxis_colorbar=dict(
            title=var,
            thickness=15,
            len=0.7,
            bgcolor="rgba(0,0,0,0)"
        ),
        coloraxis_cmin=1, 
        coloraxis_cmax=df[f"{var}_log"].max()
    ),
    fig.update_geos(
    visible=False,           # Oculta la base del mapamundi
    showland=False,          # Quita el color de tierra del resto de países
    showocean=False,         # Quita el color del océano
    showlakes=False,         # Desactiva lagos externos
    showcountries=False,     # No dibuja fronteras de otros países
    showcoastlines=False,    # Quita las líneas de costa globales
    fitbounds="locations",   # Hace que la India ocupe todo el cuadro
    bgcolor="rgba(0,0,0,0)"  # Fondo transparente
)
    fig.update_traces(marker_line_color='white', marker_line_width=0.4)

    return fig


# BOXPLOTS:

def boxplot(titulo, var, df):
    fig = px.box(
    df, 
    x="Crop_Type", 
    y=var, 
    color="Crop_Type",
    color_discrete_sequence=px.colors.sequential.Greens[2:],
    points="all",          
    log_y=True,            
    title=titulo,
    labels={
        "Crop_Type": "Tipo de Cultivo",
        var: var
    },
    template="plotly_white" 
    )
    fig.update_traces(pointpos=0, jitter=0.3)
    
    fig.update_layout(
        height=330,
    title_x=0.5,
    showlegend=True
    )
    return fig

# SECTORES:

def sectores(titulo, valores, df):
    
    fig = px.pie(
        df, 
        values=valores, 
        names='Crop_Type', 
        title=titulo,
        color='Crop_Type',
        color_discrete_sequence=px.colors.sequential.Greens[2:],
        template="plotly_white"
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=330, title_x=0.5)
    
    return fig

# BARRAS APILADAS:

def barras(titulo, valores, df):
   
    df_agrupado = df.groupby(['State', 'Crop_Type'])[valores].sum().reset_index()

    fig = px.bar(
        df_agrupado, 
        x='State', 
        y=valores, 
        color='Crop_Type',
        title=titulo,
        log_y=True,
        barmode='stack', 
        color_discrete_sequence=px.colors.sequential.Greens[2:],
        template="plotly_white"
    )

    fig.update_layout(
        title_x=0.5,
        xaxis_title="Estado",
        yaxis_title=f"Total de {valores}",
        legend_title="Tipo de Cultivo",
        xaxis={'categoryorder':'total descending'}
    )

    return fig

