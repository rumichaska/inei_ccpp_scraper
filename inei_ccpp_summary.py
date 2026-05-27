from pathlib import Path

import pandas as pd


def merge_logs(path: Path, out: Path, name: str, pattern: str):
    df_csv = open(Path(out / name), mode="w")
    df_csv.write("idccpp\n")
    for file in path.glob(pattern=pattern):
        if file.is_file():
            f = open(file)
            df_csv.write(f.read())
            f.close()

    df_csv.close()


DATA_DIR = Path("./data/processed")
DATA_OUT = Path("./data/logs")
DATA_OUT.mkdir(parents=True, exist_ok=True)

lista_depa: list[str] = [f"0{n}" if n < 10 else str(n) for n in range(1, 26)]
n_log: int = 0
n_nor: int = 0
n_err: int = 0

for depa in lista_depa:
    cod_depa = depa

    log_pattern: str = f"ubigeo_{cod_depa}*log.txt"
    nor_pattern: str = f"ubigeo_{cod_depa}*nor.txt"
    err_pattern: str = f"ubigeo_{cod_depa}*err.txt"

    merge_logs(DATA_DIR, DATA_OUT, f"{cod_depa}_log.csv", log_pattern)
    merge_logs(DATA_DIR, DATA_OUT, f"{cod_depa}_nor.csv", nor_pattern)
    merge_logs(DATA_DIR, DATA_OUT, f"{cod_depa}_err.csv", err_pattern)

    log_csv = pd.read_csv(DATA_OUT / f"{cod_depa}_log.csv", dtype=str, index_col=False)
    nor_csv = pd.read_csv(DATA_OUT / f"{cod_depa}_nor.csv", dtype=str, index_col=False)
    err_csv = pd.read_csv(DATA_OUT / f"{cod_depa}_err.csv", dtype=str, index_col=False)

    n_log = n_log + len(log_csv)
    n_nor = n_nor + len(nor_csv)
    n_err = n_err + len(err_csv)

    print(f"""
        Resumen de información del departamento {cod_depa} ({len(log_csv) + len(nor_csv) + len(err_csv)}):
        CCPP con datos: {len(log_csv)}
        CCPP sin datos: {len(nor_csv)}
        CCPP sin consulta: {len(err_csv)}
        """)


print(f"""
    Resumen de información nacional ({n_log + n_nor + n_err}):
    CCPP con datos: {n_log}
    CCPP sin datos: {n_nor}
    CCPP sin consulta: {n_err}
    """)
