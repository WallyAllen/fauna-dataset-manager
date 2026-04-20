# Dataset iNaturalist — iNaturalist Research-grade Observations

## Información general

- **Nombre del dataset:** iNaturalist Research-grade Observations

- **Institución proveedora:** iNaturalist

- **Cantidad de registros:** 1.229.599 registros

- **Cobertura geográfica:** Global. Coordenadas que van desde latitud -84.41 hasta 89.99 y longitud prácticamente desde 0 hasta -0.00000017

- **Cobertura temporal:** Desde 17 de septiembre de 1768 hasta 16 de febrero de 2026

- **Separador de campos:** Coma (`,`)

- **Codificación de caracteres (encoding):** UTF-8

- **Tipo de licencia:** Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0). Los registros individuales pueden tener licencias diferentes (CC0, CC BY o CC BY-NC).

- **Frecuencia de actualización:** Semanal

## Archivos del dataset

- **`observations.csv`:** Archivo principal con los registros de observaciones de especies. Contiene 48 columnas con información sobre la ubicación, fecha, especie observada y quién la identificó.

- **`media.csv`:** Archivo con las fotos, videos y audios asociados a las observaciones. Tiene 11 columnas y cada registro está vinculado a una observación del archivo principal.

- **`dna_derived_data.csv`:** Archivo con secuencias de ADN de algunas observaciones. Según la información proporcionada, este archivo es redundante con `media.csv` en esta descarga.

- **`meta.xml`:** Archivo técnico que indica cómo leer los archivos del dataset (separador, encoding, mapeo de columnas).

- **`eml.xml`:** Archivo con la documentación del dataset (institución, propósito, cobertura, licencia).
