import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from src.penguins_pipeline import carga_datos, apply_filters, grafico_masa_por_especie, distribucion_especie, graficos_lmplot, heatmap_correlaciones, compute_kpis


from PIL import Image
import streamlit as st

#Configuracion de la pagina

st.set_page_config(page_title="Grupazo 4", #titulo de la pagina
                   layout="wide", #para que ocupe el ancho de la ventana"
                   page_icon="🐧")


# Cargar imagen local
cabecera = Image.open("imagen_pinguinos.png")

# Mostrarla como banner
st.image(cabecera, width='stretch')

st.markdown("""
    <style>
    /* Elimina el espacio superior (padding) del contenedor principal */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

#Título debajo de la cabecera
st.title("Análisis del grupazo 4")

# Texto a poner debajo del titulo
with st.expander("👥 Integrantes del equipo"):
    st.markdown("""
    **Chiara Contreras**  
    **Jenireé Tovar**  
    **Lucia Llaneza**  
    **Michelle Olivares**  
    **Sara Bailon**  
    """)

# Carga del dataset
df = carga_datos()

#Creacion de la barra lateral
opcion = st.sidebar.selectbox(
    "Selecciona qué quieres ver:",
    [
        "Nada",
        "Gráfico: Masa corporal por especie",
        "Gráfico: Distribución por especie (pie chart)",
        "Gráficos lmplot",
        "Tabla filtrada",
        "Heatmap de correlaciones"
    ]
)

if opcion == "Gráfico: Masa corporal por especie":
    grafico_masa_por_especie(df)

if opcion == "Gráfico: Distribución por especie (pie chart)":
    distribucion_especie(df)

if opcion == "Gráficos lmplot":
    graficos_lmplot(df)

if opcion == "Tabla filtrada":
    apply_filters(df)

if opcion == "Heatmap de correlaciones":
    heatmap_correlaciones(df)

# Añadir metricas generales: 



with st.expander("📊 Métricas generales del dataset"):
    compute_kpis(df)


conteo_islas = df['Island'].value_counts().to_dict()
# Crear un mapa con las islas
m = folium.Map(location=[-62.1, -57.9], zoom_start=7)

# Centro del mapa (aprox. zona de las islas)
m = folium.Map(location=[-65.0, -64.5], zoom_start=8)

st.subheader("🗺️ Mapa de las islas analizadas")

title_html = '''
     <h3 align="center" style="font-size:20px"><b>Mapa de las islas analizadas</b></h3>
     '''
m.get_root().html.add_child(folium.Element(title_html))

# Marcadores de las islas
# Biscoe
folium.Marker(
    [-65.4333, -65.5000],
    popup=f"Isla Biscoe — {conteo_islas.get('Biscoe', 0)} 🐧",
    tooltip=f"Biscoe: {conteo_islas.get('Biscoe', 0)} 🐧",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

# Dream
folium.Marker(
    [-64.7333, -64.2333],
    popup=f"Isla Dream — {conteo_islas.get('Dream', 0)} 🐧",
    tooltip=f"Dream: {conteo_islas.get('Dream', 0)} 🐧",
    icon=folium.Icon(color="green", icon="info-sign")
).add_to(m)

# Torgersen
folium.Marker(
    [-64.7667, -64.0833],
    popup=f"Isla Torgersen — {conteo_islas.get('Torgersen', 0)} 🐧",
    tooltip=f"Torgersen: {conteo_islas.get('Torgersen', 0)} 🐧",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# Mostrar mapa en Streamlit
st_folium(m, width=700, height=500)

