import os
from dotenv import load_dotenv
import polars as pl
from ingestion.raw_loader import load_snapshot
from ingestion.download import download

load_dotenv()
DATA_PATH: str = os.getenv("DATA_PATH")

while not DATA_PATH or len(os.listdir(DATA_PATH)) == 0:
    DATA_PATH = download()

file_dirs: list[str] = [entry.name for entry in os.scandir(DATA_PATH) if entry.is_dir()]

dataset_dir: str = os.path.join(DATA_PATH, file_dirs[0], file_dirs[0])
print(dataset_dir)
data_dirs: list[str] = [entry.name for entry in os.scandir(dataset_dir) if not entry.is_dir()]
data_dir_path: str = os.path.join(DATA_PATH, file_dirs[0], file_dirs[0], data_dirs[0])
test: pl.DataFrame = load_snapshot(data_dir_path, 2)

print(test.head())
