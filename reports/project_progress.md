# Perth Housing Market Analysis

## 1. Project Overview

**Project type:** End-to-end data analytics project  
**Location of analysis:** Perth, Western Australia  
**Dataset:** `all_perth_310121.csv`  
**Tools:** Python, Pandas, Git, GitHub, and Power BI (planned)

### Objective

The objective of this project is to analyse historical Perth property sales data, identify meaningful patterns and trends, investigate data-quality issues, and develop an interactive Power BI dashboard.

The project follows a structured analytics workflow, from initial data auditing and cleaning to exploratory data analysis, visualisation, and business insights.

## 2. Project Structure

The project is organised into the following folders:

- `data/raw/` — Original source dataset.
- `data/processed/` — Data prepared for analysis.
- `notebooks/` — Exploratory data analysis and experiments.
- `src/` — Reusable Python scripts.
- `sql/` — SQL queries for future analysis.
- `powerbi/` — Power BI dashboard files.
- `reports/` — Project documentation and findings.

## 3. Dataset Overview

The original dataset contains **33,656 rows and 19 columns**.

The available fields cover property addresses, suburbs, sale prices, bedrooms, bathrooms, garages, land and floor areas, construction years, distances to the CBD and nearby facilities, sale dates, postcodes, coordinates, and school information.

The sale dates span April 1988 to December 2020.

## 4. Work Completed

### 4.1 Project Setup

- Created the project folder structure.
- Downloaded the source CSV and placed it in `data/raw/`.
- Created and activated a Python virtual environment.
- Installed Pandas and its required dependencies.

### 4.2 Initial Data Audit

Created and executed `src/data_audit.py`.

The audit examined:

- Dataset dimensions and column names.
- Data types.
- Missing values.
- Exact duplicate rows.
- Distinct values in each column.
- Numeric summary statistics.
- Initial distributions and ranges.

The initial audit found no exact duplicate rows.

### 4.3 Data Quality Checks

Created and executed `src/data_quality_checks.py`.

Checks included invalid or non-positive prices, room counts, land and floor areas, garage values, coordinate ranges, construction years, sale-date parsing, and extreme measurements.

No non-positive prices, bedroom counts, bathroom counts, land areas, or floor areas were identified. No coordinates fell outside the standard latitude and longitude ranges.

### 4.4 Missing Data

Three columns contain missing values:

| Column | Missing records | Percentage |
|---|---:|---:|
| NEAREST_SCH_RANK | 10,952 | 32.54% |
| BUILD_YEAR | 3,155 | 9.37% |
| GARAGE | 2,478 | 7.36% |

These values will be investigated before deciding how to handle them. Missing garage values will not automatically be treated as zero.

### 4.5 Outlier and Anomaly Investigation

The initial checks identified:

- 102 records with garage counts of 10 or more.
- 80 records with seven or more bedrooms.
- 10 records with six or more bathrooms.
- 2,018 records with land areas of at least 10,000.
- Two records with floor areas of 10 or less.

These thresholds identify records for investigation; they do not establish that every flagged value is incorrect. Large land areas may be legitimate for rural properties.

### 4.6 Duplicate Candidate Investigation

An initial review identified five rows belonging to two potential duplicate groups:

- Three records for 123 Fairway, Crawley.
- Two records for 4 Carmel Road, Carmel.

The Crawley records share the same visible sale and property details but have slightly different coordinates and nearby-school distances.

These records have not been removed. Further investigation is required before making a decision.

### 4.7 Sale-Date and Distribution Checks

The sale-date strings contain extra whitespace in the raw CSV. The dates can be parsed successfully after trimming whitespace.

The dataset contains records from 1988 to 2020, with the largest annual counts occurring in the later years. The year distribution will be considered when analysing historical trends.

## 5. Current Data Quality Assessment

The dataset is suitable for continued exploratory investigation, subject to further validation.

The following decisions remain open:

- Confirming whether potential duplicate records represent repeated observations or duplicate transactions.
- Investigating implausible floor-area and property-feature values.
- Determining suitable treatments for missing values.
- Verifying dataset provenance, licensing, and measurement units.
- Establishing documented cleaning rules before producing the processed dataset.

The original CSV remains unchanged. No source records have been deleted.

## 6. Next Steps

1. Complete the duplicate-record investigation.
2. Verify the dataset's source documentation and licence.
3. Define and document cleaning rules.
4. Create a reproducible data-cleaning script.
5. Save a processed dataset separately from the original.
6. Perform exploratory data analysis to identify price patterns and relationships.
7. Develop visualisations and key findings.
8. Build an interactive Power BI dashboard.
9. Document project outcomes and publish an appropriate GitHub portfolio repository.

## 7. Project Status

**Completed:** Initial project setup, dataset audit, basic data-quality checks, and preliminary anomaly investigation.

**In progress:** Record-level investigation and preparation for reproducible data cleaning.

**Planned:** Data cleaning, exploratory analysis, visualisation, Power BI dashboard development, and GitHub portfolio publication.