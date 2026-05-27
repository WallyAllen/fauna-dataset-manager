import streamlit as st
from src.dataset_config import TRADUCTOR_DATASETS

ACTIVE_DATASET_SESSION_KEY = "dataset_activo"


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

    current_dataset = st.session_state[ACTIVE_DATASET_SESSION_KEY]
    if current_dataset not in datasets:
        current_dataset = datasets[0]
        st.session_state[ACTIVE_DATASET_SESSION_KEY] = current_dataset

    selected_dataset = st.sidebar.selectbox(
        "Dataset activo",
        options=datasets,
        index=datasets.index(current_dataset),
        key="sidebar_dataset_selector",
    )
    st.session_state[ACTIVE_DATASET_SESSION_KEY] = selected_dataset

    return selected_dataset