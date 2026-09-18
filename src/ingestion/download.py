"""Download source data from kagglehub."""

import shutil
from pathlib import Path

import kagglehub  # Download latest version


def download(data_path: Path) -> None:
    """Download source data from kagglehub.

    Args:
        data_path (Path): The path where the data are saved
    """
    path: str = kagglehub.dataset_download("vinayak123tyagi/bearing-dataset")
    shutil.move(path, data_path)
