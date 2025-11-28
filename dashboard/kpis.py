import streamlit as st

def render_kpis(df_filtrado):
    df_filtrado["TotalSales"] = df_filtrado["Sales"] * df_filtrado["Quantity"]
    df_filtrado["TotalDiscount"] = df_filtrado["TotalSales"] * df_filtrado["Discount"]

    total_sales = df_filtrado["TotalSales"].sum()
    total_profit = df_filtrado["Profit"].sum()
    total_discount = df_filtrado["TotalDiscount"].sum()
    avg_sales_per_order = df_filtrado["TotalSales"].mean()

    # --- KPIs en horizontal ---
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.metric("Total Sales Amount", f"${total_sales:,.2f}")
    with kpi_cols[1]:
        st.metric("Total Profit", f"${total_profit:,.2f}")
    with kpi_cols[2]:
        st.metric("Total Discount", f"${total_discount:,.2f}")
    with kpi_cols[3]:
        st.metric("Avg Sales per Order", f"${avg_sales_per_order:,.2f}")
