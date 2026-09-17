import os
import sys
from dotenv import load_dotenv
import polars as pl
from ingestion.raw_loader import load_snapshot
from ingestion.download import download
from pathlib import Path
from schemas.dataset_specs import DatasetSpec
import numpy as np


def bronze_pipeline(mapping: list[dict], id: int):
    dataset: dict = next(d for d in mapping if d["id"] == id)
    #
    load_dotenv()
    data_path: Path = Path(os.getenv("DATA_PATH"))

    if not data_path.exists() or not any(data_path.iterdir()):
        data_path = download()

    if data_path is None:
        sys.exit("No Data Path found")

    files: list[Path] = [
        f for f in (data_path / dataset.get("relative_path")).iterdir() if not f.is_dir()
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
        single_files.append(load_snapshot(f, dataset.get("id")))
    merged_files = pl.concat(single_files)

    # Check that the concatenation worked
    if merged_files.height != len(single_files) * DatasetSpec.get_rows():
        sys.exit("Loss of data during dataframe concatenation")

    path_to_bronze_data: Path = Path(f"./data/bronze/set{id}_bronze.parquet")
    merged_files.write_parquet(path_to_bronze_data)

    print(f"Size of parquet file: {os.path.getsize(path_to_bronze_data)}")
    print(f"Size of raw dataset files: {sizes.sum()}")
