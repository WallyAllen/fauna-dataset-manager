import streamlit as st
from src.ui_state import get_current_dataset
from src.lectura import load_dataframe
from src.busquedas import buscar_en_dataframe

st.set_page_config(
    page_title="Búsqueda",
    page_icon=":mag:",
    layout="wide",
)

dataset_name = get_current_dataset()

try:
    df_full = load_dataframe(dataset_name)
except Exception:
    st.warning("No hay datos disponibles. Revisa que hatyas generado los archivos procesados con `generar_processed.py`.")
    st.stop()

st.title("Búsqueda de registros")
st.divider()

# --- Ejercicio 2.A---
st.subheader("Búsqueda por texto libre")

col_texto, col_valor = st.columns([1, 2])
with col_texto:
    col_seleccionada = st.selectbox("Columna", options=df_full.columns.tolist())
with col_valor:
    texto_buscado = st.text_input("Texto a buscar (substring, sin distinción de mayúsculas)")

df = buscar_en_dataframe(
    df_full,
    dataset=dataset_name,
    texto_libre=(col_seleccionada, texto_buscado) if texto_buscado else None,
)

st.markdown(f"**{len(df):,} registros encontrados**")
st.dataframe(df, use_container_width=True, hide_index=True)
