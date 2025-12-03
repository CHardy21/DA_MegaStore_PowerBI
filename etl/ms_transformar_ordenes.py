import pandas as pd

def transformar_ordenes(df):
    """
    Replica el ETL de Fact_Sales en Power Query:
    - Renombra columnas para quitar espacios
    - Elimina duplicados exactos
    - Consolida por OrderID + ProductID
    """

    # Paso 0: renombrado limpio
    df = df.rename(columns={
        "Order ID": "OrderID",
        "Order Date": "OrderDate",
        "Ship Date": "ShipDate",
        "Ship Mode": "ShipMode",
        "Customer ID": "CustomerID",
        "Product ID": "ProductID",
        "Postal Code": "PostalCode",
        "Sub-Category": "SubCategory"
    })

    # Convertir tipos (similar a TransformColumnTypes)
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df["ShipDate"] = pd.to_datetime(df["ShipDate"])
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").astype("Int64")
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    if "Devolucion" in df.columns:
        df["Devolucion"] = pd.to_numeric(df["Devolucion"], errors="coerce").astype("Int64")

    # Paso 1: eliminar duplicados exactos
    df = df.drop_duplicates()

    # Paso 2: consolidar por OrderID + ProductID
    agg_funcs = {
        "OrderDate": "min",       # fecha mínima
        "ShipDate": "max",        # fecha máxima
        "ShipMode": "first",      # primer valor
        "CustomerID": "first",
        "City": "first",
        "Sales": "sum",
        "Quantity": "sum",
        "Discount": "mean",       # promedio si varía
        "Profit": "sum",
    }
    if "Devolucion" in df.columns:
        agg_funcs["Devolucion"] = "max"

    df = df.groupby(["OrderID", "ProductID"], as_index=False).agg(agg_funcs)

    return df
