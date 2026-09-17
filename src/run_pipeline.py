from pathlib import Path
from ingestion.bronze_pipeline import bronze_pipeline
from features.silver_pipeline import silver_pipeline
import time

DATASET_MAPPING: list[dict] = [
    {"relative_path": "1st_test/1st_test", "id": 1},
    {"relative_path": "2nd_test/2nd_test", "id": 2},
    {"relative_path": "3rd_test/3rd_test", "id": 3},
]
TARGET_ID: int = 2


path_to_bronze_data: Path = Path(f"./data/bronze/set{TARGET_ID}_bronze.parquet")
path_to_silver_data: Path = Path(f"./data/silver/set{TARGET_ID}_silver.parquet")

time_bronze: float = 0
time_silver: float = 0
if not path_to_bronze_data.exists():
    start_time_bronze: float = time.time()
    bronze_pipeline(DATASET_MAPPING, TARGET_ID)
    time_bronze = time.time() - start_time_bronze
else:
    print("Skipping bronze layer ingestion: parquet file already exists")

if not path_to_silver_data.exists():
    start_time_silver: float = time.time()
    silver_pipeline(TARGET_ID)
    time_silver = time.time() - start_time_silver
else:
    print("Skipping silver layer ingestion: parquet file already exists")

print(f"Time to execute bronze + silver pipelines: {(time_bronze + time_silver):2.2f} s")
