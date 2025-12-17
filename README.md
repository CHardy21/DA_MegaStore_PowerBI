## Objetivo del Laboratorio

Aplicar los conocimientos de Power BI Desktop para transformar datos crudos, modelar un esquema relacional (estrella/copo de nieve) y crear un panel de control (dashboard) interactivo y profesional que permita la toma de decisiones informadas.

### Requerimientos Técnicos
- Entorno: Power BI
- Repositorio: GitHub (público)

<details>

### Consigna:
Elaborar un informe de Power BI profesional que aborde el análisis de ventas y rendimiento, utilizando los datos proporcionados o autogenerados por el estudiante.


#### 1. Etapa de Extracción, Transformación y Carga (ETL)
- **Fuentes**: Conectar Power BI a un mínimo de 3 fuentes de datos distintas de tu elección.

- **Power Query**: Utilizar el Editor de Power Query para realizar al menos tres transformaciones significativas en los datos (ej. renombrar columnas, cambiar tipos de datos, eliminar errores, combinar/anexar consultas, crear columnas condicionales).

- **Limpieza de Datos**: Asegurar que los datos cargados estén limpios y listos para el modelado (sin valores nulos o inconsistentes en las claves).

#### 2. Modelado de Datos
- **Estructura**: Crear un Modelo de Datos Relacional (esquema Estrella o Copo de Nieve) estableciendo relaciones correctas entre las tablas de Hechos y Dimensiones.

- **Cardinalidad**: Definir la cardinalidad y el filtro cruzado (dirección de la relación) de manera adecuada (ej. 1 a muchos, muchos a uno).

- **Inteligencia de Tiempo (Time Intelligence)**: Crear una Tabla de Calendario (Date Table) separada, marcarla como tal en Power BI, y conectarla a la tabla de Hechos.

#### 3. Medidas DAX y Cálculos
- **Medidas Explícitas**: Crear al menos 3 medidas DAX explícitas esenciales para el análisis.

- **KPIs**: Utilizar estas medidas en los objetos visuales para mostrar Indicadores Clave de Rendimiento (KPIs).

#### 4. Creación del Dashboard (Página de Informe)
    Diseñar una única página de informe (dashboard) que cumpla con los siguientes requisitos visuales y funcionales:

- Visuales Requeridos: Incluir al menos 4 objetos visuales distintos.

- Obligatorio: Un Mapa (de puntos o coroplético) que muestre la distribución de las ventas por Ciudad o País.

- Otros: Gráfico de barras/columnas, gráfico de líneas para tendencia, tarjeta KPI.

- Segmentación: Incluir un Panel de Segmentadores (Slicers) que permita filtrar el informe por al menos dos dimensiones.

- Interactividad: Asegurar que todos los objetos visuales interactúen correctamente al seleccionar filtros o elementos en otros visuales.
</details>

## Autor
Trabajo realizado por **Christian R. Hardy**

**Laboratorio 2. – Módulo de Análisis de Datos**

***Informatorio 2025***



## 🤝 Contribuciones

¡Contribuciones y comentarios son bienvenidos!

---

### Screenshots:


#### Dashboard PowerBI
![Dashboard](/assets/screenshot_powerbi.jpg)

#### Modelo de Datos
![Modelo Estrella](/assets/vista_modelo.png)