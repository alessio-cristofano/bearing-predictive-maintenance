"""Silver layer data transformation for the Bearings Predictive Maintenance pipeline."""

import logging
from pathlib import Path

import polars as pl

from src.schemas.dataset_specs import SPECS

logger = logging.getLogger(__name__)


def silver_pipeline(dataset_id: int) -> None:
    """Orchestrates the transformation of bronze data into silver level features.

    Parses polar dataframe from the bronze layer containing the target dataset id,
    computes features for each 1 second slice and writes the output to the Silver
    layer (data/silver/) in Parquet file format.
    The computed features are the following:
    - Mean
    - Standard Deviation
    - RMS
    - Peak-to-Peak
    - Kurtosis

    Args:
        dataset_id (int): Target dataset identifier (1, 2, or 3).
    """
    path_to_bronze_data: Path = Path(f"./data/bronze/set{dataset_id}_bronze.parquet")
    bronze_data: pl.DataFrame = pl.read_parquet(path_to_bronze_data)
    data_columns: list[str] = SPECS.get(dataset_id).column_names
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

    logger.info("Rows of the silver dataset: %s", silver_data.height)
    path_to_silver_data: Path = Path(f"./data/silver/set{dataset_id}_silver.parquet")
    silver_data.write_parquet(path_to_silver_data)
