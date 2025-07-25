import requests
import tarfile
from pathlib import Path
import shutil
import gzip


def download_tar_file(url: str, dest_path: Path):
    """Download a .tar file from the given URL."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"✅ Downloaded TAR file to: {dest_path}")


def extract_tar_file(tar_path: Path, extract_to: Path):
    """Extract all files from a .tar archive to the specified directory."""
    extract_to.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(path=extract_to)
    print(f"📦 Extracted all contents to: {extract_to}")


def extract_gz_files_in_dir(directory: Path):
    """Extract all .gz files in the given directory and remove the .gz files."""
    for gz_file in directory.glob("*.gz"):
        out_path = gz_file.with_suffix('')
        with gzip.open(gz_file, 'rb') as f_in, open(out_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print(f"🗜️ Extracted: {gz_file} -> {out_path}")
        gz_file.unlink()  # Delete the .gz file


def delete_file_or_dir(path: Path):
    """Delete a file or directory."""
    if path.is_file():
        path.unlink()
        print(f"🗑️ Deleted file: {path}")
    elif path.is_dir():
        shutil.rmtree(path)
        print(f"🗑️ Deleted directory: {path}")
    else:
        print(f"⚠️ Path does not exist: {path}")


def gse180286_asset_main():
    url = "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE180286&format=file"
    dest_dir = Path("assets/")
    tar_path = dest_dir / "GSE180286_RAW.tar"
    tar_dest_dir = dest_dir / "GSE180286"

    # Download and extract
    download_tar_file(url, tar_path)
    extract_tar_file(tar_path, tar_dest_dir)

    # Extract all .gz files in the extracted folder
    extract_gz_files_in_dir(tar_dest_dir)

    # Delete the downloaded tar file
    delete_file_or_dir(tar_path)


if __name__ == "__main__":
    gse180286_asset_main()
