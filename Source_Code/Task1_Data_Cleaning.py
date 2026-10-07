import pandas as pd
import numpy as np
from IPython.display import display

import warnings

warnings.filterwarnings("ignore")

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv(r"E:\Netflix_Data_Analysis\Datasets\Dataset.csv")

print("=" * 50)
print("NETFLIX DATA CLEANING & PREPARATION")
print("=" * 50)

print("\nOriginal Dataset Shape:", df.shape)


# ==========================================
# 2. CHECK MISSING VALUES
# ==========================================

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())


# ==========================================
# 3. CHECK DUPLICATES
# ==========================================

print("\nDuplicate Rows Before Cleaning:")
print(df.duplicated().sum())


# ==========================================
# 4. REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates()


# ==========================================
# 5. STANDARDIZE TEXT COLUMNS
# ==========================================

text_columns = [
    "type",
    "title",
    "director",
    "country",
    "rating",
    "duration",
    "listed_in"
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()


# ==========================================
# 6. STANDARDIZE TYPE
# ==========================================

df["type"] = df["type"].str.title()


# ==========================================
# 7. STANDARDIZE RATING
# ==========================================

df["rating"] = df["rating"].str.upper()


# ==========================================
# 8. CONVERT DATE
# ==========================================

df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)


# ==========================================
# 9. CREATE DATE FEATURES
# ==========================================

df["date_added_year"] = df["date_added"].dt.year

df["date_added_month"] = df["date_added"].dt.month

df["date_added_month_name"] = (
    df["date_added"].dt.month_name()
)


# ==========================================
# 10. CLEAN DURATION
# ==========================================

df["duration_value"] = (
    df["duration"]
    .str.extract(r"(\d+)")
    .astype(float)
)


# ==========================================
# 11. FINAL VALIDATION
# ==========================================

print("\nFinal Dataset Shape:", df.shape)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nDuplicate Rows After Cleaning:")
print(df.duplicated().sum())


# ==========================================
# 12. DISPLAY CLEANED DATA
# ==========================================

print("\nCleaned Dataset:")
display(df.head(5))


# ==========================================
# 13. EXPORT CLEANED DATASET
# ==========================================

df.to_csv(
    "Netflix_Cleaned.csv",
    index=False
)

print("\n" + "=" * 50)
print("TASK 1 COMPLETED SUCCESSFULLY")
print("Cleaned file: Netflix_Cleaned.csv")
print("=" * 50)