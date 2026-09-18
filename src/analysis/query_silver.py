"""Queries to analyse the Silver layer parquet file."""

from pathlib import Path

import duckdb

from src.schemas.dataset_specs import SPECS

TARGET_ID = 2
path_to_silver_data: Path = Path(f"./data/silver/set{TARGET_ID}_silver.parquet")
if not path_to_silver_data.exists():
    raise FileNotFoundError(
        f"{path_to_silver_data.name}: Provided path does not exists"
    )

data_columns: list[str] = SPECS.get(TARGET_ID).column_names

TARGET_METRIC: str = "rms"
QUERY_PAYLOAD: str = ",".join(
    [f"max({col}_{TARGET_METRIC}) AS max_{col}_{TARGET_METRIC}" for col in data_columns]
)
QUERY_MAX_VALUES: str = f"""SELECT {QUERY_PAYLOAD} FROM '{path_to_silver_data}'"""
duckdb.sql(QUERY_MAX_VALUES).show()

QUERY_MAX_B1RMS: str = f"""SELECT snapshot_timestamp,b1_rms FROM '{path_to_silver_data}'
                 ORDER BY b1_rms DESC LIMIT 5"""
duckdb.sql(QUERY_MAX_B1RMS).show()
