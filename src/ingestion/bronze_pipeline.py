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
        single_files.append(load_snapshot(f, dataset_id))
    merged_files = pl.concat(single_files)

    # Check that the concatenation worked
    if merged_files.height != len(single_files) * DatasetSpec.get_rows():
        sys.exit("Loss of data during dataframe concatenation")

    path_to_bronze_data: Path = Path(f"./data/bronze/set{dataset_id}_bronze.parquet")
    merged_files.write_parquet(path_to_bronze_data)

    logger.info("Size of parquet file: %s", os.path.getsize(path_to_bronze_data))
    logger.info("Size of raw dataset files: %s", sizes.sum())
