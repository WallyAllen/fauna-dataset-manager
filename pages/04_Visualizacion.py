import streamlit as st
import pandas as pd
from src.ui_state import get_current_dataset
from src.lectura import load_dataframe
from src.dataset_config import get_dataset_config

st.set_page_config(
    page_title="Visualización",
    page_icon="📊",
    layout="wide",
)

# 1. Obtener el dataset seleccionado en el sidebar
dataset_name = get_current_dataset()

st.title("📊 Análisis Visual de Biodiversidad")
st.caption(f"Explorando el dataset: **{dataset_name.upper()}**")
st.divider()

# 2. Cargar el DataFrame y su configuración específica
try:
    with st.spinner("Cargando datos..."):
        df = load_dataframe(dataset_name)
        config = get_dataset_config(dataset_name)
except Exception as e:
    st.error(f"Error al cargar el dataset: {e}")
    st.stop()

# 3. Lógica del Ejercicio 3.A
# Identificamos las columnas según el traductor
col_pais = config.get('pais')
col_provincia = config.get('provincia')

# Contamos registros por país para decidir la granularidad del gráfico
# Eliminamos nulos para la lógica de decisión
paises_presentes = df[col_pais].dropna().unique()

if len(paises_presentes) > 1:
    # Caso: Más de un país
    col_a_graficar = col_pais
    titulo_grafico = "Cantidad de registros por País"
    label_slider = "países"
else:
    # Caso: Un solo país (o ninguno declarado, tomamos el primero si existe)
    # Buscamos provincia, si no existe o es None en config, buscamos locality
    if col_provincia and col_provincia in df.columns:
        col_a_graficar = col_provincia
    elif 'locality' in df.columns:
        col_a_graficar = 'locality'
    elif 'verbatimLocality' in df.columns:
        col_a_graficar = 'verbatimLocality'
    else:
        st.warning("No se encontraron columnas de ubicación (provincia/localidad) para este dataset.")
        st.stop()
    
    nombre_pais = paises_presentes[0] if len(paises_presentes) > 0 else "el dataset"
    titulo_grafico = f"Cantidad de registros en {nombre_pais} (por Provincia/Localidad)"
    label_slider = "ubicaciones"

# 4. Renderizado del componente visual
st.subheader(titulo_grafico)

# Calculamos las frecuencias
frecuencias = df[col_a_graficar].value_counts()

if frecuencias.empty:
    st.info("No hay datos suficientes para generar el gráfico.")
else:
    # Slider para elegir cuántos mostrar (N más frecuentes)
    n_total = len(frecuencias)
    n_mostrar = st.slider(
        f"Seleccioná cuántos {label_slider} mostrar",
        min_value=1,
        max_value=min(n_total, 50),
        value=min(n_total, 10),
        help="Muestra los registros con mayor cantidad de apariciones."
    )

    # Filtrar y graficar
    datos_grafico = frecuencias.head(n_mostrar)
    
    # Usamos st.bar_chart para una integración rápida y estética con Streamlit
    st.bar_chart(datos_grafico)

    # Información adicional
    with st.expander("Ver datos tabulares"):
        st.dataframe(datos_grafico, use_container_width=True)
