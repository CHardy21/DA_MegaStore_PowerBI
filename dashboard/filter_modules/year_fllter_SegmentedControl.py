import streamlit as st

def render_year_filter(df):
    years = sorted(df["OrderDate"].dt.year.dropna().unique())
    year = st.sidebar.segmented_control("Año", years)
    return year
