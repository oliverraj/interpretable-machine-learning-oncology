# Precision Oncology through Interpretable Machine Learning : Tumor vs Normal Cell Signatures from Single-Cell Data

This project analyzes single-cell and spatial transcriptomics data from human breast cancers, focusing on distinguishing tumor and normal cell populations through comprehensive computational methods. The workflow includes data acquisition, feature engineering, copy number variation analysis, machine learning classification, and integration of therapeutic target information using DGIdb and Open Targets databases to identify clinically relevant gene targets for precision oncology.


---

## Folder Structure
The repository is organized in the following manner where the details inside brackets is not included in the repository, to avoid size and LFS limitations. When you clone the repository please follow the instructions in the README to set up the environment and download the data files and place them in the appropriate directories.

```
ghost-cell-busters/
│
├── assets/
│   ├── Gencode/
│   │   ├── (extracted GTF files)
│   │   └── README.md
│   │
│   ├── GSE161529/
│   │   ├── (extracted data files)
│   │   └── README.md
│   │
│   ├── GSE176078/
│   │   ├── (extracted data files)
│   │   └── README.md
│   │
│   └── GSE180286/
│       ├── (extracted data files)
│       └── README.md
│
├── notebooks/
│   ├── 01_GSE176078.ipynb
│   ├── 02_GSE176078_model.ipynb
│   ├── 03_GSE176078_shap.ipynb
│   ├── 04_GSE161529_validation.ipynb
│   ├── 05_GSE161529_cross_validation.ipynb
│   ├── 06_GSE161529_oncogene.ipynb
│   ├── 07_GSE180286_validation.ipynb
│   ├── 08_GSE180286_cross_validation.ipynb
│   ├── 09_GSE180286_oncogene.ipynb
│   ├── 10_Combined_DE.ipynb
│   └── README.md
│
├── scripts/
│   ├── Gencode_asset.py
│   ├── GSE161529_asset.py
│   ├── GSE176078_asset.py
│   ├── GSE180286_asset.py
│   └── README.md
│
├── (venv)/
│   └── (virtual environment files)
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Setup Instructions

### 1. Prerequisites

- Ensure Python 3.11.9 or above is installed.
- Ensure git is installed.

### 2. Clone the Repository

```sh
git clone "https://github.com/mads-capstone-team24-summer-2025/ghost-cell-busters.git"
cd ghost-cell-busters
```

### 3. Install Dependencies

Recommended: Use a virtual environment.

```sh
python -m venv venv  # On Windows
python3 -m venv venv  # On Mac/Linux

# Activate the virtual environment
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt
```

If `requirements.txt` is missing, install these packages:

```sh
pip install scanpy pandas numpy matplotlib seaborn scikit-learn gseapy mygene infercnvpy shap xgboost imbalanced-learn gtfparse
```

### 4. Data Preparation

- Use the scripts in the `scripts/` folder to help organize and prepare your data:
  - For each dataset, run the corresponding script to download or process files as needed. For example:
    ```sh
    python scripts/GSE176078_asset.py
    ```
    This will help set up the `assets/GSE176078/` directory with required files.
  - Similarly, use `GSE161529_asset.py` and `GSE180286_asset.py` for other datasets.
  - To prepare gene annotation assets, run:
    ```sh
    python scripts/Gencode_asset.py
    ```
    This will download the GTF annotation file (`gencode.v44.annotation.gtf.gz`) if not already present.

### 5. Running the Analysis

- Open `notebooks/01_GSE176078.ipynb` and `notebooks/02_GSE176078_model.ipynb` in Jupyter or VS Code.
- Execute cells sequentially to:
  - Load and preprocess single-cell transcriptomics data
  - Engineer relevant features including cell cycle, apoptosis, ribosomal content, OXPHOS, and CNV scores
  - Classify tumor versus normal cells based on transcriptomic signatures
  - Visualize and explore classification results
  - Train machine learning models and interpret feature importance using SHAP values
- Repeat for other notebooks as needed.

---

## Main Analysis Steps

1. **Data Loading:** Construct AnnData objects from raw single-cell sequencing data.
2. **Feature Engineering:** Calculate key cellular features including cell cycle, apoptosis, ribosomal content, OXPHOS, and CNV scores.
3. **Cell Classification:** Identify and classify tumor versus normal cells based on transcriptomic and genomic signatures.
4. **Visualization:** Generate plots to explore distributions and proportions across cell subtypes and states.
5. **Differential Expression:** Detect genes differentially expressed between tumor and normal cells.
6. **CNV Analysis:** Annotate genes, perform inferCNV analysis, and quantify CNV burden per cell.
7. **Machine Learning:** Develop classifiers for tumor/normal prediction and interpret model outputs using SHAP.
8. **Therapeutic Mapping:** Integrate DGIdb druggability data and Open Targets disease association scores to stratify genes by therapeutic relevance and breast cancer support.

---

## Outputs

- Processed AnnData objects (`*obs.csv`)
- Machine Learning Model (`*.pkl`)
- Plots and figures (generated by running the notebooks)

---

## Notes

- The project uses both Python scripts and IPython notebooks.
- Some steps require substantial memory and compute (especially CNV and Machine Learning).

---

## References

- [Scanpy documentation](https://scanpy.readthedocs.io/)
- [infercnvpy documentation](https://icbi-lab.github.io/infercnvpy/)
- [MSigDB Hallmark gene sets](https://www.gsea-msigdb.org/gsea/msigdb/collections.jsp#H)
- [Gencode GTF files](https://www.gencodegenes.org/human/)

---

## Statement of Work
- Rajeev Prasad:
1) Led data preprocessing and feature engineering, including calculation of biological scores (CNV, cell cycle, apoptosis, oxphos).
2) Developed, trained, and optimized the XGBoost machine learning model, applying SMOTE for class balancing and conducting model evaluation.
3) Performed SHAP-based interpretability analyses and generated key visualizations.
4) Integrated drug-gene interaction and clinical trial data to prioritize therapeutic targets.
5) Conducted cross-dataset validation, biological concordance, network and pathway analyses.
6) Authored these report sections, including Methodology, Results, Discussion, and Future Directions.

- Haider Rizvi:
1) Set up the Python environment and configured software tools.
2) Organized, cleaned, and maintained the project notebooks in VSCode for reproducibility and ease of collaboration.
3) Managed the GitHub repository setup, including version control and collaborative workflow management.
4) Provided ongoing support in codebase management and troubleshooting.
5) Authored these report sections, including Project Statement, Methodology.
6) Helped in the cross-validation of GSE161529 dataset.

---

## Authors

- Haider Rizvi - [GitHub](https://github.com/rizvi-haider)
- Rajeev Prasad - [GitHub](https://github.com/oliverraj)

---

**Note:** The `assets/` folder containing raw and processed data is **not included** in this repository due to size and LFS limitations.
