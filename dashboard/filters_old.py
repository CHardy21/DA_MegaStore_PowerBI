import streamlit as st
import pandas as pd

# Importar las funciones de los módulos
from .filter_modules.year_fllter_SegmentedControl import render_year_filter
from .filter_modules.category_filter import render_category_filter


def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renderiza todos los filtros en la sidebar, obtiene sus valores
    y aplica la lógica de filtrado al DataFrame.
    """
    st.sidebar.title("🔎 Filtros")

    # 1. Obtener valores de los filtros llamando a los módulos:
    
    # Llama al módulo de año (Debe devolver INT)
    year = render_year_filter(df) 
    
    # Llama al módulo de categoría (Debe devolver STR, o "Todas")
    categoria = render_category_filter(df)
    
    # --- LÍNEAS DE DEBUG (PARA VER EL VALOR Y EL TIPO) ---
    st.sidebar.caption(f"DEBUG YEAR: '{year}' (Type: {type(year).__name__})")
    st.sidebar.caption(f"DEBUG CAT: '{categoria}' (Type: {type(categoria).__name__})")
    # -----------------------------------------------------

    
    # --- Aplicación de Filtros (Lógica Secuencial Confirmada) ---
    
    df_filtrado = df.copy() 
    
    # 2. Aplicar filtro de Año 
    # **La clave: 'year' debe ser INT para comparar con df["OrderDate"].dt.year**
    if year is not None:
        try:
            # Aseguramos que sea un INT antes de comparar
            year_int = int(year) 
            df_filtrado = df_filtrado[df_filtrado["OrderDate"].dt.year == year_int]
        except ValueError:
            # Si la conversión a INT falla, ignoramos el filtro de año para no romper la app
            st.warning("Advertencia de filtro: El valor del año no es un número entero.")
            
    
    # 3. Aplicar filtro de Categoría
    if categoria != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Category"] == categoria]
        
    # 4. Retorna el DataFrame filtrado
    return df_filtrado


# import streamlit as st

# def render_filters(df):
#     st.sidebar.title("🔎 Filtros")
    
#     year = st.sidebar.selectbox(
#         "Año",
#         sorted(df["OrderDate"].dt.year.dropna().unique())
#     )
    
#     categoria = st.sidebar.selectbox(
#         "Categoría",
#         ["Todas"] + sorted(df["Category"].dropna().unique())
#     )
    
#     # --- Aplicación de filtros ---
#     df_filtrado = df[df["OrderDate"].dt.year == year]
#     if categoria != "Todas":
#         df_filtrado = df_filtrado[df_filtrado["Category"] == categoria]
    
#     return df_filtrado
