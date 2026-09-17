from datetime import datetime
from pathlib import Path
from random import random

import polars as pl
import pytest

from src.ingestion.raw_loader import load_snapshot, parse_filename_timestamp
from src.schemas.dataset_specs import SPECS, DatasetSpec

VALID_TIMESTAMP_SAMPLES = [
    ("2000.12.30.08.30.21", datetime(2000, 12, 30, 8, 30, 21)),
    ("2004.02.12.10.32.39", datetime(2004, 2, 12, 10, 32, 39)),
]

INVALID_TIMESTAMP_SAMPLES = [
    "2000.13.30.08.30.21",  # Wrong month
    "2000.12.32.08.30.21",  # Wrong day
    "2000.12.30.25.30.21",  # Wrong hour
    "2000.12.30.08.61.21",  # Wrong minute
    "2000.12.30.08.30.61",  # Wrong second
    "not_a_timestamp",  # Malformed string
]

ID_SAMPLES = [1, 2, 3]


@pytest.mark.parametrize("input,result", VALID_TIMESTAMP_SAMPLES)
def test_parse_filename_timestamp_valid(input: str, result: datetime) -> None:
    assert parse_filename_timestamp(input) == result


@pytest.mark.parametrize("input", INVALID_TIMESTAMP_SAMPLES)
def test_parse_filename_timestamp_invalid(input: str) -> None:
    with pytest.raises(ValueError):
        parse_filename_timestamp(input)


def create_synthetic_dataset(m: int, n: int, filename: str):
    with open(filename, "w") as file:
        for _ in range(m):
            rnd: list[str] = [str(random()) for _ in range(n)]
            file.write("\t".join(rnd) + "\n")


@pytest.mark.parametrize("test_id", ID_SAMPLES)
def test_load_snapshot(
    test_id: int, tmp_path: Path
):  # Usage of tmp_path does not require manual clean up
    """Test that load_snapshot loads the correct number of rows and correct column names"""
    test_height: int = 20480
    spec: DatasetSpec = SPECS[test_id]
    test_file_path: str = tmp_path / "2004.02.12.10.32.39"
    test_column_names: list[str] = spec.column_names
    create_synthetic_dataset(test_height, len(test_column_names), test_file_path)
    test_dataframe: pl.DataFrame = load_snapshot(test_file_path, test_id)
    expected_columns = list(spec.column_names) + [
        "snapshot_timestamp",
        "sample_index",
    ]  # add metadata columns
    assert test_dataframe.height == test_height
    assert test_dataframe.columns == expected_columns
