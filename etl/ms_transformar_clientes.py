import pandas as pd

def transformar_clientes(df):
    """
    ETL de Dim_Clientes:
    - Renombra columnas
    - Convierte tipos
    - Consolida clientes únicos
    """

    df = df.rename(columns={
        "Customer ID": "CustomerID",
        "Customer Name": "CustomerName",
        "Segment": "Segment",
        "Country": "Country",
        "City": "City",
        "State": "State",
        "Postal Code": "PostalCode",
        "Region": "Region"
    })

    df["PostalCode"] = pd.to_numeric(df["PostalCode"], errors="coerce").astype("Int64")

    # Consolidar por CustomerID
    df = (
        df.groupby("CustomerID", as_index=False)
          .agg({
              "CustomerName": "first",
              "Segment": "first",
              "Country": "first",
              "City": "first",
              "State": "first",
              "PostalCode": "first",
              "Region": "first"
          })
    )

    return df   # <-- solo devuelve la dimensión oficial
