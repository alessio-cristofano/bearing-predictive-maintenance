from datetime import datetime
import polars as pl
from schemas.dataset_specs import SPECS


def parse_filename_timestamp(filename: str) -> datetime:
    """Parses timestamp format YYYY.MM.DD.HH.MM.SS from IMS filename."""
    return datetime.strptime(filename, "%Y.%m.%d.%H.%M.%S")


def load_snapshot(file_path: str, dataset_id: int) -> pl.DataFrame:
    """
    Loads a single 20,480-row IMS ASCII snapshot and attaches metadata.
    """
    spec = SPECS[dataset_id]
    filename = file_path.split("/")[-1]
    ts = parse_filename_timestamp(filename)

    # Files are tab-separated or space-separated ASCII without headers
    df = pl.read_csv(
        file_path,
        separator="\t",
        has_header=False,
        new_columns=spec.column_names,
        schema_overrides={col: pl.Float32 for col in spec.column_names},
    )

    if df.height != spec.expected_rows:
        raise ValueError(f"{filename}: Expected {spec.expected_rows} rows, got {df.height}")

    return df.with_columns(
        pl.lit(ts).alias("snapshot_timestamp"),
        pl.int_range(0, pl.len(), dtype=pl.UInt16).alias("sample_index"),
    )
