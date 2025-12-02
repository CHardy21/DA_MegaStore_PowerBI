# 🐍 Código Python para Generar el Dataset Simulado
# Vamos a generar una tabla principal que contenga ventas mensuales, desglosadas por canal, para los períodos 2018-2024.

# 1. Script de Generación de Datos



import pandas as pd
import numpy as np
from datetime import date, timedelta

# --- 1. Definición del Período de Tiempo y Parámetros ---
# Simularemos 84 meses: 7 años (2018 a 2024)
start_date = date(2018, 1, 1)
end_date = date(2024, 12, 1) # Usaremos datos proyectados hasta el fin de 2024
dates = pd.date_range(start=start_date, end=end_date, freq='MS')
n_months = len(dates)

# Parámetros Base para Ventas (en una unidad de venta, ej: Millones)
# Ventas base que crecerán a lo largo del tiempo
base_sales = 50.0 
base_growth = 0.005 # Crecimiento mensual pre-pandemia (0.5%)

# Puntos de Inflexión de la Historia
PANDEMIC_START_INDEX = np.where(dates == pd.to_datetime('2020-03-01'))[0][0]
PANDEMIC_PEAK_INDEX = np.where(dates == pd.to_datetime('2021-06-01'))[0][0]
POST_PANDEMIC_START_INDEX = np.where(dates == pd.to_datetime('2022-01-01'))[0][0]

# --- 2. Generación de las Ventas Totales Mensuales ---
monthly_sales = []
current_sales = base_sales

for i in range(n_months):
    # Crecimiento Base Pre-Pandemia
    growth_factor = base_growth
    
    if i < PANDEMIC_START_INDEX:
        # Pre-Pandemia: Crecimiento estable con ruido
        growth_factor = base_growth + np.random.uniform(-0.002, 0.004)
        
    elif i >= PANDEMIC_START_INDEX and i < POST_PANDEMIC_START_INDEX:
        # Pandemia (Mar 2020 - Dic 2021): Boom de Ventas
        # Fuerte crecimiento al inicio (necesidad) que se desacelera (stock/saturación)
        if i < PANDEMIC_PEAK_INDEX:
            # Boom inicial
            growth_factor = 0.015 + np.random.uniform(0.005, 0.015) 
        else:
            # Desaceleración por saturación del mercado/escasez
            growth_factor = 0.001 + np.random.uniform(-0.005, 0.008)
            
    else:
        # Post-Pandemia (Ene 2022 - Dic 2024): Normalización y Enfriamiento
        # Se normaliza la demanda, crecimiento lento o estancamiento/caída
        growth_factor = 0.002 + np.random.uniform(-0.008, 0.004)
    
    current_sales *= (1 + growth_factor)
    
    # Aplicar estacionalidad (ej: Black Friday/Navidad en Nov/Dic)
    if dates[i].month in [11, 12]:
        current_sales *= 1.15  # Pico de estacionalidad
    elif dates[i].month in [1, 2]:
        current_sales *= 0.9  # Valle de estacionalidad
        
    # Añadir un poco de ruido general
    current_sales += np.random.uniform(-1.5, 1.5)
    
    monthly_sales.append(max(0, current_sales)) # Asegurar que no haya ventas negativas

# Crear el DataFrame base
df = pd.DataFrame({'Fecha': dates, 'Ventas_Totales_USD_MM': monthly_sales})

# --- 3. Desglose por Canales de Venta (Online vs. Sucursales) ---
# Simular la dramática migración de Sucursal -> Online durante la pandemia

def get_online_share(date_series):
    """Retorna la cuota de mercado Online basada en la fecha."""
    
    # Pre-Pandemia (Hasta Mar 2020): Cuota baja (ej: 15%) con ligero crecimiento
    if date_series < pd.to_datetime('2020-03-01'):
        return 0.15 + (date_series.month / 1200) + np.random.uniform(-0.02, 0.02)
    
    # Pandemia (Mar 2020 - Dic 2021): Rápido crecimiento hasta un pico (ej: 45%)
    elif date_series < pd.to_datetime('2022-01-01'):
        # Calculamos la posición dentro del período pandémico para un crecimiento sigmoidal
        delta = (date_series - pd.to_datetime('2020-03-01')).days
        max_delta = (pd.to_datetime('2022-01-01') - pd.to_datetime('2020-03-01')).days
        # Transición rápida de 15% a 45%
        share = 0.15 + 0.30 * (delta / max_delta)**0.5 
        return share + np.random.uniform(-0.03, 0.05)
    
    # Post-Pandemia (Ene 2022 en adelante): Consolidación (ej: 40%) con menor ruido
    else:
        return 0.40 + np.random.uniform(-0.04, 0.01)

# Aplicar la función y calcular las columnas finales
df['Cuota_Online'] = df['Fecha'].apply(get_online_share).clip(0.05, 0.60) # Limitar la cuota entre 5% y 60%
df['Ventas_Online_USD_MM'] = df['Ventas_Totales_USD_MM'] * df['Cuota_Online']
df['Ventas_Sucursales_USD_MM'] = df['Ventas_Totales_USD_MM'] * (1 - df['Cuota_Online'])

# Redondear y formatear
df = df.round(2)
df.insert(0, 'Año', df['Fecha'].dt.year)
df.insert(1, 'Mes', df['Fecha'].dt.month)

# --- 4. Generación de Subcategorías de Productos (Opcional, pero enriquece la historia) ---
# Simularemos 3 subcategorías clave:
# 1. Tecnología_Remoto (Laptops, Monitores, Webcams): Boom en Pandemia
# 2. Línea_Blanca (Refrigeradores, Lavadoras): Crecimiento estable, impulso por el hogar
# 3. Accesorios_Entretenimiento (Gadgets, Auriculares): Crecimiento moderado
df['Tecnologia_Remoto_USD_MM'] = df['Ventas_Totales_USD_MM'] * (0.35 + np.random.normal(0, 0.05)) # Peso medio 35%
df['Linea_Blanca_USD_MM'] = df['Ventas_Totales_USD_MM'] * (0.40 + np.random.normal(0, 0.05)) # Peso medio 40%
df['Accesorios_Entretenimiento_USD_MM'] = df['Ventas_Totales_USD_MM'] * (0.25 + np.random.normal(0, 0.05)) # Peso medio 25%

# Asegurar que la suma sea ~Ventas_Totales
df['Suma_Categorias'] = df['Tecnologia_Remoto_USD_MM'] + df['Linea_Blanca_USD_MM'] + df['Accesorios_Entretenimiento_USD_MM']
df['Ajuste_Factor'] = df['Ventas_Totales_USD_MM'] / df['Suma_Categorias']

df['Tecnologia_Remoto_USD_MM'] *= df['Ajuste_Factor']
df['Linea_Blanca_USD_MM'] *= df['Ajuste_Factor']
df['Accesorios_Entretenimiento_USD_MM'] *= df['Ajuste_Factor']

# Limpieza final
df = df.drop(columns=['Suma_Categorias', 'Ajuste_Factor', 'Cuota_Online'])
df.rename(columns={'Ventas_Totales_USD_MM': 'Ventas_Netas_Totales_USD_MM'}, inplace=True)
df = df.round(2)

print("¡Dataset simulado generado con éxito!")
print(df.head(5))
print(df.tail(5))

# Guardar el dataset para su uso posterior
df.to_csv('ventas_electro_tecnologia_simulado.csv', index=False)