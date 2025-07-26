import requests
import gzip
from pathlib import Path
import shutil
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def download_gz_file(url: str, dest_path: Path, max_retries=5):
    """Download a .gtf.gz file from the given URL with retries."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    retries = Retry(total=max_retries, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    try:
        response = session.get(url, timeout=60)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded GTF file to: {dest_path}")
    except Exception as e:
        print(f"Download failed: {e}")
        if dest_path.exists():
            dest_path.unlink()  # Remove incomplete file


def extract_gtf_gz_file(gtf_gz_path: Path, extract_to: Path):
    """Extract a .gtf.gz file to the target directory."""
    extract_to.mkdir(parents=True, exist_ok=True)
    output_path = extract_to / gtf_gz_path.with_suffix('').name  # Remove .gz
    with gzip.open(gtf_gz_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"Successfully extracted file to: {output_path}")


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


def Gencode_asset_main():
    url = "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_44/gencode.v44.annotation.gtf.gz"
    dest_dir = Path("assets/")
    gz_path = dest_dir / "gencode.v44.annotation.gtf.gz"
    gtf_dest_dir = dest_dir / "Gencode"

    # Download and extract
    download_gz_file(url, gz_path)
    extract_gtf_gz_file(gz_path, gtf_dest_dir)

    # Delete the downloaded gtf.gz file
    delete_file_or_dir(gz_path)


if __name__ == "__main__":
    Gencode_asset_main()
