# ==========================================
# TASK 3 - COUNTRY-WISE NETFLIX ANALYSIS
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


# ------------------------------------------
# 1. LOAD CLEANED DATASET
# ------------------------------------------

df = pd.read_csv("Netflix_Cleaned.csv")

print("=" * 55)
print("       COUNTRY-WISE NETFLIX CONTENT ANALYSIS")
print("=" * 55)

print("\nDataset Shape:", df.shape)


# ------------------------------------------
# 2. CLEAN COUNTRY INFORMATION
# ------------------------------------------

df["country"] = df["country"].astype(str).str.strip()

country_df = df.copy()

# Split multiple countries
country_df["country"] = country_df["country"].str.split(",")

# Create separate row for each country
country_df = country_df.explode("country")

# Remove extra spaces
country_df["country"] = country_df["country"].str.strip()


# ------------------------------------------
# 3. COUNT CONTENT BY COUNTRY
# ------------------------------------------

country_counts = country_df["country"].value_counts()

print("\nTop 10 Countries:")
print(country_counts.head(10))


# ------------------------------------------
# 4. CREATE COUNTRY RANKING
# ------------------------------------------

country_ranking = country_counts.reset_index()

country_ranking.columns = [
    "Country",
    "Content_Count"
]

country_ranking["Rank"] = (
    country_ranking["Content_Count"]
    .rank(method="dense", ascending=False)
    .astype(int)
)

country_ranking = country_ranking[
    ["Rank", "Country", "Content_Count"]
]


# ------------------------------------------
# 5. TOP 10 COUNTRIES
# ------------------------------------------

top_10_countries = country_counts.head(10)

print("\n===== TOP 10 CONTENT-PRODUCING COUNTRIES =====")

print(top_10_countries)


# ------------------------------------------
# 6. VISUALIZATION
# ------------------------------------------

plt.figure(figsize=(12, 6))

sns.barplot(
    x=top_10_countries.values,
    y=top_10_countries.index
)

plt.title("Top 10 Countries by Netflix Content")
plt.xlabel("Number of Titles")
plt.ylabel("Country")

plt.show()


# ------------------------------------------
# 7. MOVIES VS TV SHOWS BY COUNTRY
# ------------------------------------------

country_type = (
    country_df
    .groupby(["country", "type"])
    .size()
    .unstack(fill_value=0)
)

top_country_names = country_counts.head(10).index

top_country_type = country_type.loc[
    country_type.index.intersection(top_country_names)
]

top_country_type.plot(
    kind="bar",
    figsize=(14, 7)
)

plt.title("Movies vs TV Shows in Top Netflix Countries")
plt.xlabel("Country")
plt.ylabel("Number of Titles")

plt.xticks(rotation=45)

plt.legend(title="Content Type")

plt.tight_layout()

plt.show()


# ------------------------------------------
# 8. TOP COUNTRY
# ------------------------------------------

top_country = country_counts.index[0]
top_country_count = country_counts.iloc[0]

print("\nTop Content-Producing Country:")
print(top_country)

print("\nNumber of Titles:")
print(top_country_count)


# ------------------------------------------
# 9. BUSINESS INSIGHTS
# ------------------------------------------

print("\n" + "=" * 55)
print("             TASK 3 BUSINESS INSIGHTS")
print("=" * 55)

print(
    f"\n{top_country} has the highest number "
    f"of Netflix titles in the dataset."
)

print(
    f"It has approximately {top_country_count} titles."
)

print("\nTop 5 countries:")

for i, (country, count) in enumerate(
    country_counts.head(5).items(),
    start=1
):
    print(f"{i}. {country}: {count} titles")


# ------------------------------------------
# 10. EXPORT RESULTS
# ------------------------------------------

country_ranking.to_csv(
    "Netflix_Country_Analysis.csv",
    index=False
)

print("\nCountry analysis saved as:")
print("Netflix_Country_Analysis.csv")

print("\nTASK 3 COMPLETED SUCCESSFULLY!")