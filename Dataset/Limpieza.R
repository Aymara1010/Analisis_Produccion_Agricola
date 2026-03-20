library("tidyverse")
options(scipen = 999)
# Leer Archivo

agricultura <- read.csv("Agricultura.csv")
glimpse(agricultura)


# Filtrar variables y registros necesarios

df <- agricultura %>% 
  filter( Season == "Whole Year ", Crop_Year < 2010 ) %>% 
  select(Crop_Year, State, Crop, Production, Area, Yield)

# Recategorizar variables cultivo:

# Categorias
cultivos <- list(
  tipo1 = c("Rice", "Wheat", "Maize", "Barley", "Jowar", "Bajra", "Ragi", "Small millets", "Tapioca", "Sannhamp"),
  tipo2 = c("Arhar/Tur", "Gram", "Horse-gram", "Moong(Green Gram)", "Urad", "Cowpea(Lobia)", "Moth", "Khesari", "Masoor", "Peas & beans (Pulses)"),
  tipo3 = c("Groundnut", "Sesamum", "Sunflower", "Soyabean", "Rapeseed &Mustard", "Castor seed", "Linseed", "Safflower", "Niger seed", "other oilseeds", "Oilseeds total"),
  tipo4 = c("Dry chillies", "Turmeric", "Cardamom", "Coriander", "Garlic", "Ginger", "Black pepper", "Onion", "Potato", "Sweet potato"),
  tipo5 = c("Coconut ", "Arecanut", "Cashewnut", "Banana", "Sugarcane", "Cotton(lint)", "Mesta", "Tobacco", "Guar seed"))

# Función para categorizar
clasificar_cultivo <- function (dataframe, lista = cultivos) { 
  nueva_columna <- dataframe %>% 
    mutate( Type_Crop = case_when(
      Crop %in% cultivos$tipo1 ~ "Cereales y Granos",
      Crop %in% cultivos$tipo2 ~ "Leguminosas ",
      Crop %in% cultivos$tipo3 ~ "Oleaginosas",
      Crop %in% cultivos$tipo4 ~ "Especias, Tubérculos y Hortalizas",
      Crop %in% cultivos$tipo5 ~ "Cultivos Industriales, Fibras y Frutales",
      TRUE ~ "Na") )
  return(nueva_columna)}

# Aplicar función al dataframe
df <- clasificar_cultivo(df)
glimpse(df)
summary(df)

# Filtrar df por estado, cultivo y año:

# Crear una función para agrupar:
agrupar_categorias <- function (columna){
  dataframe <- df %>% 
    group_by({{columna}}) %>% 
    summarise(Registros = n(),
              Production = sum(Production),
              Area = sum(Area),
              Yield = sum(Yield))
  return(dataframe)}

Crop <- agrupar_categorias(Crop) %>% clasificar_cultivo()
State <- agrupar_categorias(State)
Year <- agrupar_categorias(Crop_Year)

# Detección de datos atipicos

# Total de Outliers
Outliers <- function(Columna, data){
  Q1 <- quantile(Columna, 0.25)
Q3 <- quantile(Columna, 0.75)
RIQ <- Q3 - Q1
inf <- Q1 - (1.5 * RIQ)
sup <- Q3 + (1.5 * RIQ)
if (inf < 0 ){ inf <- 0 }
outliers <- data[(Columna < inf) | (Columna > sup), ]
return(nrow(outliers))}

# Sacar el porcentaje:
porcentaje <- function(columna){
  porcentaje = (Outliers(columna, df)/2238)*100
  return(round(porcentaje, 2))
}

# Tabla de Resumen
datos_atipicos <- data.frame(
  Variable = c("Produccion", "Area", "Rendimiento"),
  Registros = c(nrow(df), nrow(df), nrow(df)),
  Total_Atipicos = c(Outliers(df$Production, df), Outliers(df$Area, df), Outliers(df$Yield, df)),
  Porcentaje = c(porcentaje(df$Production), porcentaje(df$Area), porcentaje(df$Yield))
  )


# Gráficos de Caja y Bigote (ESTÁN FEOS YA SE ARREGLARÁ):
# Producción:
ggplot(df, aes(Type_Crop, Production, fill = Type_Crop)) +
  geom_boxplot() +
  scale_y_log10() +
  theme_minimal() +
  theme(
    axis.text.x = element_blank(),
    plot.title = element_text(hjust = 0.5),
    plot.subtitle = element_text(hjust = 0.5)
  ) +
  labs(
    title = "Boxplot de la Producción Agricola dado el Tipo de Cultivo",
    subtitle = "Observación de datos atipicos",
    x = "Tipo de Cultivo",
    y = "Producción Agrícola (ton)",
    fill = "Type_Crop"
  )

# Area:
ggplot(df, aes(Type_Crop, Area, colour = Type_Crop)) +
  geom_boxplot() +
  scale_y_log10()

# Rendimiento:
ggplot(df, aes(Type_Crop, Yield, colour = Type_Crop)) +
  geom_boxplot() +
  scale_y_log10()


# Gráficos de disperción (NO OFICIAL):
# Producción vs Rendimiento
ggplot(df, aes(Production, Yield, colour = Type_Crop)) +
  geom_point() +
  scale_x_log10() +
  scale_y_log10()

# Producción vs Area
ggplot(df, aes(Production, Area, colour = Type_Crop)) +
  geom_point() +
  scale_x_log10() +
  scale_y_log10()

# Area vs Rendimiento
ggplot(df, aes(Area, Yield, colour = Type_Crop)) +
  geom_point() +
  scale_x_log10() +
  scale_y_log10()






