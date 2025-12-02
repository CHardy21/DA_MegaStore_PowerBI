import streamlit as st
import pandas as pd


def render_year_filter(df, tipo="selectbox"):
    
    # Valores únicos de año
    years = sorted(df["OrderDate"].dt.year.dropna().unique())
    
    # Segmentador dinámico según tipo
    if tipo == "selectbox":
        year = st.sidebar.selectbox("Año", years)
    
    elif tipo == "radio":
        years = sorted(df["OrderDate"].dt.year.dropna().unique())
        year = st.sidebar.radio("Año", years, horizontal=True)

    elif tipo == "segmentedControl":
        years = sorted(df["OrderDate"].dt.year.dropna().unique())
        year = st.sidebar.segmented_control("Año", years)

    elif tipo == "buttons":
        if "selected_year" not in st.session_state:
            st.session_state.selected_year = years[-1]

        # Usamos filas dinámicas en el sidebar
        n_cols = 3  # cantidad de botones por fila
        for i in range(0, len(years), n_cols):
            cols = st.sidebar.columns(n_cols)
            for j, y in enumerate(years[i:i+n_cols]):
                if cols[j].button(str(y), key=f"btn_{y}"):
                    st.session_state.selected_year = y

        year = st.session_state.selected_year

    elif tipo == "buttons2":
        # CSS para resaltar el botón activo
        st.markdown("""
            <style>
            .pill-container {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }
            .pill-button {
                border: none;
                border-radius: 20px;
                padding: 6px 14px;
                background-color: #f0f2f6;
                font-weight: 600;
                cursor: pointer;
            }
            .pill-button.active {
                background-color: #4CAF50;
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)

        # Render dinámico con estado
        st.markdown("<div class='pill-container'>", unsafe_allow_html=True)
        for y in years:
            active_class = "active" if st.session_state.selected_year == y else ""
            if st.button(f"{y}", key=f"btn_{y}"):
                st.session_state.selected_year = y
            st.markdown(
                f"<button class='pill-button {active_class}'>{y}</button>",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

        year = st.session_state.selected_year
        
    elif tipo == "multiselect":
        year = st.sidebar.multiselect("Año", years, default=[years[-1]])
    
    elif tipo == "checkboxes":
        # Renderizar cada año como checkbox
        selected_years = []
        for y in years:
            if st.sidebar.checkbox(str(y), value=(y == years[-1])):
                selected_years.append(y)
        year = selected_years
    
    else:
        st.sidebar.warning("Tipo de filtro no soportado")
        year = None
    
    return year



# def render_year_filter(df: pd.DataFrame):
    
#     # 1. Obtener opciones (como ENTEROS)
#     years_series = df["OrderDate"].dt.year.dropna()
#     available_years = sorted(years_series.unique().tolist())
    
#     if not available_years:
#         return None 
    
#     # 2. Valor por defecto (siempre el último año, como ENTERO)
#     default_year_int = available_years[-1]
    
#     # 3. Preparar para st.pills (convirtiendo a STRING)
#     options_as_strings = [str(year) for year in available_years]
#     default_year_str = str(default_year_int)
    
#     # Renderizar el filtro (devuelve una lista de strings)
#     # CORRECCIÓN: AÑADIMOS key="year_filter_key" para forzar la actualización
#     selected_years = st.sidebar.pills(
#         "Año",
#         options=options_as_strings,
#         default=default_year_str,
#         key="year_filter_key" # <-- SOLUCIÓN AL PROBLEMA DE ACTUALIZACIÓN
#     )
    
#     # 4. Devolver el valor seleccionado como ENTERO
#     if selected_years and selected_years[0].isdigit():
#         # Devolver el valor seleccionado como entero
#         return int(selected_years[0])
#     else:
#         # Devolver el valor por defecto como entero (en caso de fallas)
#         return default_year_int