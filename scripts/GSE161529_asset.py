import requests
import tarfile
from pathlib import Path
import shutil
import gzip


def download_gz_file(url: str, dest_path: Path):
    """Download a .gz file from the given URL."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Successfully downloaded GZ file to: {dest_path}")


def extract_single_gz_file(gz_path: Path):
    """Extract a single .gz file and remove the .gz file."""
    out_path = gz_path.with_suffix('')
    with gzip.open(gz_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"Successfully extracted: {gz_path} -> {out_path}")
    gz_path.unlink()  # Delete the .gz file


def download_tar_file(url: str, dest_path: Path):
    """Download a .tar file from the given URL."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Successfully downloaded TAR file to: {dest_path}")


def extract_tar_file(tar_path: Path, extract_to: Path):
    """Extract all files from a .tar archive to the specified directory."""
    extract_to.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(path=extract_to)
    print(f"Successfully extracted all contents to: {extract_to}")


def extract_gz_files_in_dir(directory: Path):
    """Extract all .gz files in the given directory and remove the .gz files."""
    for gz_file in directory.glob("*.gz"):
        out_path = gz_file.with_suffix('')
        with gzip.open(gz_file, 'rb') as f_in, open(out_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print(f"Successfully extracted: {gz_file} -> {out_path}")
        gz_file.unlink()  # Delete the .gz file


def delete_file_or_dir(path: Path):
    """Delete a file or directory."""
    if path.is_file():
        path.unlink()
        print(f"Successfully deleted file: {path}")
    elif path.is_dir():
        shutil.rmtree(path)
        print(f"Successfully deleted directory: {path}")
    else:
        print(f"Path does not exist: {path}")


def gse161529_asset_main():
    # URLs for GSE161529 data
    tar_url = "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE161529&format=file"
    features_url = "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE161529&format=file&file=GSE161529%5Ffeatures%2Etsv%2Egz"
    
    dest_dir = Path("assets/")
    tar_path = dest_dir / "GSE161529_RAW.tar"
    tar_dest_dir = dest_dir / "GSE161529"
    features_gz_path = tar_dest_dir / "GSE161529_features.tsv.gz"

    # Download and extract the main TAR file
    download_tar_file(tar_url, tar_path)
    extract_tar_file(tar_path, tar_dest_dir)

    # Extract all .gz files in the extracted folder
    extract_gz_files_in_dir(tar_dest_dir)

    # Download and extract the features.tsv.gz file
    download_gz_file(features_url, features_gz_path)
    extract_single_gz_file(features_gz_path)

    # Delete the downloaded tar file
    delete_file_or_dir(tar_path)


if __name__ == "__main__":
    gse161529_asset_main()
