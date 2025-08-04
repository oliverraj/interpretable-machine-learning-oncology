# Notebooks

This folder contains Jupyter notebooks related to the Ghost Cell Busters project. The notebooks are organized to facilitate exploration, experimentation, and documentation of the project's data analysis, modeling, and results.

## Structure

### Data Processing and Feature Engineering
- **01_GSE176078.ipynb** [01_GSE176078.ipynb](./01_GSE176078.ipynb)  
   Initial data loading, preprocessing, and feature engineering for the GSE176078 training dataset.

- **04_GSE161529_obs.ipynb** [04_GSE161529_obs.ipynb](./04_GSE161529_obs.ipynb)  
   Data processing and observation file generation for the GSE161529 validation dataset.

- **07_GSE180286_obs.ipynb** [07_GSE180286_obs.ipynb](./07_GSE180286_obs.ipynb)  
   Data processing and observation file generation for the GSE180286 validation dataset.

### Model Development and Interpretation
- **02_GSE176078_model.ipynb** [02_GSE176078_model.ipynb](./02_GSE176078_model.ipynb)  
   XGBoost model training, validation, and performance evaluation using GSE176078 dataset.

- **03_GSE176078_shap.ipynb** [03_GSE176078_shap.ipynb](./03_GSE176078_shap.ipynb)  
   SHAP analysis for model interpretability and feature importance visualization.

### Cross-Dataset Validation
- **05_GSE161529_cross_validation.ipynb** [05_GSE161529_cross_validation.ipynb](./05_GSE161529_cross_validation.ipynb)  
   Cross-validation of trained model on GSE161529 dataset with tumor prediction generation.

- **08_GSE180286_cross_validation.ipynb** [08_GSE180286_cross_validation.ipynb](./08_GSE180286_cross_validation.ipynb)  
   Cross-validation of trained model on GSE180286 dataset with tumor prediction generation.

### Biological Analysis
- **06_GSE161529_oncogene.ipynb** [06_GSE161529_oncogene.ipynb](./06_GSE161529_oncogene.ipynb)  
   Oncogene expression analysis, differential expression testing, and pathway visualization for GSE161529.

- **09_GSE180286_oncogene.ipynb** [09_GSE180286_oncogene.ipynb](./09_GSE180286_oncogene.ipynb)  
   Oncogene expression analysis, differential expression testing, and pathway visualization for GSE180286.

### Comparative Analysis
- **10_Combined_DE.ipynb** [10_Combined_DE.ipynb](./10_Combined_DE.ipynb)  
   Combined differential expression analysis across datasets with drug target identification and clinical relevance assessment.

## Usage

1. Clone the repository and navigate to this folder.
2. Open notebooks using JupyterLab or Jupyter Notebook.
3. Follow the instructions in each notebook for reproducibility.

## Notes

- Notebooks are organized by topic and stage of the project.
- Please refer to individual notebook headers for specific details and requirements.
- For questions or contributions, see the main project README.
