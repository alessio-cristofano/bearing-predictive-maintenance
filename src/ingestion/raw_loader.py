"""Raw Loader module from raw ASCII file to in-memory polars DataFrames."""

from datetime import datetime
from pathlib import Path

import polars as pl

from src.schemas.dataset_specs import SPECS, DatasetSpec


def parse_filename_timestamp(filename: str) -> datetime:
    """Parses timestamp format YYYY.MM.DD.HH.MM.SS from IMS filename."""
    return datetime.strptime(filename, "%Y.%m.%d.%H.%M.%S")


def load_snapshot(file_path: Path, dataset_id: int) -> pl.DataFrame:
    """Loads a single 20,480-row IMS ASCII snapshot and attaches metadata.

    Two columns are added as metadata:
    - snapshot_timestamp: timestamp of the data (derived from filename)
    - sample_index: internal sequential integer index

    Args:
        file_path (Path): the path to the dataset.
        dataset_id (int): the ID of the dataset to analyse.

    Returns:
        polars DataFrame representation of the dataset + metadata
    """
    spec: DatasetSpec = SPECS[dataset_id]
    filename: str = file_path.name
    ts: datetime = parse_filename_timestamp(filename)

    # Files are tab-separated or space-separated ASCII without headers
    df: pl.DataFrame = pl.read_csv(
        file_path,
        separator="\t",
        has_header=False,
        new_columns=spec.column_names,
        schema_overrides={col: pl.Float32 for col in spec.column_names},
    )

    if df.height != spec.expected_rows:
        raise ValueError(
            f"{filename}: Expected {spec.expected_rows} rows, got {df.height}"
        )

    return df.with_columns(
        pl.lit(ts).alias("snapshot_timestamp"),
        pl.int_range(0, pl.len(), dtype=pl.UInt16).alias("sample_index"),
    )
