import streamlit as st
import pandas as pd
import plotly.express as px
from etl.transformar_clientes import transformar_clientes
from etl.transformar_localizacion import transformar_localizacion
from etl.transformar_productos import transformar_productos
from etl.transformar_ordenes import transformar_ordenes
from etl.build_modelo_estrella import construir_modelo
from etl.generar_calendar import generar_calendar
from dashboard.styles import apply_custom_css
from dashboard.filters import render_filters
from dashboard.layout import render_layout

# --- Configuración inicial ---
st.set_page_config(
    #page_title="📊 MegaStore Dashboard (Python)",
    layout="wide",  
    initial_sidebar_state="expanded"
)

# Aplico CSS global
apply_custom_css()

# --- Carga de datos crudos ---
clientes = pd.read_csv("data/raw/clientes.csv")
localizacion = pd.read_csv("data/raw/localizacion.csv")
productos = pd.read_csv("data/raw/productos.csv")
ordenes = pd.read_csv("data/raw/ordenes.csv")

# --- ETL modular ---
clientes = transformar_clientes(clientes)
localizacion = transformar_localizacion(localizacion)
productos = transformar_productos(productos)
ordenes = transformar_ordenes(ordenes)
# --- Generar calendario ---
calendar = generar_calendar(ordenes)

# --- Construcción del modelo estrella ---
df = construir_modelo(clientes, localizacion, productos, ordenes, calendar)

# --- Sidebar de filtros ---
df_filtrado = render_filters(df)

st.title("📊 MegaStore Dashboard (Python)")

render_layout(df_filtrado)