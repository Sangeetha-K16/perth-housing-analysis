
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

csv_files = list(RAW_DIR.glob("*.csv"))

if len(csv_files) != 1:
    raise ValueError(
        f"Expected exactly one CSV in {RAW_DIR}, "
        f"but found {len(csv_files)}."
    )

df = pd.read_csv(csv_files[0], low_memory=False)

print("=" * 65)
print("PERTH HOUSING — DATA QUALITY INVESTIGATION")
print("=" * 65)

# 1. Check invalid or unusual numeric values
print("\n1. BASIC VALIDITY CHECKS")

checks = {
    "Price <= 0": df["PRICE"] <= 0,
    "Bedrooms <= 0": df["BEDROOMS"] <= 0,
    "Bathrooms <= 0": df["BATHROOMS"] <= 0,
    "Garage < 0": df["GARAGE"] < 0,
    "Land area <= 0": df["LAND_AREA"] <= 0,
    "Floor area <= 0": df["FLOOR_AREA"] <= 0,
    "Latitude outside -90 to 90":
        ~df["LATITUDE"].between(-90, 90),
    "Longitude outside -180 to 180":
        ~df["LONGITUDE"].between(-180, 180),
}

for label, condition in checks.items():
    print(f"{label}: {int(condition.sum())}")

# 2. Investigate extreme values — these are flags, not deletions
print("\n2. EXTREME VALUE COUNTS")

extreme_checks = {
    "Garage >= 10": df["GARAGE"] >= 10,
    "Bedrooms >= 7": df["BEDROOMS"] >= 7,
    "Bathrooms >= 6": df["BATHROOMS"] >= 6,
    "Land area >= 10,000": df["LAND_AREA"] >= 10_000,
    "Floor area <= 10": df["FLOOR_AREA"] <= 10,
    "Floor area >= 500": df["FLOOR_AREA"] >= 500,
    "Build year > 2021": df["BUILD_YEAR"] > 2021,
}

for label, condition in extreme_checks.items():
    print(f"{label}: {int(condition.sum())}")

# Show the records behind some of the flags
print("\n3. EXAMPLE EXTREME RECORDS")
for col, threshold in [
    ("GARAGE", 10),
    ("BATHROOMS", 6),
    ("LAND_AREA", 10_000),
    ("FLOOR_AREA", 500),
]:
    flagged = df.loc[df[col] >= threshold,
                     ["ADDRESS", "SUBURB", "PRICE", col]]
    print(f"\n{col} >= {threshold}:")
    print(flagged.head(10).to_string(index=False))

# 4. Inspect date formatting and coverage
print("\n4. DATE INVESTIGATION")

date_text = df["DATE_SOLD"].astype("string").str.strip()
parsed_dates = pd.to_datetime(
    date_text,
    format="%m-%Y",
    errors="coerce"
)

print("Unparsed dates:", int(parsed_dates.isna().sum()))
print("Earliest sale month:", parsed_dates.min())
print("Latest sale month:", parsed_dates.max())
print("\nMost common original date values:")
print(df["DATE_SOLD"].value_counts().head(10).to_string())

# 5. Investigate repeated addresses
print("\n5. REPEATED ADDRESS INVESTIGATION")

normalised_address = (
    df["ADDRESS"]
    .astype("string")
    .str.strip()
    .str.casefold()
)

print(
    "Rows with a repeated normalised address:",
    int(normalised_address.duplicated(keep=False).sum())
)

address_counts = normalised_address.value_counts()
repeated_addresses = address_counts[address_counts > 1]

print("Number of address labels appearing more than once:",
      len(repeated_addresses))

if not repeated_addresses.empty:
    sample_addresses = repeated_addresses.head(10).index
    examples = df.loc[
        normalised_address.isin(sample_addresses),
        ["ADDRESS", "SUBURB", "PRICE", "DATE_SOLD", "POSTCODE"]
    ]
    print("\nExamples:")
    print(examples.sort_values("ADDRESS").to_string(index=False))

print("\n6. PRICE DISTRIBUTION")
print(df["PRICE"].quantile(
    [0, 0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99, 1]
).to_string())

print("\nInvestigation complete. No records were modified or deleted.")
