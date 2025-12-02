import streamlit as st
import pandas as pd

# Importar las funciones de los módulos
from .filter_modules.year_filter import render_year_filter
from .filter_modules.category_filter import render_category_filter



def aplicar_filtro(df: pd.DataFrame, columna: str, seleccion, todas_opciones=None) -> pd.DataFrame:
    """
    Aplica filtro universal para cualquier columna y selección.
    - seleccion puede ser un valor único, lista o 'Todas'
    - todas_opciones: lista con todas las categorías posibles (para detectar selección completa)
    """
    if seleccion is None:
        return df
    
    # Caso multiselect vacío → mostrar todo
    if isinstance(seleccion, list) and len(seleccion) == 0:
        return df
    
    # Caso multiselect con todas las opciones → mostrar todo
    if todas_opciones is not None and isinstance(seleccion, list):
        if set(seleccion) == set(todas_opciones):
            return df
    
    # Caso 'Todas' explícito
    if seleccion == "Todas":
        return df
    
    # Caso lista parcial
    if isinstance(seleccion, list):
        return df[df[columna].isin(seleccion)]
    
    # Caso valor único
    return df[df[columna] == seleccion]



def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renderiza todos los filtros en la sidebar, obtiene sus valores
    y aplica la lógica de filtrado al DataFrame.
    """
    st.sidebar.title("🔎 Filtros")

    # --- Estado inicial ---
    if "reset" not in st.session_state:
        st.session_state.reset = False

    # 1. Obtener valores de los filtros llamando a los módulos:
    if st.session_state.reset:
        # Si se presionó reset → vaciamos selección
        year = None
        categoria = []
        st.session_state.reset = False
    else:
        year = render_year_filter(df, tipo="segmentedControl")        # Debe devolver INT
        categoria = render_category_filter(df, tipo="selectbox")      # Puede devolver STR, lista o "Todas"

    # --- LÍNEAS DE DEBUG (PARA VER EL VALOR Y EL TIPO) ---
    st.sidebar.caption(f"DEBUG YEAR: '{year}' (Type: {type(year).__name__})")
    st.sidebar.caption(f"DEBUG CAT: '{categoria}' (Type: {type(categoria).__name__})")
    # -----------------------------------------------------

    # --- Aplicación de Filtros ---
    df_filtrado = df.copy()

    # 2. Aplicar filtro de Año
    if year is not None:
        try:
            year_int = int(year)
            df_filtrado = df_filtrado[df_filtrado["OrderDate"].dt.year == year_int]
        except ValueError:
            st.warning("Advertencia de filtro: El valor del año no es un número entero.")

    # 3. Aplicar filtro de Categoría
    todas_categorias = df["Category"].unique().tolist()

    # Normalizar selección: si incluye "Todas", lo tratamos como lista vacía
    if isinstance(categoria, list) and "Todas" in categoria:
        categoria = []

    df_filtrado = aplicar_filtro(df_filtrado, "Category", categoria, todas_opciones=todas_categorias)

    # --- Botón Reset ---
    if st.sidebar.button("🔄 Resetear filtros"):
        st.session_state.reset = True
        st.rerun()

    # 4. Retorna el DataFrame filtrado
    return df_filtrado
