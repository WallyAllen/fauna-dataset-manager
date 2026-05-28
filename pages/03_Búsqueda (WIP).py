import streamlit as st
from datetime import date
from src.ui_state import get_current_dataset
from src.lectura import load_dataframe
from src.busquedas import buscar_en_dataframe
from src.dataset_config import get_dataset_config

st.set_page_config(
    page_title="Búsqueda",
    page_icon=":mag:",
    layout="wide",
)

dataset_name = get_current_dataset()

try:
    df_full = load_dataframe(dataset_name)
except Exception:
    st.warning("No hay datos disponibles. Revisa que hayas generado los archivos procesados con `generar_processed.py`.")
    st.stop()

st.title("Búsqueda de registros")
st.divider()

config = get_dataset_config(dataset_name)

# --- Ejercicio 2.A ---
st.subheader("Búsqueda por texto libre")

col_texto, col_valor = st.columns([1, 2])
with col_texto:
    col_seleccionada = st.selectbox("Columna", options=df_full.columns.tolist())
with col_valor:
    texto_buscado = st.text_input("Texto a buscar (substring, sin distinción de mayúsculas)")

# --- Ejercicio 2.B ---
st.subheader("Filtros combinados")

col_sci   = "scientificName" if "scientificName" in df_full.columns else None
col_obs   = config.get("observador")
col_pais  = config.get("pais")
col_prov  = config.get("provincia")
col_fecha_raw = config.get("fecha")
col_fecha = col_fecha_raw[0] if isinstance(col_fecha_raw, list) else col_fecha_raw


def _opciones(col):
    """Devuelve valores únicos no nulos de una columna, o lista vacía si no existe."""
    if not col or col not in df_full.columns:
        return []
    return sorted(df_full[col].dropna().unique().tolist())


c1, c2 = st.columns(2)
with c1:
    sel_sci  = st.multiselect("Nombre científico", _opciones(col_sci),
                               disabled=not col_sci)
    sel_pais = st.multiselect("País",              _opciones(col_pais),
                               disabled=not col_pais)
    sel_prov = st.multiselect("Provincia",         _opciones(col_prov),
                               disabled=not (col_prov and col_prov in df_full.columns))

with c2:
    obs_deshabilitado = not (col_obs and col_obs in df_full.columns)
    txt_obs = st.text_input("Observador (substring)", disabled=obs_deshabilitado)

    rango_disp = bool(col_fecha and col_fecha in df_full.columns)
    if rango_disp:
        fecha_desde = st.date_input("Fecha desde", value=date(2000, 1, 1), key="fecha_desde")
        fecha_hasta = st.date_input("Fecha hasta", value=date.today(),      key="fecha_hasta")
    else:
        st.info("Este dataset no tiene columna de fecha disponible.")
        fecha_desde = fecha_hasta = None

# --- Aplicar todos los filtros vía buscar_en_dataframe ---
filtros_isin = {}
if sel_sci:                      filtros_isin[col_sci]  = sel_sci
if sel_pais:                     filtros_isin[col_pais] = sel_pais
if sel_prov and col_prov:        filtros_isin[col_prov] = sel_prov

filtros_substring = {}
if txt_obs and col_obs:          filtros_substring[col_obs] = txt_obs

df = buscar_en_dataframe(
    df_full,
    dataset=dataset_name,
    texto_libre=(col_seleccionada, texto_buscado) if texto_buscado else None,
    isin=filtros_isin or None,
    substring=filtros_substring or None,
    rango_fecha=(col_fecha, fecha_desde, fecha_hasta) if rango_disp else None,
)

# --- Ejercicio 2.C ---
# Columnas a mostrar: ID + nombre científico + ubicación (país/provincia) +
# observador + fecha primaria + nivel taxonómico (taxonRank, family, genus).
# Se excluyen coordenadas (reservadas para el mapa en P4) y taxonomía alta
# (kingdom, phylum, class, order) que no aportan valor en una búsqueda puntual.
_CANDIDATE_DISPLAY = [
    config['id'],
    'scientificName',
    col_pais,
    col_prov,
    col_obs,
    col_fecha,
    'taxonRank',
    'family',
    'genus',
]
display_cols = [c for c in _CANDIDATE_DISPLAY if c and c in df.columns]

st.markdown(f"**{len(df):,} registros encontrados**")

PAGE_SIZE = 50
page_key  = f"busqueda_pagina_{dataset_name}"
total_key = f"busqueda_total_{dataset_name}"

if page_key not in st.session_state:
    st.session_state[page_key] = 0

# Volver a la primera página cuando cambian los resultados del filtro
if st.session_state.get(total_key) != len(df):
    st.session_state[page_key] = 0
    st.session_state[total_key] = len(df)

pagina        = st.session_state[page_key]
total_paginas = max(1, (len(df) + PAGE_SIZE - 1) // PAGE_SIZE)
inicio        = pagina * PAGE_SIZE
fin           = inicio + PAGE_SIZE

bc1, bc2, bc3 = st.columns([1, 4, 1])
with bc1:
    if st.button("← Anterior", disabled=(pagina == 0)):
        st.session_state[page_key] -= 1
        st.rerun()
with bc2:
    st.caption(f"Página {pagina + 1} de {total_paginas}")
with bc3:
    if st.button("Siguiente →", disabled=(pagina >= total_paginas - 1)):
        st.session_state[page_key] += 1
        st.rerun()

st.dataframe(
    df[display_cols].iloc[inicio:fin].reset_index(drop=True),
    use_container_width=True,
    hide_index=True,
)
