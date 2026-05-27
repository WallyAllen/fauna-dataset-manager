import streamlit as st
from src.dataset_config import TRADUCTOR_DATASETS
from src.log_operaciones import current_date
from src.lectura import load_dataframe

ACTIVE_DATASET_SESSION_KEY = "dataset_activo"
SELECTION_TIME_KEY = "fecha_seleccion"

def handle_selection_change():
    """
    Función callback para ejecutar al cambiar el selectbox
    """
    st.session_state[SELECTION_TIME_KEY] = current_date()

def get_current_dataset():
    """
    Renderiza el selector de datasets en el sidebar y persiste la elección
    en el st.session_state, para que se comparta en las distintas páginas
    """
    datasets = sorted(TRADUCTOR_DATASETS.keys())
    if not datasets:
        raise ValueError("No hay datasets en TRADUCTOR_DATASETS.")

    if ACTIVE_DATASET_SESSION_KEY not in st.session_state:
        st.session_state[ACTIVE_DATASET_SESSION_KEY] = datasets[0]
        st.session_state[SELECTION_TIME_KEY] = current_date()

    current_dataset = st.session_state[ACTIVE_DATASET_SESSION_KEY]
    if current_dataset not in datasets:
        current_dataset = datasets[0]
        st.session_state[ACTIVE_DATASET_SESSION_KEY] = current_dataset

    with st.sidebar:
        selected_dataset = st.selectbox(
        "Seleccioná un dataset",
        options=datasets,
        index=datasets.index(current_dataset),
        key="sidebar_dataset_selector",
        on_change=handle_selection_change
    )

        st.session_state[ACTIVE_DATASET_SESSION_KEY] = selected_dataset

        # NOTA: PReguntar si es necesario hacer display, porque ya está en el selectbox

        st.info(f'**DATASET ACTUAL:** {selected_dataset}')

        # PENDIENTE: Ejercicio 1.C, parte 2. Cantidad de registros del dataset.
        # NO tenemos archivos en processed_datasets/ como para llegar a esto. 

        st.caption(f'Seleccionado el {st.session_state[SELECTION_TIME_KEY]}')

    return selected_dataset