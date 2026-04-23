import streamlit as st

st.set_page_config(
    page_title = "PLACEHOLDER",
    page_icon = ":herb:",
    layout = "wide"
)

st.title("🌿 PLACEHOLDER", text_alignment="center")
st.divider()

main_col, instructions_col = st.columns([2, 2])

with main_col:
    st.header("🎯 ¿Qué hace PLACEHOLDER?", divider=True)
    st.write(""" 
        Esta plataforma tiene como propósito centralizar, analizar y visualizar información relacionada 
        con el avistamiento de especies del reino animal y vegetal en Argentina. A través de un procesamiento 
        de conjuntos de datos estandarizados, la aplicación permite realizar controles de calidad espacial y 
        temporal, sanitizar registros biológicos, y generar nuevas vistas de información listas para el análisis 
        estadístico. 
        """)

    st.header("🧬 Acerca de Darwin Core", divider=True)
    st.write(""" 
        El análisis estructurado de datos de biodiversidad es fundamental para comprender los ecosistemas y monitorear 
        los cambios en la distribución de especies. Al limpiar y unificar millones de registros provenientes de diversas 
        instituciones científicas, podemos transformar observaciones aisladas en evidencia sólida. Esto permite a 
        investigadores y organizaciones identificar patrones de migración, evaluar el impacto del cambio climático, 
        gestionar esfuerzos de conservación y desarrollar políticas públicas basadas en información confiable y 
        accesible globalmente.
        """)

with instructions_col:
    st.header("📖 Instrucciones")
    st.info("""
    **Instrucciones de navegación:**
    Para interactuar con la plataforma, utilizá el menú lateral (sidebar) ubicado en la parte izquierda de la pantalla.
    Desde ahí podés alternar entre los distintos módulos funcionales de la aplicación haciendo clic en el nombre de cada página.

    **Información disponible para consulta:** 
    El sistema se divide en cuatro módulos principales:
    * **(P1) Inicio:** Información general sobre la plataforma y el estándar Darwin Core.
    * **(P2) Estado del sistema:** Visualización tabular del historial de operaciones realizadas sobre los conjuntos de datos. 
    Permite auditar las modificaciones detallando la fecha, el dataset afectado, el tipo de operación (inserción, actualización o eliminación) 
    y la cantidad de registros involucrados.
    * **(P3) Búsqueda:** Módulo de consulta interactiva que permite filtrar los registros biológicos utilizando múltiples criterios simultáneos, 
    como el identificador único (occurrenceID), el nombre científico (scientificName) o el país de origen.
    * **(P4) Visualización:** Sección dedicada al análisis gráfico de la información de biodiversidad procesada, facilitando la interpretación 
    de los datos a través de representaciones visuales.
    """, icon='📑')