
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
files = list((ROOT / "data" / "raw").glob("*.csv"))

if len(files) != 1:
    raise ValueError(f"Expected one CSV file, found {len(files)}")

df = pd.read_csv(files[0], low_memory=False)

# Standardise text only for investigation; do not modify the source file.
for col in ["ADDRESS", "SUBURB", "DATE_SOLD", "NEAREST_STN", "NEAREST_SCH"]:
    df[col] = df[col].astype("string").str.strip()

print("=" * 65)
print("RECORD INVESTIGATION")
print("=" * 65)

# 1. Check the three suspicious address examples
print("\n1. RECORDS FOR 123 FAIRWAY, CRAWLEY")

example = df[
    df["ADDRESS"].str.casefold().eq("123 fairway")
    & df["SUBURB"].str.casefold().eq("crawley")
]

print("Number of matching rows:", len(example))
if not example.empty:
    print(example.to_string(index=False))

# 2. Find records with matching address, suburb, postcode,
#    price and sale month.
# These are duplicate candidates, not confirmed errors.
key = ["ADDRESS", "SUBURB", "POSTCODE", "PRICE", "DATE_SOLD"]

candidate_mask = df.duplicated(subset=key, keep=False)
candidates = df.loc[candidate_mask].sort_values(key)

print("\n2. POSSIBLE DUPLICATE TRANSACTION RECORDS")
print("Rows in candidate groups:", len(candidates))

if not candidates.empty:
    print(candidates[
        ["ADDRESS", "SUBURB", "POSTCODE", "PRICE", "DATE_SOLD",
         "BEDROOMS", "BATHROOMS", "GARAGE", "LAND_AREA", "FLOOR_AREA"]
    ].head(30).to_string(index=False))

# 3. Investigate particularly unusual measurements
print("\n3. VERY SMALL FLOOR AREAS")
print(df.loc[df["FLOOR_AREA"] <= 10, [
    "ADDRESS", "SUBURB", "PRICE", "BEDROOMS",
    "BATHROOMS", "LAND_AREA", "FLOOR_AREA"
]].to_string(index=False))

print("\n4. EXTREME GARAGE VALUES")
print(df.loc[df["GARAGE"] >= 30, [
    "ADDRESS", "SUBURB", "PRICE", "GARAGE"
]].to_string(index=False))

print("\n5. EXTREME BATHROOM VALUES")
print(df.loc[df["BATHROOMS"] >= 10, [
    "ADDRESS", "SUBURB", "PRICE", "BATHROOMS"
]].to_string(index=False))

print("\n6. EXTREME LAND AREA VALUES")
print(df.loc[df["LAND_AREA"] >= 100_000, [
    "ADDRESS", "SUBURB", "PRICE", "LAND_AREA", "FLOOR_AREA"
]].to_string(index=False))

# 4. Understand how sales are distributed across years
print("\n7. SALES RECORDS BY YEAR")

dates = pd.to_datetime(
    df["DATE_SOLD"],
    format="%m-%Y",
    errors="coerce"
)

year_counts = dates.dt.year.value_counts().sort_index()
print(year_counts.to_string())

print("\n8. MISSINGNESS BY FIELD")
print(
    df.isna().sum()
      .loc[lambda s: s > 0]
      .sort_values(ascending=False)
      .to_string()
)

print("\nInvestigation complete. No source records were deleted.")
