# Dataset Xeno-canto — Bird sounds from around the world

## Información general

- **Nombre del dataset:** Xeno-canto - Bird sounds from around the world

- **Institución proveedora:** Xeno-canto Foundation for Nature Sounds

- **Cantidad de registros:** 13.471 registros

- **Cobertura geográfica:** Global. Coordenadas que van desde latitud -90 hasta 90 y longitud -180 hasta 180

- **Cobertura temporal:** Desde 1900 hasta la actualidad

- **Separador de campos:** Coma (`,`)

- **Codificación de caracteres (encoding):** UTF-8

- **Tipo de licencia:** Creative Commons Attribution Non Commercial 4.0 (CC BY-NC 4.0)

- **Frecuencia de actualización:** No declarada en el EML

## Archivos del dataset

- **`Occurrence.txt`:** Archivo principal con los registros de grabaciones de cantos y sonidos de aves. Contiene 37 columnas con información sobre la especie, ubicación, fecha y características de la grabación.

- **`Multimedia.txt`:** Archivo con los archivos de audio asociados a cada registro. Tiene 16 columnas con información sobre el archivo de sonido (URL, formato, creador, licencia, dispositivo de captura).

- **`meta.xml`:** Archivo técnico que indica cómo leer los archivos del dataset (separador, encoding, mapeo de columnas).

- **`eml.xml`:** Archivo con la documentación del dataset (institución, propósito, cobertura, licencia).



# Ejercicio 1.B — Atributos del Dataset Xeno-canto
 
El archivo principal `Occurrence.txt` tiene 37 columnas. A continuación se describe cada una.

### Identificación del registro
 
- **`id`:** Identificador único del registro en Xeno-canto. Ejemplo: `997656@XC`
- **`occurrenceID`:** URL que identifica la observación. Ejemplo: `https://data.biodiversitydata.nl/xeno-canto/observation/XC997656`
- **`catalogNumber`:** Número de catálogo de la grabación. Ejemplo: `XC997656`
- **`basisOfRecord`:** Tipo de registro. En este dataset todos son `HumanObservation`.
- **`collectionCode`:** Nombre de la colección. En todos los registros es `Wildlife sounds - Birds`.
- **`otherCatalogNumbers`:** Otros identificadores asociados al registro. Puede estar vacío.
### Información técnica de la grabación
 
- **`dynamicProperties`:** Información adicional en formato JSON sobre el equipo usado. Ejemplo: `{"recordingDevice":"Audiornis 014 & Zoom 4Hn","microphone":"Zoom 4Hn"}`
- **`preparations`:** Tipo de preparación del registro. En este dataset es `field recording`.
- **`fieldNotes`:** Notas de campo del grabador con detalles de la observación. Ejemplo: `Espécimen acústico asociado a la publicación...`
### Información taxonómica
 
- **`scientificName`:** Nombre científico de la especie. Ejemplo: `Zonotrichia capensis`
- **`genus`:** Género taxonómico. Ejemplo: `Zonotrichia`
- **`specificEpithet`:** Epíteto específico. Ejemplo: `capensis`
- **`infraspecificEpithet`:** Epíteto infraespecífico (subespecie). Puede estar vacío.
- **`taxonRank`:** Rango taxonómico. Ejemplo: `species`
- **`kingdom`:** Reino taxonómico. En todos los registros es `Animalia`.
- **`family`:** Familia taxonómica. Ejemplo: `Passerellidae`
- **`higherClassification`:** Clasificación taxonómica jerárquica separada por pipes. Ejemplo: `Animalia|PASSERIFORMES|Passerellidae`
- **`nomenclaturalCode`:** Código de nomenclatura utilizado. En este dataset es `ICZN`.
- **`vernacularName`:** Nombre común de la especie. Ejemplo: `Rufous-collared Sparrow`
- **`identificationRemarks`:** Observaciones sobre la identificación. Puede estar vacío.
### Información geográfica
 
- **`longitudeDecimal`:** Longitud en grados decimales. Ejemplo: `-62.4476`
- **`latitudeDecimal`:** Latitud en grados decimales. Ejemplo: `-39.5435`
- **`geodeticDatum`:** Sistema de referencia geodésico. En este dataset es `WGS84`.
- **`country`:** País donde se realizó la grabación (nombre completo, no código ISO). Ejemplo: `Argentina`
- **`locality`:** Localidad de la grabación. Ejemplo: `Refugio de Vida Silvestre Marahué`
- **`verbatimElevation`:** Elevación tal como fue registrada. Ejemplo: `10 m`
### Información del evento
 
- **`recordedBy`:** Nombre de quien realizó la grabación. Ejemplo: `Bernabe Lopez-Lanus`
- **`eventDate`:** Fecha del evento en formato ISO. Ejemplo: `2024-12-24`
- **`eventTime`:** Hora de la grabación. Ejemplo: `11:00`
- **`verbatimEventDate`:** Fecha como fue ingresada originalmente. Ejemplo: `2024-12-24`
### Información del organismo
 
- **`behavior`:** Comportamiento del ave al momento de la grabación. Ejemplo: `song`
- **`sex`:** Sexo del ave. Ejemplo: `undetermined`
- **`lifeStage`:** Etapa de vida del ave. Ejemplo: `adult`
- **`Associated Taxa`:** Taxones asociados al registro. Puede estar vacío.
### Derechos y referencias
 
- **`references`:** URL de referencia del registro. Ejemplo: `https://data.biodiversitydata.nl/xeno-canto/observation/XC997656`
- **`rightsHolder`:** Titular de los derechos de la grabación. Ejemplo: `Bernabe Lopez-Lanus`
- **`license`:** Licencia del registro. Ejemplo: `CC BY-NC`