"""Bronze layer data ingestion for the Bearings Predictive Maintenance pipeline."""

import logging
import os
import sys
from pathlib import Path

import numpy as np
import polars as pl
from dotenv import load_dotenv

from src.ingestion.download import download
from src.ingestion.raw_loader import load_snapshot
from src.schemas.dataset_specs import DatasetSpec

logger = logging.getLogger(__name__)


def validate_snapshot(
    df: pl.DataFrame, expected_cols: int, expected_rows: int = 20480
) -> None:
    """Enforce data contracts based on physical sensor constraints.

    Args:
        df (pl.DataFrame): dataframe containing bronze data.
        expected_cols (int): Expected number of column (4 or 8).
        expected_rows (int): Expected number of rows (20480).

    Raises:
        ValueError:
            - df has at least one null value
            - df has not the expected number of columns or rows
    """
    # 1. Enforce Exact Snapshot Duration
    if df.height != expected_rows:
        raise ValueError(
            f"Data contract violation: Expected {expected_rows} rows, got {df.height}."
        )

    # 2. Enforce Sensor Channel Count
    if df.width != expected_cols:
        raise ValueError(
            f"Schema violation: Expected {expected_cols} columns, got {df.width}."
        )

    # 3. Enforce Signal Continuity (No dropped packets)
    null_counts = df.null_count().sum(axis=1).item()
    if null_counts > 0:
        raise ValueError(
            f"Signal corruption: Found {null_counts} NULL values in snapshot."
        )


def bronze_pipeline(config: dict[str, dict], dataset_id: int) -> None:
    """Orchestrates the ingestion of raw IMS bearing data into Parquet format.

    Parses raw ASCII files containing 20kHz vibration snapshots, dynamically
    maps column headers based on the sensor configuration (4 or 8 channels),
    and writes the compressed output to the Bronze layer (data/bronze/).

    Args:
        config (dict[str,dict]): Configuration mapping containing relative paths.
        dataset_id (int): Target dataset identifier (1, 2, or 3).

    Raises:
        ValueError: If the dataset_id is not found in the mapping.
    """
    dataset: dict = config.get("datasets").get(dataset_id)
    expected_columns: int = dataset.get("channels") + 2  # two metadata columns added
    load_dotenv()
    data_path: Path = Path(os.getenv("DATA_PATH"))

    if not data_path.exists() or not any(data_path.iterdir()):
        data_path = download()

    if data_path is None:
        sys.exit("No Data Path found")

    files: list[Path] = [
        f
        for f in (data_path / dataset.get("relative_path")).iterdir()
        if not f.is_dir()
    ]
    sizes: np.ndarray = np.array(
        [
            os.path.getsize(f)
            for f in (data_path / dataset.get("relative_path")).iterdir()
            if not f.is_dir()
        ]
    )
    single_files: list[pl.DataFrame] = []
    for f in files:
        snapshot: pl.DataFrame = load_snapshot(f, dataset_id)
        validate_snapshot(snapshot, expected_columns)
        single_files.append(snapshot)
    merged_files = pl.concat(single_files)

    # Check that the concatenation worked
    if merged_files.height != len(single_files) * DatasetSpec.get_rows():
        sys.exit("Loss of data during dataframe concatenation")

    path_to_bronze_data: Path = Path(f"./data/bronze/set{dataset_id}_bronze.parquet")
    merged_files.write_parquet(path_to_bronze_data)

    logger.info("Size of parquet file: %s", os.path.getsize(path_to_bronze_data))
    logger.info("Size of raw dataset files: %s", sizes.sum())
