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
    
    # Opciones de Visualización
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
    )
    
    # Opciones geográficas
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
    # Opciones de bordes
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
    fig.update_layout(height=400, title_x=0.5)
    
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

# HISTORIGRAMA:

def histograma(titulo, var, df):
    fig = px.histogram(
        
        df, 
        x=var,
        title=titulo,
        color_discrete_sequence=px.colors.sequential.Greens[2:], 
        template="plotly_dark"
    )
    fig.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=var, 
        yaxis_title="Frecuencia",
        bargap=0.1,
        height=500
    )
    
    return fig

# LINEA:
def linea(titulo, var, df):
    df_agrupado = df.groupby("Crop_Year")[var].sum().reset_index()
    
    fig = px.line(
    df_agrupado, 
    x="Crop_Year", 
    y=var,
    title=titulo,
    markers=True, 
    template="plotly_dark"
    )
    
    fig.update_layout(
    title_x=0.5, 
    xaxis_title="Año de Cosecha",
    yaxis_title=var,
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', dtick=1), 
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', tickformat=',.0f'), 
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_traces(
    line_color='#00ff88', 
    line_width=3,
    marker=dict(size=8, color='white', symbol='circle'),
    fill='tozeroy', 
    fillcolor='rgba(0, 255, 136, 0.1)'
    )
    
    return fig

# BARRAS MARIPOSA:
def bar_mariposa(titulo, var, df):
    
    #preparar data:
    media_general = df['Production'].mean()
    
    df_agrupado = df.groupby("State")["Production"].mean().reset_index()
    df_agrupado['Desviacion_Media'] = df_agrupado['Production'] - media_general
    df_agrupado['Estado_Comparacion'] = df_agrupado['Desviacion_Media'].apply(lambda x: 'Sobre la Media' if x >= 0 else 'Bajo la Media')
    
    df_agrupado = df_agrupado.sort_values(by='Desviacion_Media', ascending=True)
    
    # gráfico:
    fig = px.bar(
    df_agrupado,
    x='Desviacion_Media',
    y='State',            
    orientation='h', 
    color='Estado_Comparacion', 
    color_discrete_map={
        'Sobre la Media': '#1a9641', 
        'Bajo la Media': '#d7191c'    
    },
    title="Diferencia de Producción Media por Estado Respecto a la Media General",
    labels={
        'Desviacion_Media': 'Desviación de Producción',
        'State': 'Estado',
        'Estado_Comparacion': 'Estado Comparación'
    },
    template="plotly_dark"
    )


    fig.add_vline(x=0, line_width=3, line_dash="solid", line_color="white")

    fig.update_layout(
    title_x=0.5, 
    xaxis_tickformat=',.0f',
    yaxis_title=None, 
    bargap=0.3,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
  
    margin=dict(l=150, r=20, t=50, b=80),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)' 
    )

    fig.update_traces(
    hovertemplate="<b>%{y}</b><br>Desviación: %{x:,.0f}<br>Comparación: %{text}",
    text=df_agrupado['Estado_Comparacion'] 
    )
    
    return fig


# TOP:

def top_mejores(Titulo, var, df, tipo):
    top = df.groupby(tipo)[var].sum().reset_index()
    top = top.sort_values(by=var, ascending=True).tail(5)
    
    fig = px.bar(
    top,
    y=tipo,
    x=var,
    text_auto='.2s',
    title=Titulo,
    color=var,
    color_continuous_scale=px.colors.sequential.Greens,
    template="plotly_dark"
    )
    
    fig.update_traces(
    marker_line_color='rgb(255,255,255)',
    marker_line_width=1.5,
    opacity=0.8
    )
    
    fig.update_layout(
    title_x=0.5,
    xaxis_title=tipo,
    yaxis_title=f"{var} Total",
    coloraxis_showscale=False, 
    bargap=0.4
    )
    
    return fig

def top_peores(Titulo, var, df, tipo):
    top = df.groupby(tipo)[var].sum().reset_index()
    top = top.sort_values(by=var, ascending=True).head(5)
    
    fig = px.bar(
    top,
    y=tipo,
    x=var,
    text_auto='.2s',
    title=Titulo,
    color=var,
    color_continuous_scale=px.colors.sequential.Greens,
    template="plotly_dark"
    )
    
    fig.update_traces(
    marker_line_color='rgb(255,255,255)',
    marker_line_width=1.5,
    opacity=0.8
    )
    
    fig.update_layout(
    title_x=0.5,
    xaxis_title="Tipo de Cultivo",
    yaxis_title=f"{var} Total",
    coloraxis_showscale=False, 
    bargap=0.4
    )
    
    return fig

# data sin ouliers:
def outliers(variable, data):
    Q1 = data[variable].quantile(0.25)
    Q3 = data[variable].quantile(0.75)
    RIQ = Q3 - Q1
    
    Inf = Q1 - (1.5 * RIQ)
    Sup = Q3 + (1.5 * RIQ)
    
    if Inf < 0: Inf = 0
    atipicos = data[(data[variable] < Inf) | (data[variable] > Sup)]
    df = data.drop(atipicos.index)
    
    return df
 
def len_outliers(variable, data):
    Q1 = data[variable].quantile(0.25)
    Q3 = data[variable].quantile(0.75)
    RIQ = Q3 - Q1
    
    Inf = Q1 - (1.5 * RIQ)
    Sup = Q3 + (1.5 * RIQ)
    
    if Inf < 0: Inf = 0
    atipicos = data[(data[variable] < Inf) | (data[variable] > Sup)]
    
    return len(atipicos)

# Matriz de Correlacion
def matriz(df):
    columnas = ['Production', 'Yield', 'Area']
    df[columnas] = np.log1p(df[columnas])
    matriz_corr = df[columnas].corr()
    
    fig = px.imshow(
    matriz_corr,
    text_auto='.2f',
    aspect="auto",
    color_continuous_scale='RdYlGn',
    title="Matriz de Correlación: Producción, Rendimiento y Área",
    template="plotly_dark",
    labels=dict(color="Correlación")
     )
    
    fig.update_layout(
    title_x=0.5,
    width=600,
    height=600
    )
    
    return fig  
    
# Comparacion de tiempo:
def linea_comparacion(df):
    df_tendencia = df.groupby('Crop_Year')[['Production', 'Area', 'Yield']].sum().reset_index()
    
    fig = px.line(df_tendencia, 
              x='Crop_Year', 
              y=['Production', 'Area', 'Yield'],
              title='Tendencia Histórica: Producción, Área y Rendimiento',
              template='plotly_dark',
              labels={'value': 'Unidades', 'Crop_Year': 'Año', 'variable': 'Métrica'})

    fig.update_layout(
    title_x=0.5, 
    xaxis_title="Año de Cosecha",
    yaxis_title="ton, hec y ton/hec",
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', dtick=1), 
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', tickformat=',.0f'), 
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=400
    )
    
    fig.update_traces(
    line_color='#00ff88', 
    line_width=3,
    marker=dict(size=8, color='white', symbol='circle'),
    fill='tozeroy', 
    fillcolor='rgba(0, 255, 136, 0.1)'
    )

    fig.update_layout(legend_orientation="h", legend_y=1.1)
    return fig

# Dispercion
def dispercion(titulo, var1, var2,var3, df):
    fig = px.scatter(
    df, 
    x=var1, 
    y=var2, 
    color="Crop", 
    size=var3,
    hover_name="Crop",       
    hover_data=["State", "Crop_Year"],
    log_x=True,           
    log_y=True, 
    title=titulo,
    template="plotly_dark",
    color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
    title_x=0.5,
    xaxis_title=var1,
    yaxis_title=var2,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_traces(marker=dict(size=8, opacity=0.6, line=dict(width=0.5, color='white')))
    
    return fig


    



