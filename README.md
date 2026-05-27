# PROYECTO PARA OBTENER INFORMACIÓN POR CENTRO POBLADO

Este proyecto recopila información de los centros poblados del Perú mediente el uso *web scraping* y `Python`.

## Entorno de desarrollo

El presente proyecto fue desarrollado utilizando `python 3.10`. Para replicar el entorno de desarrollo puede utilizar los siguientes comandos:

Utilizando `uv`:
> [!INFO] Puede instalar `uv` siguiendo la [documentación oficial](https://docs.astral.sh/uv/getting-started/installation/)

```sh
uv sync
```

Utilizando `venv` y `pip` (Linux):
> [!INFO] Para SO Windows, puede seguir los pasos descritos en [el siguiente link](https://docs.python.org/3/library/venv.html)

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

Estos *logs* se guardan en la carpeta `./data/processed/` con el siguiente patrón `ubigeo_{codigo_del_ubigeo}_{tipo_de_log}.txt`, por ejemplo, `ubigeo_010101_log.txt` corresponde a la lista de centros poblados del ubigeo 010101 con consulta exitosa.

El código `./inei_ccpp_summary.py` se encarga de resumir los resultados de la recopilación de datos, la información se resumen en 3 tipos de salidas:

* CCPP con datos: se refiere a los centros poblados que resultaron en consulta exitosa y contaron con registros.
* CCPP sin datos: se refiere a los centros poblados que resultaron en consulta exitosa pero no contaron con registros.
* CCPP sin consulta: se refiere a los centros poblados que no resultaron en una consulta exitosa.

En caso se obtuvieran centro poblados sin consulta exitosa (CCPP sin consulta), es necesario volver a ejecutar el código para tratar de recabar esta información.
