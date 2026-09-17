from pathlib import Path

import polars as pl

from src.schemas.dataset_specs import SPECS


def silver_pipeline(id: int):
    path_to_bronze_data: Path = Path(f"./data/bronze/set{id}_bronze.parquet")
    bronze_data: pl.DataFrame = pl.read_parquet(path_to_bronze_data)

    # Group by snapshot timestamp (1 second) and compute relevant metrics
    ## Metrics to compute:
    # Mean
    # Standard Deviation
    # RMS
    # Peak-to-Peak
    # Kurtosis

    data_columns: list[str] = SPECS.get(id).column_names
    aggr_exprs: list[pl.Expr] = []

    for column in data_columns:
        aggr_exprs.extend(
            [
                pl.mean(column).name.suffix("_mean"),
                pl.std(column).name.suffix("_std"),
                (((pl.col(column) ** 2).mean()) ** 0.5).name.suffix("_rms"),
                (pl.max(column) - pl.min(column)).name.suffix("_p2p"),
                (((pl.col(column) - pl.mean(column)) / pl.std(column)) ** 4)
                .mean()
                .name.suffix("_kurtosis"),
                pl.count(column).name.suffix("_count"),
            ]
        )
    silver_data: pl.DataFrame = bronze_data.group_by("snapshot_timestamp").agg(
        aggr_exprs
    )

    print(f"Rows of the silver dataset: {silver_data.height}")
    path_to_silver_data: Path = Path(f"./data/silver/set{id}_silver.parquet")
    silver_data.write_parquet(path_to_silver_data)
