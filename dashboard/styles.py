import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Estilos para los KPIs */
        div[data-testid="metric-container"] {
            background-color: transparent;   /* 👈 fondo transparente */
            border: 1px solid #ccc;          /* 👈 borde gris claro */
            border-radius: 12px;             /* 👈 borde redondeado */
            padding: 12px;
            margin: 5px;
        }

        /* Opcional: centrar texto dentro de los KPIs */
        div[data-testid="metric-container"] > div {
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
