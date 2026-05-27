# PROYECTO PARA OBTENER INFORMACIÓN POR CENTRO POBLADO

> [!IMPORTANT]
> Todavía no se contempla el código para juntar todas las bases de datos parciales (`./data/processed/ubigeo_{codigo_ubigeo}_data.csv`) y unirlas (*join*) con `./data/raw/ccpp_data.csv`.

Este proyecto recopila información de los centros poblados del Perú mediente el uso *web scraping* y `Python`.

## Entorno de desarrollo

El presente proyecto fue desarrollado utilizando `python 3.10`. Para replicar el entorno de desarrollo puede utilizar los siguientes comandos:

Utilizando `uv`:
> [!NOTE]
> Puede instalar `uv` siguiendo la [documentación oficial](https://docs.astral.sh/uv/getting-started/installation/)

```sh
uv sync
```

Utilizando `venv` y `pip` (Linux):
> [!NOTE]
> Para SO Windows, puede seguir los pasos descritos en [el siguiente link](https://docs.python.org/3/library/venv.html)

```sh
python -m venv ./.venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

## Estructura del proyecto

El proyecto tiene la siguiente estructura:

```
./
├── data/
│   ├── logs/
│   ├── processed/
│   └── raw/
│       └── ccpp_data.csv # Información de centros poblados
├── inei_ccpp.py
├── inei_ccpp_summary.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── uv.lock
└── README.md
```

El código `./inei_ccpp.py` se encarga de recopilar la información a nivel de departamento por lo que es necesario modificar la variable `cod_depa` en cada ejecución. Este paso se puede obviar mediante un *for loop* que itere sobre los 25 departamentos (01-25). El código, además, cuenta con *logs* de avance para recuperar la consulta en caso se dieran problemas de conexión, esto implica que la siguiente ejecución del código solo realizará la consulta para aquellos centros poblados que aun no han sido registrados o tuvieron algun problema (*status code 400*). Los *logs* se dividen en 3 tipos:

* `log`: Información del código de centro poblado que resultó en consulta exitosa y con registros.
* `nor`: Información del código de centro poblado que resultó en consulta exitosa y sin registros.
* `err`: Información del código de centro poblado que no resultó en consulta exitosa.

Estos *logs* se guardan en la carpeta `./data/processed/` con el siguiente patrón `ubigeo_{codigo_ubigeo}_{tipo_log}.txt`, por ejemplo, `ubigeo_010101_log.txt` corresponde a la lista de centros poblados del ubigeo 010101 con consulta exitosa.

El código `./inei_ccpp_summary.py` se encarga de resumir los resultados de la recopilación de datos, la información se resumen en 3 tipos de salidas:

* CCPP con datos: se refiere a los centros poblados que resultaron en consulta exitosa y contaron con registros.
* CCPP sin datos: se refiere a los centros poblados que resultaron en consulta exitosa pero no contaron con registros.
* CCPP sin consulta: se refiere a los centros poblados que no resultaron en una consulta exitosa.

En caso se obtuvieran centro poblados sin consulta exitosa (CCPP sin consulta), es necesario volver a ejecutar el código para tratar de recabar esta información.

## Entradas y Salidas

La base de datos `ccpp_data.csv` se utiliza como insumo para determinar todos los centros poblados sujetos a recopilación de información. Esta base de datos cuenta con los siguientes campos:

* `idccpp`: Código único del centro poblado.
* `nombccpp`: Nombre del centro poblado.
* `codccpp`: Código del centro poblado.
* `nomdist`: Nombre del distrito.
* `nomprov`: Nombre de la provincia.
* `nomdep`: Nombre del deparatmento.
* `ubigeo`: Código ubigeo.
* `area_censa`: Área censal (de acuerdo al Censo Nacional 2017)
* `lon`: Coordenada geográfica longitud.
* `lat`: Coordenada geográfica latitud.

Las bases de datos resultantes del proceso de recopilación mediante *web scraping* cuenta con las siguientes variables:

* `DEPARTAMENTO`
* `PROVINCIA`
* `DISTRITO`
* `CENTRO POBLADO`
* `CATEGORIA`
* `CODIGO DE UBIGEO Y CENTRO POBLADO`
* `LONGITUD`
* `LATITUD`
* `ALTITUD`
* `POBLACION`
* `VIVIENDA`
* `AGUA POR RED PUBLICA`
* `ENERGIA ELECTRICA EN LA VIVIENDA`
* `DESAGUE POR RED PUBLICA`
* `VIA DE MAYOR USO`
* `TRANSPORTE DE MAYOR USO`
* `FRECUENCIA`
* `TIEMPO EN MINUTOS HACIA LA CAPITAL DEL DISTRITO`
* `DISTANCIA DEL CENTRO POBLADO HACIA LA CAPITAL DEL DISTRITO(KM)`
* `DISTANCIA DEL CENTRO POBLADO HACIA EL CENTRO POBLADO EDUCATIVO `
* `DISTANCIA DEL CENTRO POBLADO HACIA EL CENTRO DE SALUD MAS CERCA`
* `ALUMBRADO PUBLICO`
* `TELEFONO PUBLICO`
* `LOCAL COMUNAL`
* `HOSTAL / ALBERGUE`
* `ESTACION DE RADIO`
* `INSTITUCION EDUCATIVA PRIMARIA`
* `INSTITUCION EDUCATIVA SECUNDARIA`
* `ESTABLECIMIENTO/ PUESTO DE SALUD`
* `PUESTO POLICIAL`
* `OFICINA DE CORREO`
* `CABINA DE INTERNET`
* `HELADAS /NEVADAS`
* `GRANIZADAS`
* `LLUVIAS`
* `SEQUIAS`
* `VENDAVALES (VIENTOS FUERTES)`
* `INUNDACIONES`
* `DERRUMBES/DESLIZAMIENTOS`
* `HUAYCOS / ALUDES/ALUVIONES`
* `DESERTIFICACIONES`
* `SALINIZACION DE LOS SUELOS`
* `ACTIVIDAD VOLCANICA`
* `SISMOS`
* `TSUNAMI U OLEADAS ANOMALOS`
* `OTROS FENOMENOS NAT.`
* `DERRAME DE SUSTANCIAS O DESECHOS TOXICOS`
* `FUGAS DE GASES TOXICOS`
* `EXPLOSIONES`
* `INCENDIOS Y QUEMAS`
* `CRIANZA DE ANIMALES EN ZONAS URBANAS`
* `INCREMENTO DE ZONAS INDUS. NO AUTORIZADAS`
* `ZONAS AEREOPORTUARIAS`
* `RELLENOS SANITARIOS`
* `SUBVERSIONES Y/O CONFLICTOS SOCIALES`
* `OTROS PELIGROS`
* `UN LECHO DE RIO O QUEBRADA`
* `UN CUARTEL MILITAR O POLICIAL`
* `UNA VIA FERREA`
* `LA EROSION DE RIOS EN LADERAS DE CERROS`
* `BARRANCOS O PRECIPICIOS`
* `OTROS`
* `PISTAS Y VEREDAS EN LA MAYORI DE SUS CALLES Y/O MANZANAS`
* `CANALES DE DRENAJE EN LAS CALLES PARA LA EVACUACION DE LAS AGUA`
* `IDIOMA O LENGUA QUE SE HABLA CON MAYOR FRECUENCIA`
