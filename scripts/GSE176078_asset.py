import requests
import tarfile
from pathlib import Path
import shutil
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def download_gz_file(url: str, dest_path: Path, max_retries=5):
    """Download a .tar.gz file from the given URL with retries."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    retries = Retry(total=max_retries, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    try:
        with session.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                    if chunk:
                        f.write(chunk)
        print(f"Successfully downloaded TAR file to: {dest_path}")
    except Exception as e:
        print(f"Download failed: {e}")
        if dest_path.exists():
            dest_path.unlink()  # Remove incomplete file


def extract_tar_gz_file(tar_gz_path: Path, extract_to: Path):
    """Extract all files from a .tar.gz archive directly into the target directory (flatten structure)."""
    extract_to.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_gz_path, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile():
                member.name = Path(member.name).name  # Remove any folder structure
                tar.extract(member, path=extract_to)
    print(f"Successfully extracted all files to: {extract_to}")


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


def GSE176078_asset_main():
    url = "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE176078&format=file&file=GSE176078%5FWu%5Fetal%5F2021%5FBRCA%5FscRNASeq%2Etar%2Egz"
    dest_dir = Path("assets/")
    tar_path = dest_dir / "GSE176078_RAW.tar.gz"
    tar_dest_dir = dest_dir / "GSE176078"

    # Download and extract
    download_gz_file(url, tar_path)
    extract_tar_gz_file(tar_path, tar_dest_dir)

    # Delete the downloaded tar.gz file
    delete_file_or_dir(tar_path)


if __name__ == "__main__":
    GSE176078_asset_main()
