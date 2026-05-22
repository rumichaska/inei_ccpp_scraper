from pathlib import Path

import pandas as pd
import requests as re

BASE_URL = (
    "http://sige.inei.gob.pe/test/atlas/index.php/area_influencia/consultar_reporte_zsc"
)

# TEST

# Parámetros de la consulta
cod_ubigeo = ["010202", "010101"]
cod_ccpp = ["0001", "0002", "0003", "0004", "0057"]

with re.Session() as s:
    for ub in cod_ubigeo:
        # Archivo de chequeo
        log_path = Path("./ubigeo_" + ub + "_log.txt")
        log_path.touch(exist_ok=True)

        data_path = Path("./ubigeo_" + ub + "_data.csv")
        try:
            ccpp_df = pd.read_csv(data_path, index_col=False)
            if ccpp_df.empty:
                ccpp_df = pd.DataFrame()
        except pd.errors.EmptyDataError:
            ccpp_df = pd.DataFrame()
        except FileNotFoundError:
            ccpp_df = pd.DataFrame()
            data_path.touch(exist_ok=True)

        # Consulta
        for id in cod_ccpp:
            cod_total = ub + id
            # NOTE: Agregar validación para ccpp que no tengan registros
            value_exists = False
            with open(file=log_path, mode="r") as f:
                for line in f:
                    if line.rstrip("\n\r") == cod_total:
                        value_exists = True
                        break
            if not value_exists:
                params = {"ubigeo": ub, "ccpp": id}
                r = s.get(url=BASE_URL, params=params)
                if r.status_code == 200:
                    if r.json()["records"] == 1:
                        with open(file=log_path, mode="a") as f:
                            f.write(cod_total + "\n")
                        r_content = r.json()["rows"]
                        r_df = (
                            pd.DataFrame(
                                data=[item["cell"] for item in r_content],
                                columns=["col", "row"],
                            )
                            .set_index("col")
                            .T
                        )
                        ccpp_df = pd.concat([ccpp_df, r_df], ignore_index=True)
                    else:
                        print("No se encontró información de ccpp para:", cod_total)
                else:
                    print("No se encontró conexión exitosa para:", cod_total)

        ccpp_df.to_csv(data_path, index=False)
