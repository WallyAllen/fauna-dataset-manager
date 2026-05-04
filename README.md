<div align="center">
  <img src="icon.png" alt="Darwinite Logo" width="128"/>
</div>

# **Darwinite - Procesamiento de Datasets Darwin Core**

Este proyecto provee herramientas de Python para interactuar, validar, buscar, insertar y eliminar registros de datasets biológicos bajo el estándar Darwin Core (DwC). Está configurado específicamente para trabajar con los datasets de la **Colección Ornitológica del IADIZA-CCT**, **iNaturalist** y **Xeno-canto**.

## **Integrantes del Equipo**

- **Josías Emanuel Segovia**
- **Felipe Joaquín Borrazas**
- **Joaquín Meza**
- **Rocco Milito**
- **Valentino Perazzo**

---

## **Requisitos y Configuración Inicial**

El proyecto hace uso de bibliotecas estándar de Python, pero requiere dependencias externas para funciones específicas de validación geográfica y ejecución de libretas interactivas.

### **Instalación de dependencias**

Para instalar las dependencias, abrí tu terminal en la raíz del proyecto (la carpeta `code/`) y ejecuta el siguiente comando:

```bash
pip install pycountry jupyter streamlit
```

_Las bibliotecas requeridas actualmente son:_

- **`pycountry`**: Para validaciones robustas de los códigos de países (ISO 3166-1 alpha-2).
- **`jupyter`**: Para la ejecución interactiva de los Notebooks (`.ipynb`).
- **`streamlit`**: Para ejecutar la aplicación web y visualización de datos.

---

## **Estructura del Proyecto**

- `src/`: Contiene el código fuente y lógica principal del sistema.
  - `lectura.py`, `validaciones.py`, `insercion.py`, `busquedas.py`, `eliminaciones.py`, `log_operaciones.py`.
- `notebooks/`: Jupyter Notebooks utilizados como interfaz de usuario para interactuar paso a paso con los módulos.
- `raw_datasets/`: Archivos originales en formato crudo (.txt, .csv) de los datasets biológicos.
- `processed_datasets/`: Directorio destino donde se guardan los archivos resultantes tras realizar operaciones de inserción o depuración.

---

## **Instrucciones de Ejecución**

Las operaciones principales están organizadas de forma visual y secuencial en Jupyter Notebooks para facilitar el control de los datos.
Se recomienda ejecutar los notebooks en el orden de los ejercicios, oséase:

`Lectura → validación → inserción → actualización → eliminación → logging.`

1. Abrí tu terminal en la carpeta principal del proyecto (`code/`).
2. Iniciá el servidor de Jupyter ejecutando:
   ```bash
   jupyter notebook
   ```
3. En tu navegador, navegá hasta la carpeta `notebooks/`.
4. Abrí el notebook que corresponda a la tarea que deseás realizar.
5. Ejecutá las celdas secuencialmente de arriba hacia abajo presionando `Shift + Enter`.
6. Si alguna de las celdas solicita entrada por teclado, la consola interactiva de la celda aparecerá debajo de ella esperando tus datos.
