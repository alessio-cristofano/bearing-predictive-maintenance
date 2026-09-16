import kagglehub  # Download latest version


def download():
    path = kagglehub.dataset_download("vinayak123tyagi/bearing-dataset")
    print("Path to dataset files:", path)
    return path
