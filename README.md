# Cleaning, Transformation, and Analysis of Home Visit Data by Health Agents in the City of Rio de Janeiro

This repository was initially created for a **Data Scientist position challenge** for the **Innovation and Technology Directorate of the Rio de Janeiro City Hall**, in the health department. However, I took the opportunity to go beyond and implement statistical analyses after cleaning and processing the data. See ```README_pt.md``` for a portuguese version of this README file.

The initial challenge involved analyzing, structuring, and transforming data provided in a file containing multiple entries from questionnaires filled out by health agents during home visits to patients. The data provides crucial registration information to understand the profile of each family and is constantly updated throughout the patient follow-up by CF/CMS. For an introduction to the data, refer to the file ```descricao_de_campos.xlsx```.

## Goals 🎯

- Understand the meaning of each column
- Detect issues (formatting errors, missing values, incorrect values, etc.)
- Solve the issues
- Extras: analyze the data and create a report using **Microsoft Power BI**

## Project Structure 📦

### 1. **`cleaning.py`**
This file contains the complete solution for the data cleaning and transformation process. In it, I performed the following steps:
- Identification and treatment of errors in the data
- Conversion of variable values to appropriate formats
- Creation of new variables, when necessary
- Final structuring of the data for analysis

### 2. **`exploring_data.ipynb`**
This file is a Jupyter notebook where I conducted the exploratory data analysis. In it, I aimed to:
- Identify patterns, trends, and inconsistencies in the data
- Investigate the possible causes of errors
- Suggest solutions to the problems found

## How to Use 💻

1. Download or clone the repository:
   ```bash
   git clone https://github.com/micahgcnavia/DIT-Test.git
   ```

2. Download the `dados_ficha_a_desafio.csv` file from the [Google Drive link](https://drive.google.com/file/d/1dWC1ZUPNlCQBalYPY8uP4Zzs0aue9nkQ/view?usp=sharing)

3. Change ```file_path``` in the .py and .ipynb files to the corresponding path of the file on your machine
