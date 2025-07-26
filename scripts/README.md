# Scripts for Dataset Download and Management

This directory contains scripts for downloading and managing datasets used in the project. The scripts handle downloading, extracting, and organizing datasets from various sources, ensuring they are ready for analysis.

## Script Overview

Each script in this directory is designed to:

- Download a specific dataset from its source.
- Extract the dataset contents to the appropriate location.
- Delete the original compressed files after extraction to save space.

## Usage

1. Ensure you have Python 3.11 or above installed.
2. Install required dependencies from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the desired script to download and prepare a dataset:
    ```bash
    python GSE176078_asset.py
    ```

    ```bash
    python GSE161529_asset.py
    ```

    ```bash
    python GSE180286_asset.py
    ```

    ```bash
    python Gencode_asset.py
    ```
