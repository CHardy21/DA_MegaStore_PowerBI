import pandas as pd

def transformar_productos(df):
    """
    ETL de Dim_Productos:
    - Renombra columnas
    - Elimina fila duplicada de encabezados si quedó
    - Consolida productos únicos por ProductID
    """

    df = df.rename(columns={
        "Product ID": "ProductID",
        "Product Name": "ProductName",
        "Category": "Category",
        "Sub-Category": "SubCategory"
    })

    # Eliminar fila duplicada de encabezados si quedó
    if set(df.columns).issubset(set(df.iloc[0].values)):
        df = df.iloc[1:].reset_index(drop=True)

    # Consolidar por ProductID
    df = (
        df.groupby("ProductID", as_index=False)
          .agg({
              "ProductName": "first",
              "Category": "first",
              "SubCategory": "first"
          })
    )

    return df   # <-- solo devuelve la dimensión oficial

