import pandas as pd
import numpy as np
from datetime import date, timedelta
import random
from faker import Faker # Para generar nombres y direcciones falsas

fake = Faker('es_AR') # Faker para Argentina

# --- 1. Definición del Período de Tiempo ---
start_date = date(2018, 1, 1)
end_date = date(2024, 12, 31) # Datos hasta fin de 2024
dates = pd.date_range(start=start_date, end=end_date, freq='D') # Datos diarios para transacciones

PANDEMIC_START_DATE = pd.to_datetime('2020-03-01')
POST_PANDEMIC_START_DATE = pd.to_datetime('2022-01-01')

# --- 2. Dimensión Productos (dim_productos.csv) ---
productos_data = {
    'producto_id': range(1, 21),
    'nombre_producto': [
        'Laptop Premium', 'Monitor UltraHD', 'Webcam Full HD', 'Router WiFi 6', 'Impresora Multifunción',
        'Heladera No Frost', 'Lavadora Carga Frontal', 'Cocina Vitrocerámica', 'Microondas Digital', 'Aire Acondicionado Inverter',
        'Smart TV 55"', 'Consola Gaming', 'Auriculares Inalámbricos', 'Smartwatch Deportivo', 'Parlante Bluetooth',
        'Tablet Pro', 'Cafetera Espresso', 'Aspiradora Robot', 'Licuadora de Alta Potencia', 'Barra de Sonido'
    ],
    'categoria_producto': [
        'Tecnologia_Remoto', 'Tecnologia_Remoto', 'Tecnologia_Remoto', 'Tecnologia_Remoto', 'Tecnologia_Remoto',
        'Linea_Blanca', 'Linea_Blanca', 'Linea_Blanca', 'Linea_Blanca', 'Linea_Blanca',
        'Accesorios_Entretenimiento', 'Accesorios_Entretenimiento', 'Accesorios_Entretenimiento', 'Accesorios_Entretenimiento', 'Accesorios_Entretenimiento',
        'Tecnologia_Remoto', 'Linea_Blanca', 'Linea_Blanca', 'Linea_Blanca', 'Accesorios_Entretenimiento'
    ],
    'precio_unitario_usd': [
        1200, 450, 70, 150, 220,
        900, 750, 600, 180, 1100,
        800, 500, 120, 250, 80,
        600, 100, 300, 90, 200
    ]
}
df_productos = pd.DataFrame(productos_data)
df_productos.to_csv('dim_productos.csv', index=False)
print("Generado: dim_productos.csv")

# --- 3. Dimensión Clientes (dim_clientes.csv) ---
n_clientes = 5000
clientes_data = {
    'cliente_id': range(1, n_clientes + 1),
    'nombre_cliente': [fake.name() for _ in range(n_clientes)],
    'email_cliente': [fake.email() for _ in range(n_clientes)],
    'ciudad_cliente': [fake.city() for _ in range(n_clientes)],
    'segmento_cliente': np.random.choice(['Premium', 'Frecuente', 'Ocasional', 'Nuevo'], n_clientes, p=[0.1, 0.3, 0.4, 0.2])
}
df_clientes = pd.DataFrame(clientes_data)
df_clientes.to_csv('dim_clientes.csv', index=False)
print("Generado: dim_clientes.csv")

# --- 4. Dimensión Sucursales (dim_sucursales.csv) ---
provincias_argentinas = [
    'Buenos Aires', 'Catamarca', 'Chaco', 'Chubut', 'Córdoba', 'Corrientes', 'Entre Ríos', 'Formosa',
    'Jujuy', 'La Pampa', 'La Rioja', 'Mendoza', 'Misiones', 'Neuquén', 'Río Negro', 'Salta',
    'San Juan', 'San Luis', 'Santa Cruz', 'Santa Fe', 'Santiago del Estero', 'Tierra del Fuego', 'Tucumán'
]
n_sucursales = 20
sucursales_data = {
    'sucursal_id': range(1, n_sucursales + 1),
    'nombre_sucursal': [f'Sucursal {chr(65 + i)}' for i in range(n_sucursales)],
    'direccion_sucursal': [fake.address().replace('\n', ', ') for _ in range(n_sucursales)],
    'provincia_sucursal': random.choices(provincias_argentinas, k=n_sucursales)
}
df_sucursales = pd.DataFrame(sucursales_data)

# Introducir errores intencionales para ETL
# Error 1: Nombres de provincia mal escritos
df_sucursales.loc[3, 'provincia_sucursal'] = 'Bunoes Aires'
df_sucursales.loc[7, 'provincia_sucursal'] = 'Cordoba' # sin tilde
df_sucursales.loc[12, 'provincia_sucursal'] = 'Misiones ' # espacio extra
# Error 2: Sucursales sin provincia asignada (NaN)
df_sucursales.loc[15, 'provincia_sucursal'] = np.nan
# Error 3: Alguna dirección mal formada
df_sucursales.loc[5, 'direccion_sucursal'] = 'Calle Falsa 123, Error City'

df_sucursales.to_csv('dim_sucursales.csv', index=False)
print("Generado: dim_sucursales.csv (con errores para ETL)")

# --- 5. Dimensión Canales (dim_canales.csv) ---
canales_data = {
    'canal_id': [1, 2],
    'nombre_canal': ['Online', 'Sucursal Fisica']
}
df_canales = pd.DataFrame(canales_data)
df_canales.to_csv('dim_canales.csv', index=False)
print("Generado: dim_canales.csv")

# --- 6. Tabla de Hechos - Ventas (fact_ventas.csv) ---
# Vamos a generar transacciones diarias.
# El número de transacciones variará por período para reflejar la tendencia.

ventas_list = []
transaction_id = 1

for current_date in dates:
    num_transactions = 0
    
    # Base de transacciones diarias
    if current_date < PANDEMIC_START_DATE:
        num_transactions = int(np.random.normal(50, 10)) # Pre-pandemia: ~50 transacciones/día
    elif current_date < POST_PANDEMIC_START_DATE:
        # Pandemia: Boom de transacciones
        num_transactions = int(np.random.normal(150, 40)) # ~150 transacciones/día
    else:
        num_transactions = int(np.random.normal(80, 20)) # Post-pandemia: se normaliza a ~80

    # Estacionalidad semanal (ej: más ventas los fines de semana)
    if current_date.weekday() in [4, 5]: # Viernes, Sábado
        num_transactions = int(num_transactions * 1.2)
    elif current_date.weekday() == 6: # Domingo
        num_transactions = int(num_transactions * 0.8) # Más Online, menos sucursales

    # Reducir transacciones en periodos de cierre (ej: Abril-Mayo 2020)
    if PANDEMIC_START_DATE <= current_date < PANDEMIC_START_DATE + timedelta(days=90):
        num_transactions = int(num_transactions * 0.5) # Caída brusca en sucursales, online compensa

    # Asegurar que el número de transacciones sea al menos 1
    num_transactions = max(1, num_transactions)
    
    for _ in range(num_transactions):
        cliente_id = random.randint(1, n_clientes)
        producto_id = random.choice(df_productos['producto_id'])
        canal_id = 0 # Temporal
        sucursal_id = np.nan # Temporal
        
        # Lógica para determinar el canal (Online vs Sucursal)
        online_share_daily = 0.15 # Base pre-pandemia
        if current_date >= PANDEMIC_START_DATE:
            if current_date < POST_PANDEMIC_START_DATE:
                # Crecimiento lineal en pandemia para la cuota online
                delta_days = (current_date - PANDEMIC_START_DATE).days
                total_pandemic_days = (POST_PANDEMIC_START_DATE - PANDEMIC_START_DATE).days
                online_share_daily = 0.15 + 0.35 * (delta_days / total_pandemic_days) # Pasa de 15% a 50%
            else:
                online_share_daily = 0.45 + np.random.uniform(-0.05, 0.05) # Se estabiliza en post-pandemia

        if random.random() < online_share_daily:
            canal_id = 1 # Online
            sucursal_id = np.nan # No aplica para ventas online
        else:
            canal_id = 2 # Sucursal Fisica
            sucursal_id = random.randint(1, n_sucursales)

        # Precio unitario base del producto
        precio_unitario = df_productos[df_productos['producto_id'] == producto_id]['precio_unitario_usd'].iloc[0]
        
        # Cantidad vendida (generalmente 1, a veces 2)
        cantidad = random.choice([1, 1, 1, 1, 2])
        
        venta_total = precio_unitario * cantidad * (1 + np.random.uniform(-0.05, 0.05)) # Pequeña variación de precio
        
        ventas_list.append({
            'transaction_id': transaction_id,
            'fecha': current_date,
            'cliente_id': cliente_id,
            'producto_id': producto_id,
            'canal_id': canal_id,
            'sucursal_id': sucursal_id,
            'cantidad': cantidad,
            'monto_venta_usd': round(venta_total, 2)
        })
        transaction_id += 1

df_fact_ventas = pd.DataFrame(ventas_list)
df_fact_ventas.to_csv('fact_ventas.csv', index=False)
print("Generado: fact_ventas.csv")
print(f"Total de {len(df_fact_ventas)} transacciones generadas.")

# --- 7. Dimensión Fecha (dim_fecha.csv) ---
# Esto ya es estándar en muchos modelos de datos
df_fecha = pd.DataFrame({'fecha': dates})
df_fecha['año'] = df_fecha['fecha'].dt.year
df_fecha['mes'] = df_fecha['fecha'].dt.month
df_fecha['dia'] = df_fecha['fecha'].dt.day
df_fecha['nombre_mes'] = df_fecha['fecha'].dt.strftime('%B')
df_fecha['nombre_dia_semana'] = df_fecha['fecha'].dt.strftime('%A')
df_fecha['trimestre'] = df_fecha['fecha'].dt.quarter
df_fecha['semana_del_año'] = df_fecha['fecha'].dt.isocalendar().week.astype(int)
df_fecha.to_csv('dim_fecha.csv', index=False)
print("Generado: dim_fecha.csv")