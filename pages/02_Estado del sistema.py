import streamlit as st
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parents[1] / "logs" / "operations.log"

st.set_page_config(
    page_title="Estado del sistema",
    page_icon=":satellite_antenna:",
    layout="wide",
)

st.title("🛰️ Estado del sistema")
st.caption(f"Lectura del archivo `{LOG_FILE.relative_to(LOG_FILE.parents[1])}`")
st.divider()


def parsear_linea(linea):
    """
    Convierte una línea del log en un dict con las columnas pedidas.
    Formato esperado:
        fecha | dataset | operacion | N registros [| ERROR]
    Retorna None si la línea no respeta el formato.
    """
    partes = [p.strip() for p in linea.strip().split("|")]
    if len(partes) < 4:
        return None

    cantidad_txt = partes[3].replace("registros", "").strip()
    try:
        cantidad = int(cantidad_txt)
    except ValueError:
        cantidad = 0

    return {
        "fecha": partes[0],
        "dataset": partes[1],
        "operación": partes[2],
        "registros": cantidad,
        "estado": partes[4] if len(partes) >= 5 else "OK",
    }


def leer_log(path):
    """Lee operations.log y devuelve una lista de dicts (uno por línea válida)."""
    if not path.exists() or path.stat().st_size == 0:
        return []
    filas = []
    with open(path, encoding="utf-8") as f:
        for linea in f:
            registro = parsear_linea(linea)
            if registro is not None:
                filas.append(registro)
    return filas


col_recargar, _ = st.columns([1, 5])
with col_recargar:
    if st.button("🔄 Recargar log"):
        st.rerun()

filas = leer_log(LOG_FILE)

if not filas:
    st.info("Todavía no hay operaciones registradas en `logs/operations.log`.")
    st.stop()

total_ops = len(filas)
total_errores = sum(1 for f in filas if f["estado"] == "ERROR")
total_afectados = sum(f["registros"] for f in filas)
ultima_fecha = filas[-1]["fecha"]

m1, m2, m3, m4 = st.columns(4)
m1.metric("Operaciones", total_ops)
m2.metric("Con ERROR", total_errores)
m3.metric("Registros afectados (suma)", total_afectados)
m4.metric("Última operación", ultima_fecha)

st.divider()

datasets = sorted({f["dataset"] for f in filas})
operaciones = sorted({f["operación"] for f in filas})
estados = sorted({f["estado"] for f in filas})

f1, f2, f3 = st.columns(3)
with f1:
    sel_datasets = st.multiselect("Filtrar por dataset", datasets, default=datasets)
with f2:
    sel_ops = st.multiselect("Filtrar por operación", operaciones, default=operaciones)
with f3:
    sel_estados = st.multiselect("Filtrar por estado", estados, default=estados)

filas_filtradas = [
    f for f in filas
    if f["dataset"] in sel_datasets
    and f["operación"] in sel_ops
    and f["estado"] in sel_estados
]

st.subheader(f"Operaciones registradas ({len(filas_filtradas)} de {total_ops})")

if not filas_filtradas:
    st.warning("Ninguna operación coincide con los filtros aplicados.")
else:
    st.dataframe(
        list(reversed(filas_filtradas)),
        width="stretch",
        hide_index=True,
        column_config={
            "fecha": st.column_config.TextColumn("Fecha"),
            "dataset": st.column_config.TextColumn("Dataset"),
            "operación": st.column_config.TextColumn("Operación"),
            "registros": st.column_config.NumberColumn("Registros", format="%d"),
            "estado": st.column_config.TextColumn("Estado"),
        },
    )
