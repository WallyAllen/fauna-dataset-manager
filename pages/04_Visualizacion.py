import streamlit as st
import pandas as pd
from src.ui_state import get_current_dataset
from src.lectura import load_dataframe, get_null_percentage
from src.dataset_config import get_dataset_config, get_dataset_filepath
import altair as alt

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

# ---------------------------------------------------------
# Ejercicio 3.A: Gráfico de Barras (País / Provincia)
# ---------------------------------------------------------
st.header("📍 Distribución Geográfica")

col_pais = config.get('pais')
col_provincia = config.get('provincia')

paises_presentes = df[col_pais].dropna().unique()

if len(paises_presentes) > 1:
    col_a_graficar_geo = col_pais
    titulo_geo = "Cantidad de registros por País"
    label_slider_geo = "países"
else:
    if col_provincia and col_provincia in df.columns:
        col_a_graficar_geo = col_provincia
    elif 'locality' in df.columns:
        col_a_graficar_geo = 'locality'
    elif 'verbatimLocality' in df.columns:
        col_a_graficar_geo = 'verbatimLocality'
    else:
        col_a_graficar_geo = None
    
    nombre_pais = paises_presentes[0] if len(paises_presentes) > 0 else "el dataset"
    titulo_geo = f"Cantidad de registros en {nombre_pais} (por Provincia/Localidad)"
    label_slider_geo = "ubicaciones"

if col_a_graficar_geo:
    st.subheader(titulo_geo)
    frecuencias_geo = df[col_a_graficar_geo].value_counts()
    
    if not frecuencias_geo.empty:
        n_mostrar_geo = st.slider(
            f"Seleccioná cuántos {label_slider_geo} mostrar",
            min_value=1,
            max_value=min(len(frecuencias_geo), 50),
            value=min(len(frecuencias_geo), 10),
            key="slider_3a"
        )
        st.bar_chart(frecuencias_geo.head(n_mostrar_geo))
    else:
        st.info("No hay datos de ubicación para graficar.")
else:
    st.warning("No se encontraron columnas de ubicación compatibles.")

st.divider()

# ---------------------------------------------------------
# Ejercicio 3.B: Gráfico de Líneas (Evolución Temporal)
# ---------------------------------------------------------
st.header("📅 Evolución Temporal")

col_fecha = 'eventDate'

if col_fecha in df.columns:
    st.subheader("Cantidad de registros por Año")
    
    fechas_limpias = pd.to_datetime(df[col_fecha], errors='coerce')
    registros_excluidos = fechas_limpias.isna().sum()
    anios = fechas_limpias.dropna().dt.year.astype(int)
    
    if not anios.empty:
        conteo_por_anio = anios.value_counts().sort_index()
        
        if registros_excluidos > 0:
            st.warning(f"⚠️ Se excluyeron **{registros_excluidos}** registros debido a fechas nulas o formatos inconsistentes.")
        else:
            st.success("✅ Todos los registros tienen fechas válidas.")

        st.line_chart(conteo_por_anio)
        
        with st.expander("Ver detalle por año"):
            st.table(conteo_por_anio.rename("Cantidad de Registros").rename_axis("Año"))
    else:
        st.info("No hay registros con fechas válidas para mostrar la evolución temporal.")
else:
    st.error(f"La columna '{col_fecha}' no existe en este dataset.")

st.divider()

# ---------------------------------------------------------
# Ejercicio 3.C: Distribución Taxonómica
# ---------------------------------------------------------
st.header("🧬 Análisis Taxonómico")

# Opciones de nivel taxonómico según la consigna
opciones_taxo = {
    "Clase": "class",
    "Orden": "order",
    "Familia": "family"
}

st.subheader("Distribución por nivel taxonómico")

# Selector para que el usuario elija el nivel (Requisito 3.C)
nivel_seleccionado = st.selectbox(
    "Seleccioná el nivel taxonómico a visualizar",
    options=list(opciones_taxo.keys()),
    index=0,
    help="Elige qué nivel de la jerarquía taxonómica quieres analizar."
)

# Obtenemos el nombre real de la columna en el DataFrame
col_taxo = opciones_taxo[nivel_seleccionado]

if col_taxo in df.columns:
    # Calculamos frecuencias ignorando nulos
    frecuencias_taxo = df[col_taxo].value_counts()
    
    if not frecuencias_taxo.empty:
        # Mostramos un slider para no saturar el gráfico si hay muchos géneros/familias
        n_mostrar_taxo = st.slider(
            f"Mostrar los {nivel_seleccionado.lower()} más frecuentes",
            min_value=1,
            max_value=min(len(frecuencias_taxo), 30),
            value=min(len(frecuencias_taxo), 10),
            key="slider_3c"
        )
        
        # Graficamos
        st.bar_chart(frecuencias_taxo.head(n_mostrar_taxo))
        
        with st.expander(f"Ver lista completa de {nivel_seleccionado}"):
            st.dataframe(frecuencias_taxo, use_container_width=True)
    else:
        st.info(f"No hay datos disponibles para el nivel: {nivel_seleccionado}.")
else:
    st.error(f"La columna '{col_taxo}' no fue encontrada en este dataset.")

st.divider()

# ---------------------------------------------------------
# Ejercicio 3.D: Completitud de los Datos
# ---------------------------------------------------------
st.header("📊 Calidad de Datos (Completitud)")

with st.spinner("Analizando completitud..."):
    # Obtenemos la ruta del archivo y configuración
    filepath = get_dataset_filepath(dataset_name)
    encoding = config.get('encoding', 'utf-8')
    delimiter = config.get('delimitador', ',')
    
    # Reutilizamos la función del Ejercicio 2.F (Requisito 3.D)
    dict_nulos = get_null_percentage(filepath, encoding=encoding, delimiter=delimiter)
    
    # Convertimos a completitud (100 - nulos)
    dict_completitud = {col: 100 - val for col, val in dict_nulos.items()}
    
    # Creamos DataFrame para graficar
    df_comp = pd.DataFrame(list(dict_completitud.items()), columns=['Columna', 'Porcentaje'])
    df_comp = df_comp.sort_values(by='Porcentaje', ascending=False)

if not df_comp.empty:
    st.subheader("Porcentaje de registros no nulos por columna")
    
    # Usamos Altair para gráfico de barras horizontales (Requisito 3.D)
    chart = alt.Chart(df_comp).mark_bar().encode(
        x=alt.X('Porcentaje:Q', title='Completitud (%)', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Columna:N', sort='-x', title='Columna'),
        color=alt.Color('Porcentaje:Q', scale=alt.Scale(scheme='greens'), legend=None),
        tooltip=['Columna', 'Porcentaje']
    ).properties(
        width='container',
        height=max(300, len(df_comp) * 20)  # Ajuste dinámico de altura según cantidad de columnas
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    with st.expander("Ver tabla de completitud"):
        st.dataframe(
            df_comp.rename(columns={'Porcentaje': '% Completitud'}), 
            use_container_width=True, 
            hide_index=True
        )
else:
    st.info("No se pudo calcular la completitud de las columnas.")

st.divider()
