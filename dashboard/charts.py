import streamlit as st
import plotly.express as px

def render_charts(df_filtrado):
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # Línea temporal: ventas y profit por mes
    df_filtrado["Month"] = df_filtrado["OrderDate"].dt.month
    df_mes = df_filtrado.groupby("Month")[["TotalSales", "Profit"]].sum().reset_index()
    fig_linea = px.line(df_mes, x="Month", y=["TotalSales", "Profit"], title="Ventas y Profit por Mes")
    with row1_col1:
        st.plotly_chart(fig_linea, use_container_width=True)

    # Barras por producto
    df_prod = df_filtrado.groupby("ProductName")[["TotalSales", "TotalDiscount", "Profit"]].sum().reset_index()
    fig_prod = px.bar(df_prod, x="ProductName", y=["TotalSales", "TotalDiscount", "Profit"], title="Métricas por Producto")
    with row1_col2:
        st.plotly_chart(fig_prod, use_container_width=True)

    # Barras por ciudad
    if "City" in df_filtrado.columns:
        df_ciudad = df_filtrado.groupby("City")["Profit"].sum().reset_index()
        fig_ciudad = px.bar(df_ciudad, x="City", y="Profit", title="Profit por Ciudad")
        with row2_col1:
            st.plotly_chart(fig_ciudad, use_container_width=True)

    # Mapa por estado (USA)
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
    with row2_col2:
        st.plotly_chart(fig_mapa, use_container_width=True)
