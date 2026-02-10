# Diccionario de Datos - Dataset Maestro de Vital Statistics Guatemala

Documentación de las 95 columnas del dataset consolidado (2009-2022). Agrupadas por categoría temática para facilitar navegación.

## 1. Identificadores y Metadata (2)

| Columna | Descripción |
|---------|-------------|
| `año` | Año del evento |
| `tipo` | Tipo de evento (nacimientos / defunciones / matrimonios / divorcios / defunciones_fetales) |

## 2. Información de Registro (5)

Datos sobre **dónde y cuándo** se registró el evento ante el INE.

| Columna | Descripción |
|---------|-------------|
| `depreg` | Código departamento de registro |
| `mupreg` | Código municipio de registro |
| `mesreg` | Mes de registro |
| `añoreg` | Año de registro |
| `clauni` | Clase de unidad (tipo de unidad de registro) |

## 3. Información de Ocurrencia (6)

Datos sobre **dónde y cuándo** ocurrió realmente el evento (puede diferir del registro).

| Columna | Descripción |
|---------|-------------|
| `depocu` | Código departamento de ocurrencia |
| `mupocu` | Código municipio de ocurrencia |
| `diaocu` | Día de ocurrencia |
| `mesocu` | Mes de ocurrencia |
| `añoocu` | Año de ocurrencia |
| `areagocu` | Área geográfica de ocurrencia |

## 4. Características Demográficas Básicas (7)

Información demográfica de la persona principal del evento.

| Columna | Descripción |
|---------|-------------|
| `sexo` | Sexo (1=Hombre, 2=Mujer) |
| `edadif` | Edad en años (defunciones / infantil) |
| `edadm` | Edad madre |
| `edadhom` | Edad hombre (matrimonios) |
| `edadmuj` | Edad mujer (matrimonios) |
| `edadp` | Edad de la persona (nacimientos / general) |
| `grupetma` | Grupo etario / clasificación por edades |

## 5. Nacionalidad y Residencia (11)

Información sobre origen, residencia y nacionalidad de padres/cónyuges.

| Columna | Descripción |
|---------|-------------|
| `nacionm` | Nacionalidad madre |
| `paisrem` | País de residencia madre |
| `deprem` | Código departamento residencia madre |
| `muprem` | Código municipio residencia madre |
| `paisnacm` | País nacionalidad madre |
| `depnam` | Departamento nacionalidad madre |
| `mupnam` | Municipio nacionalidad madre |
| `naciom` | Nacionalidad hombre (padre) |
| `paisnacp` | País nacionalidad padre |
| `depnap` | Departamento nacionalidad padre |
| `munpnap` | Municipio nacionalidad padre |
| `naciop` | Nacionalidad padre (campo alterno) |

## 6. Educación y Ocupación (7)

Información socioeconómica de padres/cónyuges.

| Columna | Descripción |
|---------|-------------|
| `escolam` | Escolaridad madre |
| `escolap` | Escolaridad padre |
| `escmuj` | Escolaridad mujer |
| `eschom` | Escolaridad hombre (nivel educativo del hombre) |
| `ocupam` | Ocupación madre |
| `ocupap` | Ocupación padre |
| `ocupap` | Ocupación padre |
| `ocuhom` | Ocupación hombre |
| `ocumuj` | Ocupación mujer |
| `ocudif` | Código/indicador de ocupación en registros de defunción |

## 7. Características Etnográficas/Culturales (9)

Información sobre pueblo/etnia y estado civil.

| Columna | Descripción |
|---------|-------------|
| `pueblopm` | Pueblo/etnia madre |
| `pueblopp` | Pueblo/etnia padre |
| `puehom` | Pueblo/etnia hombre |
| `puemuj` | Pueblo/etnia mujer |
| `puedif` | Pueblo/etnia en registro de defunción |
| `gretnm` | Grupo étnico / registro madre |
| `gretnp` | Grupo étnico padre |
| `gethom` | Grupo étnico hombre |
| `getmuj` | Grupo étnico mujer |
| `ppermuj` | Indicador de pertenencia étnica / permiso (madre) |
| `pperhom` | Indicador de pertenencia étnica / permiso (hombre) |
| `escivm` | Estado civil madre |
| `escivp` | Estado civil padre |
| `ecidif` | Estado civil en registro de defunción |

## 8. Información de Defunción (16)

Variables específicas para registros de defunción.

| Columna | Descripción |
|---------|-------------|
| `caudef` | Causa de defunción (código CIE-10 u otra codificación) |
| `cerdef` | Certificado de defunción (código/tipo) |
| `asist` | Asistencia médica (tipo/proveedor) |
| `asisrec` | Registro de asistencia recibida (detalle) |
| `sitioocu` | Sitio de ocurrencia (lugar físico del evento) |
| `mredif` | Código de registro/municipio relacionado a defunción |
| `mnadif` | Código municipio asociado a defunción |
| `dnadif` | Día asociado a defunción / indicador temporal |
| `pnadif` | Código provincia/país en registro de defunción |
| `nacdif` | Nacionalidad en registro de defunción |
| `predif` | Prediagnóstico o código previo en defunción |
| `dredif` | Departamento/registro de defunción (detalle) |
| `escodif` | Escolaridad en registro de defunción |
| `perdif` | Periodicidad/periodo clasificador (defunciones) |
| `ciuodif` | Ciudad de defunción (código) |
| `tohivi` | Tipo/clasificación de homicidio/violencia (codificado) |
| `tohinm` | Indicador de homicidio/índice masculino |
| `tohite` | Indicador de homicidio/índice temporal |

## 9. Características del Nacimiento (6)

Variables específicas para registros de nacimientos.

| Columna | Descripción |
|---------|-------------|
| `libras` | Peso al nacer — libras |
| `onzas` | Peso al nacer — onzas |
| `semges` | Semanas de gestación (nacimientos) |
| `viapar` | Vía de parto (canal de parto) |
| `clapar` | Clase de parto (normal/cesárea) |
| `tipar` | Tipo de parto (clasificación) |

## 10. Información de Padres/Cónyuges (6)

Identificadores y códigos específicos de registros de padre/madre/cónyuge.

| Columna | Descripción |
|---------|-------------|
| `nunuho` | Identificador único hombre (registro) |
| `nunumu` | Identificador único mujer (registro) |
| `ciuomad` | Código ciudad (madre) |
| `ciuohom` | Ciudad de ocurrencia (hombre) |
| `ciuomuj` | Ciudad de ocurrencia (mujer) |
| `muprep` | Código municipio de registro (padre/madre) |
| `paisrep` | País del reporte/registro |
| `deprep` | Departamento del reporte/registro |
| `munnam` | Municipio nacionalidad / nombre (otro) |
| `mupnap` | Municipio nacionalidad padre (código) |

## 11. Clasificadores y Indicadores Generales (7)

Campos de control/clasificación del sistema de registros.

| Columna | Descripción |
|---------|-------------|
| `getdif` | Indicador interno de diferencia/ajuste (registro auxiliar) |
| `areag` | Área geográfica agregada (zona/agrupación administrativa) |
| `tipoins` | Tipo de institución (donde se registró/atendió) |
| `ocur` | Código/indicador de tipo de ocurrencia |
| `nacmuj` | Código nacionalidad madre (campo uso en nacimientos) |
| `nachom` | Código nacionalidad padre (campo uso en nacimientos) |

## Notas

- **Cobertura temporal:** 2009-2022
- **Registros totales:** 7,295,381 (dataset consolidado)
- **Observación:** Muchas columnas son específicas a un tipo de evento (por ejemplo, `libras`, `semges` aplican sobre nacimientos) por lo que aparecerán con alto % de NaN en muestras de un solo tipo.

