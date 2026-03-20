install.packages(c("tidyverse", "sf", "rnaturalearth", "rnaturalearthdata", "viridis", "pak"))

# Cargar las librerías
library(tidyverse)
library(sf)
library(rnaturalearth)
library(pak)
library(viridis)

# Carga de df
df_india <- read.csv("27. Agricultura.csv")

# 2. Preparar los datos
# Agrupamos por estado ('State') y calculamos una métrica de fertilización.
# Es mejor calcular la "Intensidad" (Fertilizante / Área) en lugar del total, 
# para que los estados más grandes no sesguen el mapa por su tamaño.
df_resumen <- df_india %>%
  group_by(State) %>%
  summarise(
    Total_Fertilizer = sum(Fertilizer, na.rm = TRUE),
    Total_Area = sum(Area, na.rm = TRUE),
    Fertilizer_Intensity = Total_Fertilizer / Total_Area
  )

# 3. Descargar el mapa base de la India
india_map <- ne_states(country = "India", returnclass = "sf")

# 4. Unir el mapa con tus datos
# Debemos unirla con tu columna 'State'. 
# Es crucial que los nombres coincidan exactamente. Si hay diferencias (ej. "Andhra Pradesh" vs "Andhra"), 
# tendrás que estandarizarlos previamente usando mutate() y case_match() o recode().
mapa_datos <- india_map %>%
  left_join(df_resumen, by = c("name" = "State"))

# 5. Graficar el mapa
ggplot(data = mapa_datos) +
  # Se mapea el relleno (fill) a la intensidad de fertilización
  geom_sf(aes(fill = Fertilizer_Intensity), color = "white", size = 0.2) +
  # Configuramos la escala de colores
  scale_fill_viridis_c(
    option = "magma", 
    direction = -1,
    name = "Intensidad de\nFertilización", 
    na.value = "gray90" # Color para estados sin datos
  ) +
  # Etiquetas del gráfico
  labs(
    title = "Zonas de Fertilización en India",
    subtitle = "Uso de fertilizante por unidad de área a nivel estatal",
    caption = "Datos agrícolas de India",
    x = "", y = ""
  ) +
  # Tema visual limpio ideal para mapas
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 16, hjust = 0.5),
    plot.subtitle = element_text(size = 12, hjust = 0.5),
    axis.text = element_blank(),  # Ocultar coordenadas
    axis.ticks = element_blank(),
    panel.grid = element_blank(), # Quitar cuadrícula
    legend.position = "right"
  )
