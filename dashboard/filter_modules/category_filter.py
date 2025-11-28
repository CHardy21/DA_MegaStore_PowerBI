import streamlit as st
import pandas as pd

def render_category_filter(df: pd.DataFrame):
    """Renderiza el filtro de Categoría (usando st.selectbox) y retorna la categoría seleccionada."""
    
    # Obtener opciones
    options = ["Todas"] + sorted(df["Category"].dropna().unique())
    
    # Renderizar el filtro en la barra lateral
    categoria = st.sidebar.selectbox(
        "Categoría",
        options=options
    )
    
    # Devolver el valor
    return categoria