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



# Ejercicio 1.B — Atributos del Dataset iNaturalist
 
El archivo principal `observations.csv` tiene 48 columnas. A continuación se describe cada una.
 

### Identificación del registro
 
- **`id`:** Identificador único de la observación. Ejemplo: `42369866`
- **`occurrenceID`:** URL que identifica la observación en iNaturalist. Ejemplo: `https://www.inaturalist.org/observations/42369866`
- **`basisOfRecord`:** Tipo de registro. En este dataset todos son `HumanObservation`.
- **`modified`:** Fecha y hora de la última modificación del registro. Ejemplo: `2020-10-27T19:46:33Z`
- **`catalogNumber`:** Número de catálogo, coincide con el `id`. Ejemplo: `42369866`
- **`references`:** URL de referencia de la observación. Ejemplo: `https://www.inaturalist.org/observations/42369866`
- **`occurrenceRemarks`:** Observaciones sobre el registro. Puede estar vacío.
### Información institucional
 
- **`institutionCode`:** Código de la institución que publica el dato. En todos los registros es `iNaturalist`.
- **`collectionCode`:** Código de la colección. En todos los registros es `Observations`.
- **`datasetName`:** Nombre del dataset de origen. En todos los registros es `iNaturalist research-grade observations`.
- **`informationWithheld`:** Información que se ocultó por privacidad. Puede estar vacío.
### Información del observador
 
- **`recordedBy`:** Nombre del observador. Ejemplo: `Pablo H Capovilla`
- **`recordedByID`:** Identificador del observador. Puede estar vacío.
- **`identifiedBy`:** Nombre de quien identificó la especie. Ejemplo: `Pablo H Capovilla`
- **`identifiedByID`:** Identificador de quien identificó. Puede estar vacío.
- **`inaturalistLogin`:** Nombre de usuario en iNaturalist. Ejemplo: `pablohcapovilla`
### Información del evento
 
- **`eventDate`:** Fecha y hora de la observación. Ejemplo: `2018-03-31T08:09:00-03:00`
- **`eventTime`:** Hora del evento. Ejemplo: `08:09:00-03:00`
- **`verbatimEventDate`:** Fecha como fue ingresada originalmente por el observador. Ejemplo: `2018/03/31 8:09 AM -0300`
### Información geográfica
 
- **`verbatimLocality`:** Localidad como fue ingresada por el observador. Ejemplo: `Gral Obligado, Santa Fe, Argentina`
- **`decimalLatitude`:** Latitud en grados decimales. Ejemplo: `-28.5015951692`
- **`decimalLongitude`:** Longitud en grados decimales. Ejemplo: `-59.2650295264`
- **`coordinateUncertaintyInMeters`:** Incertidumbre de la coordenada en metros. Ejemplo: `15`
- **`geodeticDatum`:** Sistema de referencia geodésico. En este dataset es `EPSG:4326`.
- **`countryCode`:** Código ISO del país. Ejemplo: `AR`
- **`stateProvince`:** Provincia o estado. Ejemplo: `Santa Fe`
### Información taxonómica
 
- **`scientificName`:** Nombre científico de la especie. Ejemplo: `Thamnophilus doliatus`
- **`taxonID`:** Identificador del taxón. Ejemplo: `15764`
- **`taxonRank`:** Rango taxonómico. Ejemplo: `species`
- **`kingdom`:** Reino taxonómico. Ejemplo: `Animalia`
- **`phylum`:** Filo taxonómico. Ejemplo: `Chordata`
- **`class`:** Clase taxonómica. Ejemplo: `Aves`
- **`order`:** Orden taxonómico. Ejemplo: `Passeriformes`
- **`family`:** Familia taxonómica. Ejemplo: `Thamnophilidae`
- **`genus`:** Género taxonómico. Ejemplo: `Thamnophilus`
### Identificación
 
- **`identificationID`:** Identificador de la identificación taxonómica. Ejemplo: `95899387`
- **`dateIdentified`:** Fecha de la identificación. Ejemplo: `2020-04-17T04:09:14Z`
- **`identificationRemarks`:** Observaciones sobre la identificación. Puede estar vacío.
### Información del organismo
 
- **`captive`:** Indica si el organismo era salvaje o cautivo/cultivado. Ejemplo: `wild`
- **`sex`:** Sexo del organismo. Ejemplo: `male`
- **`lifeStage`:** Etapa de vida del organismo. Ejemplo: `adult`
- **`reproductiveCondition`:** Condición reproductiva. Puede estar vacío.
- **`vitality`:** Vitalidad del organismo al momento de la observación. Ejemplo: `alive`
- **`dynamicProperties`:** Propiedades adicionales en formato JSON. Puede estar vacío.
### Derechos y publicación
 
- **`license`:** Licencia del registro. Ejemplo: `https://creativecommons.org/licenses/by/4.0/`
- **`rightsHolder`:** Titular de los derechos. Ejemplo: `Pablo H Capovilla`
- **`publishingCountry`:** País desde donde se publicó la observación. Ejemplo: `AR`
- **`projectId`:** ID del proyecto de iNaturalist al que pertenece. Puede estar vacío.
