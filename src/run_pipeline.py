import time
from pathlib import Path

import click

from src.features.silver_pipeline import silver_pipeline
from src.ingestion.bronze_pipeline import bronze_pipeline

DATASET_MAPPING: list[dict] = [
    {"relative_path": "1st_test/1st_test", "id": 1},
    {"relative_path": "2nd_test/2nd_test", "id": 2},
    {
        "relative_path": "3rd_test/4th_test/txt",
        "id": 3,
    },  # different folder structure in original 3rd dataset
]


@click.command()
@click.option(
    "--dataset-id",
    "--d",
    type=click.Choice([1, 2, 3], case_sensitive=False),
    default=2,
    show_default=True,
    help="Target IMS Dataset to process",
)
def run_pipeline(dataset_id: int = 2) -> None:
    while dataset_id < 1 or dataset_id > 3:
        dataset_id = click.prompt(
            "Please enter a valid target dataset_id (1,2 or 3)", type=int
        )
    path_to_bronze_data: Path = Path(f"./data/bronze/set{dataset_id}_bronze.parquet")
    path_to_silver_data: Path = Path(f"./data/silver/set{dataset_id}_silver.parquet")

    time_bronze: float = 0
    time_silver: float = 0
    if not path_to_bronze_data.exists():
        start_time_bronze: float = time.time()
        bronze_pipeline(DATASET_MAPPING, dataset_id)
        time_bronze = time.time() - start_time_bronze
    else:
        print("Skipping bronze layer ingestion: parquet file already exists")

    if not path_to_silver_data.exists():
        start_time_silver: float = time.time()
        silver_pipeline(dataset_id)
        time_silver = time.time() - start_time_silver
    else:
        print("Skipping silver layer ingestion: parquet file already exists")

    print(
        f"Time to execute bronze + silver pipelines: {(time_bronze + time_silver):2.2f} s"
    )


if __name__ == "__main__":
    run_pipeline()
