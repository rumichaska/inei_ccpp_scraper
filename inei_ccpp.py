# IMPORTS ----

from pathlib import Path

import pandas as pd
import requests as re

# GLOBALS ----

BASE_URL = (
    "http://sige.inei.gob.pe/test/atlas/index.php/area_influencia/consultar_reporte_zsc"
)

DATA_DIR = Path("./data/processed/")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# LOGGER HELPERS ----


def create_file(filepath: str | Path) -> Path:
    """Crea un archivo si no existe"""
    filepath = Path(filepath)
    filepath.touch(exist_ok=True)

    return filepath


def load_logger(filepath: str | Path) -> set:
    """Cargar logger en memoria como un set"""
    filepath = Path(filepath)

    if not filepath.exists():
        return set()

    return set(
        line.strip
        for line in filepath.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def save_logger(filepath: str | Path, data: set) -> None:
    """Guardar logger en txt"""
    filepath = Path(filepath)
    content = "\n".join(sorted(data)) + "\n" if data else ""
    filepath.write_text(content, encoding="utf-8")


# DATA ----

df_ccpp = pd.read_csv("./data/raw/ccpp_data.csv", dtype="str")
list_cod_ubigeo = df_ccpp.sort_values(by="ubigeo")["ubigeo"].unique().tolist()


# FILTERS ----

cod_depa = "10"
cod_dist = [cod for cod in list_cod_ubigeo if cod.startswith(cod_depa)]
n_dist = len(cod_dist)

# REQUEST ----

with re.Session() as s:
    for idx, ub in enumerate(cod_dist, start=1):
        print(f"\nProcesando ubigeo: {ub} ({idx}/{n_dist})")
        # LOGGER ----

        # Creación de loggers
        log_path = create_file(DATA_DIR / f"ubigeo_{ub}_log.txt")
        err_path = create_file(DATA_DIR / f"ubigeo_{ub}_err.txt")
        nor_path = create_file(DATA_DIR / f"ubigeo_{ub}_nor.txt")

        # Carga de  ogger
        log_ids = load_logger(log_path)
        err_ids = load_logger(err_path)
        nor_ids = load_logger(nor_path)

        # DATA ----
        data_path = DATA_DIR / f"ubigeo_{ub}_data.csv"

        try:
            ccpp_df = pd.read_csv(data_path, dtype="str", index_col=False)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            create_file(data_path)
            ccpp_df = pd.DataFrame()

        # CCPP ID
        cod_ccpp = sorted(df_ccpp[df_ccpp["ubigeo"] == ub]["codccpp"].tolist())

        # LOOP
        for id in cod_ccpp:
            cod_total = ub + id

            # Revisión de registro en log
            if cod_total in log_ids:
                print(f"[SKIP LOG] {cod_total} ya consultado")
                continue

            if cod_total in nor_ids:
                print(f"[SKIP NOR] {cod_total} consultado y sin registros")
                continue

            # CONSULTA ----
            params = {"ubigeo": ub, "ccpp": id}

            # Error en consulta
            try:
                r = s.get(url=BASE_URL, params=params, timeout=30)
            except re.RequestException:
                err_ids.add(cod_total)
                print(f"[REQUEST ERROR] {cod_total} no pudo ser consultado")
                continue

            if r.status_code != 200:
                err_ids.add(cod_total)
                print(f"[HTTP {r.status_code}] {cod_total} no pudo ser consultado")
                continue

            # Error en json
            try:
                r_json = r.json()
            except ValueError:
                err_ids.add(cod_total)
                print(f"[INVALID JSON] {cod_total}")
                continue

            # Consulta exitosa
            err_ids.discard(cod_total)

            if r_json.get("records") == 1:
                try:
                    r_content = r_json["rows"]
                    r_df = (
                        pd.DataFrame(
                            data=[item["cell"] for item in r_content],
                            columns=["col", "row"],
                        )
                        .set_index("col")
                        .T
                    )
                    ccpp_df = pd.concat([ccpp_df, r_df], ignore_index=True)
                    log_ids.add(cod_total)
                    print(f"[SUCCESS] {cod_total} consulta exitosa")
                except (KeyError, ValueError, TypeError):
                    err_ids.add(cod_total)
                    print(f"[PARSING ERROR] {cod_total}")
            else:
                nor_ids.add(cod_total)
                print(f"[NO RECORDS] {cod_total} sin registros")

        # GUARDAR ARCHIVOS ----

        ccpp_df.to_csv(data_path, index=False)
        save_logger(log_path, log_ids)
        save_logger(err_path, err_ids)
        save_logger(nor_path, nor_ids)

        print(
            f"""
            Ubigeo: {ub}
            Success: {len(log_ids)}
            No records: {len(nor_ids)}
            Errors: {len(err_ids)}
            """
        )
        print(f"{ub} terminado")
