import os
from dotenv import load_dotenv
import polars as pl
from ingestion.raw_loader import load_snapshot
from ingestion.download import download
from pathlib import Path

DATASET_MAPPING: list[dict] = [
    {"relative_path": "1st_test/1st_test", "id": 1},
    {"relative_path": "2nd_test/2nd_test", "id": 2},
    {"relative_path": "3rd_test/3rd_test", "id": 3},
]
TARGET_ID: int = 2

dataset: dict = next(d for d in DATASET_MAPPING if d["id"] == TARGET_ID)
#
load_dotenv()
data_path: Path = Path(os.getenv("DATA_PATH"))

while not any(data_path.iterdir()):
    data_path = download()

files: list[Path] = [
    f for f in (data_path / dataset.get("relative_path")).iterdir() if not f.is_dir()
]
test: list[pl.DataFrame] = []
final: pl.DataFrame = None
for f in files:
    test.append(load_snapshot(f, dataset.get("id")))
final = pl.concat(test)
print(final.height)
