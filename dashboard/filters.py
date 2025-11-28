import streamlit as st

def render_filters(df):
    st.sidebar.title("🔎 Filtros")
    
    year = st.sidebar.selectbox(
        "Año",
        sorted(df["OrderDate"].dt.year.dropna().unique())
    )
    
    categoria = st.sidebar.selectbox(
        "Categoría",
        ["Todas"] + sorted(df["Category"].dropna().unique())
    )
    
    # --- Aplicación de filtros ---
    df_filtrado = df[df["OrderDate"].dt.year == year]
    if categoria != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Category"] == categoria]
    
    return df_filtrado
