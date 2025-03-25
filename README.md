# Cleaning, Transformation, and Analysis of Home Visit Data by Health Agents in the City of Rio de Janeiro

This repository was initially created for a **Data Scientist position challenge** for the **Innovation and Technology Directorate of the Rio de Janeiro City Hall**, in the health department. However, I took the opportunity to go beyond and implement statistical analyses after cleaning and processing the data. See ```README_pt.md``` for a portuguese version of this README file.

The initial challenge involved analyzing, structuring, and transforming data provided in a file containing multiple entries from questionnaires filled out by public health agents during home visits to patients. The data provides crucial registration information to understand the profile of each family and is constantly updated throughout the patient follow-up by CF/CMS.

## Goals 🎯

- Understand the meaning of each column
- Detect issues (formatting errors, missing values, incorrect values, etc.)
- Solve the issues
- Extras: analyze the data and create a report using **Microsoft Power BI**

## Project Structure 📦

### 1. **`exploring_data.ipynb`**
This file is a Jupyter notebook where I conducted the exploratory data analysis. In it, I aimed to:
- Identify patterns, trends, and inconsistencies in the data
- Investigate the possible causes of errors
- Suggest solutions to the problems found

### 2. **`cleaning.py`**
This file contains the complete solution for the data cleaning and transformation process. In it, I performed the following steps:
- Identification and treatment of errors in the data
- Conversion of variable values to appropriate formats
- Creation of new columns, when necessary
- Final structuring of the data for analysis

## How to Use 💻

1. Download or clone the repository into your machine:
   ```bash
   git clone https://github.com/micahgcnavia/Home_Visits_Public_Health_RJ.git
   ```
2. Run `cleaning.py` to get the clean table ready for analysis
3. Check the final dashboard directly by downloading the file `dashboard.pbix` or visit the [report site](https://app.powerbi.com/reportEmbed?reportId=d145b337-32d0-4f60-bd09-98865e847c13&autoAuth=true&ctid=8a425f8e-ceea-4039-8816-b9cb7af9f4cd) (you might need a Microsoft Power BI account to open the dashboard).

### Citation 📰

If you feel like using this data in your own projects, please consider citing this repository! Thank you! :)
