import streamlit as st
import pandas as pd
import plotly.express as px
from etl.transformar_clientes import transformar_clientes
from etl.transformar_localizacion import transformar_localizacion
from etl.transformar_productos import transformar_productos
from etl.transformar_ordenes import transformar_ordenes
from etl.build_modelo_estrella import construir_modelo
from etl.generar_calendar import generar_calendar

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
st.sidebar.title("🔎 Filtros")
year = st.sidebar.selectbox("Año", sorted(df["OrderDate"].dt.year.dropna().unique()))
categoria = st.sidebar.selectbox("Categoría", ["Todas"] + sorted(df["Category"].dropna().unique()))

# --- Aplicación de filtros ---
df_filtrado = df[df["OrderDate"].dt.year == year]
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Category"] == categoria]

# --- KPIs ---
df_filtrado["TotalSales"] = df_filtrado["Sales"] * df_filtrado["Quantity"]
df_filtrado["TotalDiscount"] = df_filtrado["TotalSales"] * df_filtrado["Discount"]

total_sales = df_filtrado["TotalSales"].sum()
total_profit = df_filtrado["Profit"].sum()
total_discount = df_filtrado["TotalDiscount"].sum()
avg_sales_per_order = df_filtrado["TotalSales"].mean()

st.title("📊 MegaStore Dashboard (Python)")
st.metric("Total Sales Amount", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric("Total Discount", f"${total_discount:,.2f}")
st.metric("Average Sales per Order", f"${avg_sales_per_order:,.2f}")

# --- Línea temporal: ventas y profit por mes ---
df_filtrado["Month"] = df_filtrado["OrderDate"].dt.month
df_mes = df_filtrado.groupby("Month")[["TotalSales", "Profit"]].sum().reset_index()
fig_linea = px.line(df_mes, x="Month", y=["TotalSales", "Profit"], title="Ventas y Profit por Mes")
st.plotly_chart(fig_linea)

# --- Barras por producto ---
df_prod = df_filtrado.groupby("ProductName")[["TotalSales", "TotalDiscount", "Profit"]].sum().reset_index()
fig_prod = px.bar(df_prod, x="ProductName", y=["TotalSales", "TotalDiscount", "Profit"], title="Métricas por Producto")
st.plotly_chart(fig_prod)

# --- Barras por ciudad ---
if "City" in df_filtrado.columns:
    df_ciudad = df_filtrado.groupby("City")["Profit"].sum().reset_index()
    fig_ciudad = px.bar(df_ciudad, x="City", y="Profit", title="Profit por Ciudad")
    st.plotly_chart(fig_ciudad)

# --- Mapa por estado (USA) ---
# Diccionario de estados de EE.UU.
state_map = {
    "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA","Colorado":"CO","Connecticut":"CT",
    "Delaware":"DE","Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA",
    "Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI",
    "Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH",
    "New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK",
    "Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN",
    "Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"
}

df_estado = df_filtrado.groupby("State")["TotalSales"].sum().reset_index()
df_estado["StateCode"] = df_estado["State"].map(state_map)

fig_mapa = px.choropleth(
    df_estado,
    locations="StateCode",
    locationmode="USA-states",
    color="TotalSales",
    scope="usa",
    title="Ventas por Estado"
)
st.plotly_chart(fig_mapa)
