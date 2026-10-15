
from pathlib import Path
import pandas as pd

# Locate the project and its raw data folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Find CSV files
csv_files = list(RAW_DATA_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No CSV file found in {RAW_DATA_DIR}. "
        "Check that your dataset is inside data/raw/."
    )

if len(csv_files) > 1:
    raise ValueError(
        "Multiple CSV files found. Keep the intended dataset "
        "in data/raw/ or specify the filename explicitly."
    )

file_path = csv_files[0]

# Load the original data without modifying it
df = pd.read_csv(file_path, low_memory=False)

print("\n" + "=" * 60)
print("PERTH HOUSING DATA — INITIAL AUDIT")
print("=" * 60)

print(f"\nFile name: {file_path.name}")
print(f"File size: {file_path.stat().st_size / 1_000_000:.2f} MB")

print("\n1. DATASET SIZE")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\n2. COLUMN NAMES")
print(df.columns.tolist())

print("\n3. DATA TYPES")
print(df.dtypes.to_string())

print("\n4. FIRST FIVE ROWS")
print(df.head().to_string())

print("\n5. MISSING VALUES")
missing = pd.DataFrame({
    "missing_count": df.isna().sum(),
    "missing_percent": (df.isna().mean() * 100).round(2),
})
print(missing.to_string())

print("\n6. EXACT DUPLICATE ROWS")
print(f"Duplicate rows: {df.duplicated().sum():,}")

print("\n7. DISTINCT VALUES PER COLUMN")
print(df.nunique(dropna=True).to_string())

print("\n8. NUMERIC SUMMARY")
print(df.describe().T.to_string())

print("\n9. POSSIBLE DATE COLUMNS")
for col in df.columns:
    if any(word in col.lower() for word in ["date", "time", "sold"]):
        print(f"\n{col}")
        print(df[col].head(5).to_list())

print("\n" + "=" * 60)
print("INITIAL AUDIT COMPLETE — NO DATA CLEANING PERFORMED")
print("=" * 60)
