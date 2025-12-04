import pandas as pd

def construir_modelo(clientes, localizacion, productos, ordenes, calendar):
    """
    Construye el modelo estrella uniendo fact y dimensiones:
    - Fact table: ordenes (Fact_Sales_SinDuplicados)
    - Dimensiones: clientes, productos, localización, calendario
    """

    df = ordenes.copy()

    # Aseguramos que la fecha esté en datetime
    if "OrderDate" in df.columns:
        df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

    # --- Join con productos ---
    if "ProductID" in df.columns and "ProductID" in productos.columns:
        df = df.merge(productos, on="ProductID", how="left")

    # --- Join con clientes ---
    if "CustomerID" in df.columns and "CustomerID" in clientes.columns:
        df = df.merge(clientes, on="CustomerID", how="left")

    # --- Join con localización ---
    if "City" in df.columns and "City" in localizacion.columns:
        df = df.merge(localizacion, on="City", how="left")

    # --- Join con calendario ---
    if "OrderDate" in df.columns and "Date" in calendar.columns:
        df = df.merge(calendar, left_on="OrderDate", right_on="Date", how="left")

    # --- Normalización de columnas conflictivas ---
    # Si quedaron columnas duplicadas de City, unificamos en una sola
    if "City_x" in df.columns or "City_y" in df.columns:
        df["City"] = df["City_x"].fillna(df.get("City_y"))
        df = df.drop(columns=[c for c in ["City_x", "City_y"] if c in df.columns])

    return df
