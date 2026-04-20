# Dataset IADIZA — Colección Ornitológica del IADIZA-CCT CONICET Mendoza

## Información general

- **Nombre del dataset:** Colección Ornitológica del IADIZA-CCT CONICET Mendoza: IADIZA-COI

- **Institución proveedora:** IADIZA – CCT CONICET Mendoza

- **Cantidad de registros:** 2.370 registros (el EML declara 2.365)

- **Cobertura geográfica:** Principalmente localidades de Argentina y algunos países limítrofes. Coordenadas que van desde latitud -46.02 hasta -22.25 y longitud -71.647 hasta -53.735

- **Cobertura temporal:** No declarada en el EML

- **Separador de campos:** Tabulador (`\t`)

- **Codificación de caracteres (encoding):** UTF-8

- **Tipo de licencia:** Creative Commons Attribution Non Commercial 4.0 (CC BY-NC 4.0)

- **Frecuencia de actualización:** Sin actualización programada

## Archivos del dataset

- **`occurrence.txt`:** Archivo principal con los registros de avistamientos de aves. Contiene 230 columnas con información sobre las especies observadas.

- **`verbatim.txt`:** Versión sin procesar de los registros, tal como fueron enviados originalmente por la institución.

- **`multimedia.txt`:** Archivo para fotos, videos y audios asociados a los registros. En esta descarga está vacío (solo tiene el encabezado).

- **`meta.xml`:** Archivo técnico que indica cómo leer los archivos del dataset (separador, encoding, mapeo de columnas).

- **`metadata.xml`:** Archivo con información de la descarga realizada.

- **`a0d072fc-e6be-45d7-9fa8-afa4b38b788a.xml`:** Archivo con la documentación del dataset original (título, autores, institución, cobertura, licencia).

- **`rights.txt`:** Archivo con información sobre la licencia del dataset.

- **`citations.txt`:** Archivo con la cita bibliográfica recomendada para usar en publicaciones.



# Ejercicio 1.B — Atributos del Dataset IADIZA
 
El archivo principal `occurrence.txt` tiene 230 columnas. Muchas (177) de las columnas restantes están completamente vacías en este dataset, 36 columnas están completas, mientras que solo 17 están parcialmente completas.A continuación se describen las más relevantes del archivo para el trabajo.
 
### Identificación del registro
 
- **`gbifID`:** Identificador único asignado por GBIF a cada registro. Ejemplo: `1660907957`
- **`occurrenceID`:** Identificador original del registro según la institución. Ejemplo: `IADIZA:COI:006287`
- **`catalogNumber`:** Número de catálogo del espécimen en la colección. Ejemplo: `006287`
- **`basisOfRecord`:** Tipo de registro, indica cómo se obtuvo el dato. En este dataset todos son `PRESERVED_SPECIMEN` (espécimen preservado en la colección).
### Información institucional
 
- **`institutionCode`:** Código de la institución que posee el registro. En todos los registros es `IADIZA`.
- **`collectionCode`:** Código de la colección dentro de la institución. En todos los registros es `COI`.
### Información del evento
 
- **`recordedBy`:** Nombre de quien recolectó el espécimen. Ejemplo: `Ana Fernández`
- **`eventDate`:** Fecha del evento de recolección. Vacío en todos los registros.
- **`year`:** Año del evento. Vacío en todos los registros.
### Información geográfica
 
- **`countryCode`:** Código ISO del país donde se recolectó. Ejemplo: `AR`
- **`stateProvince`:** Provincia o estado. Ejemplo: `Mendoza`
- **`locality`:** Descripción textual de la localidad. Ejemplo: `La Primavera`
- **`decimalLatitude`:** Latitud en grados decimales. Vacío en todos los registros.
- **`decimalLongitude`:** Longitud en grados decimales. Vacío en todos los registros.
### Información taxonómica
 
- **`scientificName`:** Nombre científico completo con autor. Ejemplo: `Troglodytes aedon Vieillot, 1809`
- **`kingdom`:** Reino taxonómico. En todos los registros es `Animalia`.
- **`phylum`:** Filo taxonómico. En todos los registros es `Chordata`.
- **`class`:** Clase taxonómica. En todos los registros es `Aves`.
- **`order`:** Orden taxonómico. Ejemplo: `Passeriformes`
- **`family`:** Familia taxonómica. Ejemplo: `Troglodytidae`
- **`genus`:** Género taxonómico. Ejemplo: `Troglodytes`
- **`specificEpithet`:** Epíteto específico, es decir la segunda parte del nombre científico. Ejemplo: `aedon`
- **`taxonRank`:** Rango taxonómico del registro. Ejemplo: `SPECIES`
### Campos vacíos relevantes
 
- **`sex`:** Sexo del organismo. Vacío en todos los registros.
- **`lifeStage`:** Etapa de vida del organismo. Vacío en todos los registros.
- **`vernacularName`:** Nombre común de la especie. Vacío en todos los registros.
 