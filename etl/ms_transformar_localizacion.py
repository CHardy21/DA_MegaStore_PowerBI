import pandas as pd

def transformar_localizacion(df):
    """
    Replica el ETL de Dim_Localizacion en Power Query:
    - Renombra columnas (quita espacios)
    - Convierte tipos
    """

    # Paso 0: renombrado limpio de columnas
    df = df.rename(columns={
        "City": "City",
        "Segment": "Segment",
        "Country": "Country",
        "State": "State",
        "Postal Code": "PostalCode",
        "Region": "Region"
    })

    # Paso 1: convertir tipos
    df["PostalCode"] = pd.to_numeric(df["PostalCode"], errors="coerce").astype("Int64")

    # Retorno: tabla limpia de localización
    return df
