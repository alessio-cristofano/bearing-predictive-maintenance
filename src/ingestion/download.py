"""Download source data from kagglehub."""

import kagglehub  # Download latest version


def download() -> str:
    """Download source data from kagglehub.

    Returns:
        path (str): The path where the data are saved
    """
    path: str = kagglehub.dataset_download("vinayak123tyagi/bearing-dataset")
    return path
