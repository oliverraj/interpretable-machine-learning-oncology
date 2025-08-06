"""
Script to download interactions.tsv file from DGIdb and store it in assets folder.
This file contains drug-gene interaction data needed for breast cancer gene analysis.
"""

import requests
from pathlib import Path

def main():
    # Set destination path
    assets = Path("assets/")
    destination_file = assets / "interactions.tsv"
    
    # DGIdb URL for interactions data
    url = "https://dgidb.org/data/latest/interactions.tsv"
    
    print(f"Downloading interactions.tsv from DGIdb...")
    
    # Download the file
    response = requests.get(url)
    
    # Save the file
    with open(destination_file, 'wb') as file:
        file.write(response.content)
    
    print(f"File downloaded and saved to {destination_file}")

if __name__ == "__main__":
    main()