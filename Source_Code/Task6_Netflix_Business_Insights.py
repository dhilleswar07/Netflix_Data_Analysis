# ============================================================
# TASK 6 - NETFLIX BUSINESS INSIGHTS
# Auspify Technologies - Data Analysis Using Python
# Author: DHILLESWAR JOGI
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

sns.set_style("whitegrid")

# ------------------------------------------------------------
# 1. CREATE OUTPUT FOLDER
# ------------------------------------------------------------

os.makedirs("../Analysis_Reports", exist_ok=True)

# ------------------------------------------------------------
# 2. LOAD CLEANED DATASET
# ------------------------------------------------------------

df = pd.read_csv("../Datasets/Netflix_Cleaned.csv")

print("=" * 70)
print("NETFLIX BUSINESS INSIGHTS REPORT")
print("=" * 70)

print("\nDataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Records:")
display(df.head())

# ------------------------------------------------------------
# 3. DATA QUALITY CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATA QUALITY CHECK")
print("=" * 70)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# ------------------------------------------------------------
# 4. STANDARDIZE COLUMNS
# ------------------------------------------------------------

for column in ["type", "country", "rating"]:
    if column in df.columns:
        df[column] = df[column].astype("string").str.strip()

df["type"] = df["type"].str.title()

# ------------------------------------------------------------
# 5. CONTENT TYPE ANALYSIS
# ------------------------------------------------------------

content_type_counts = df["type"].value_counts()

content_percentage = (
    df["type"].value_counts(normalize=True) * 100
).round(2)

print("\n" + "=" * 70)
print("CONTENT TYPE ANALYSIS")
print("=" * 70)

print("\nContent Counts:")
print(content_type_counts)

print("\nContent Percentage:")
print(content_percentage)

# Content Type Chart
plt.figure(figsize=(8, 5))

sns.barplot(
    x=content_type_counts.index,
    y=content_type_counts.values
)

plt.title("Netflix Content Type Distribution")
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 6. COUNTRY-WISE ANALYSIS
# ------------------------------------------------------------

country_df = df.copy()

country_df["country"] = (
    country_df["country"]
    .fillna("Unknown")
    .str.split(",")
)

country_exploded = country_df.explode("country")

country_exploded["country"] = (
    country_exploded["country"]
    .astype(str)
    .str.strip()
)

country_counts = (
    country_exploded["country"]
    .value_counts()
    .reset_index()
)

country_counts.columns = [
    "country",
    "content_count"
]

country_counts = country_counts[
    country_counts["country"] != "Unknown"
]

print("\n" + "=" * 70)
print("TOP 10 CONTENT-PRODUCING COUNTRIES")
print("=" * 70)

print(country_counts.head(10))

country_counts.to_csv(
    "../Analysis_Reports/Netflix_Country_Analysis.csv",
    index=False
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=country_counts.head(10),
    x="content_count",
    y="country"
)

plt.title("Top 10 Countries by Netflix Content")
plt.xlabel("Number of Titles")
plt.ylabel("Country")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 7. RELEASE YEAR TREND ANALYSIS
# ------------------------------------------------------------

year_counts = (
    df["release_year"]
    .value_counts()
    .sort_index()
    .reset_index()
)

year_counts.columns = [
    "release_year",
    "content_count"
]

print("\n" + "=" * 70)
print("RELEASE YEAR ANALYSIS")
print("=" * 70)

print(year_counts.tail(15))

year_counts.to_csv(
    "../Analysis_Reports/Netflix_Year_Analysis.csv",
    index=False
)

# Complete Release Year Trend
plt.figure(figsize=(12, 6))

sns.lineplot(
    data=year_counts,
    x="release_year",
    y="content_count"
)

plt.title("Netflix Content Releases by Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

plt.tight_layout()
plt.show()

# Recent Release Trend
recent_years = year_counts[
    year_counts["release_year"] >= 2000
]

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=recent_years,
    x="release_year",
    y="content_count"
)

plt.title("Netflix Content Releases Since 2000")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 8. RATING ANALYSIS
# ------------------------------------------------------------

rating_counts = (
    df["rating"]
    .fillna("Unknown")
    .value_counts()
    .reset_index()
)

rating_counts.columns = [
    "rating",
    "content_count"
]

print("\n" + "=" * 70)
print("RATING ANALYSIS")
print("=" * 70)

print(rating_counts)

rating_counts.to_csv(
    "../Analysis_Reports/Netflix_Rating_Analysis.csv",
    index=False
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=rating_counts.head(10),
    x="content_count",
    y="rating"
)

plt.title("Netflix Content Rating Distribution")
plt.xlabel("Number of Titles")
plt.ylabel("Rating")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 9. GENRE ANALYSIS
# ------------------------------------------------------------

genre_df = df.copy()

genre_df["listed_in"] = (
    genre_df["listed_in"]
    .fillna("Unknown")
)

genre_df["genre"] = (
    genre_df["listed_in"]
    .str.split(",")
)

genre_exploded = genre_df.explode("genre")

genre_exploded["genre"] = (
    genre_exploded["genre"]
    .astype(str)
    .str.strip()
)

genre_counts = (
    genre_exploded["genre"]
    .value_counts()
    .reset_index()
)

genre_counts.columns = [
    "genre",
    "content_count"
]

genre_counts = genre_counts[
    genre_counts["genre"] != "Unknown"
]

print("\n" + "=" * 70)
print("TOP 10 NETFLIX GENRES")
print("=" * 70)

print(genre_counts.head(10))

genre_counts.to_csv(
    "../Analysis_Reports/Netflix_Genre_Analysis.csv",
    index=False
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=genre_counts.head(10),
    x="content_count",
    y="genre"
)

plt.title("Top 10 Netflix Genres")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 10. RATING VS CONTENT TYPE
# ------------------------------------------------------------

rating_type = pd.crosstab(
    df["rating"].fillna("Unknown"),
    df["type"]
)

print("\n" + "=" * 70)
print("RATING BY CONTENT TYPE")
print("=" * 70)

print(rating_type)

rating_type.to_csv(
    "../Analysis_Reports/Netflix_Rating_Type_Analysis.csv"
)

plt.figure(figsize=(12, 6))

sns.countplot(
    data=df,
    x="rating",
    hue="type"
)

plt.title("Ratings by Content Type")
plt.xlabel("Rating")
plt.ylabel("Number of Titles")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 11. RATING PERCENTAGE HEATMAP
# ------------------------------------------------------------

rating_percentage = pd.crosstab(
    df["rating"].fillna("Unknown"),
    df["type"],
    normalize="columns"
) * 100

rating_percentage = rating_percentage.round(2)

plt.figure(figsize=(10, 7))

sns.heatmap(
    rating_percentage,
    annot=True,
    fmt=".1f",
    cmap="Blues"
)

plt.title("Rating Percentage by Content Type")
plt.xlabel("Content Type")
plt.ylabel("Rating")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 12. MOVIES VS TV SHOWS RELEASE TREND
# ------------------------------------------------------------

type_year = (
    df.groupby(
        ["release_year", "type"]
    )
    .size()
    .reset_index(name="content_count")
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=type_year,
    x="release_year",
    y="content_count",
    hue="type"
)

plt.title("Movies vs TV Shows Release Trend")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 13. BUSINESS KPIs
# ------------------------------------------------------------

total_titles = len(df)

total_movies = (
    df["type"]
    .str.lower()
    .eq("movie")
    .sum()
)

total_tv_shows = (
    df["type"]
    .str.lower()
    .eq("tv show")
    .sum()
)

unique_countries = (
    country_exploded[
        country_exploded["country"] != "Unknown"
    ]["country"]
    .nunique()
)

unique_genres = (
    genre_exploded[
        genre_exploded["genre"] != "Unknown"
    ]["genre"]
    .nunique()
)

most_common_rating = (
    df["rating"]
    .dropna()
    .value_counts()
    .idxmax()
)

most_common_genre = (
    genre_exploded[
        genre_exploded["genre"] != "Unknown"
    ]["genre"]
    .value_counts()
    .idxmax()
)

peak_release_year = (
    df["release_year"]
    .value_counts()
    .idxmax()
)

top_country = country_counts.iloc[0]["country"]

# ------------------------------------------------------------
# 14. DISPLAY BUSINESS KPIs
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NETFLIX BUSINESS KPIs")
print("=" * 70)

print(f"Total Titles        : {total_titles:,}")
print(f"Total Movies        : {total_movies:,}")
print(f"Total TV Shows      : {total_tv_shows:,}")
print(f"Unique Countries    : {unique_countries:,}")
print(f"Unique Genres       : {unique_genres:,}")
print(f"Most Common Rating  : {most_common_rating}")
print(f"Most Common Genre   : {most_common_genre}")
print(f"Peak Release Year   : {peak_release_year}")
print(f"Top Country         : {top_country}")

# ------------------------------------------------------------
# 15. BUSINESS INSIGHTS
# ------------------------------------------------------------

movie_percentage = (
    total_movies / total_titles
) * 100

tv_percentage = (
    total_tv_shows / total_titles
) * 100

print("\n" + "=" * 70)
print("BUSINESS INSIGHTS")
print("=" * 70)

print(
    f"1. Movies represent {movie_percentage:.2f}% "
    "of the analyzed Netflix titles."
)

print(
    f"2. TV Shows represent {tv_percentage:.2f}% "
    "of the analyzed Netflix titles."
)

print(
    f"3. {top_country} is the top content-producing country."
)

print(
    f"4. {most_common_genre} is the most common genre."
)

print(
    f"5. {most_common_rating} is the most common content rating."
)

print(
    f"6. {peak_release_year} is the peak release year."
)

# ------------------------------------------------------------
# 16. FINAL BUSINESS INSIGHTS REPORT
# ------------------------------------------------------------

final_summary = pd.DataFrame({
    "Metric": [
        "Total Titles",
        "Movies",
        "TV Shows",
        "Unique Countries",
        "Unique Genres",
        "Most Common Rating",
        "Most Common Genre",
        "Peak Release Year",
        "Top Content-Producing Country"
    ],

    "Value": [
        total_titles,
        total_movies,
        total_tv_shows,
        unique_countries,
        unique_genres,
        most_common_rating,
        most_common_genre,
        peak_release_year,
        top_country
    ]
})

display(final_summary)

final_summary.to_csv(
    "../Analysis_Reports/Netflix_Business_Insights_Report.csv",
    index=False
)

print(
    "\nNetflix Business Insights Report "
    "saved successfully."
)

# ------------------------------------------------------------
# 17. FINAL BUSINESS DASHBOARD
# ------------------------------------------------------------

fig, axes = plt.subplots(
    2,
    2,
    figsize=(16, 11)
)

# Chart 1 - Content Type
content_type_counts.plot(
    kind="bar",
    ax=axes[0, 0]
)

axes[0, 0].set_title(
    "Movies vs TV Shows"
)

axes[0, 0].set_xlabel(
    "Content Type"
)

axes[0, 0].set_ylabel(
    "Number of Titles"
)

axes[0, 0].tick_params(
    axis="x",
    rotation=0
)

# Chart 2 - Countries
sns.barplot(
    data=country_counts.head(10),
    x="content_count",
    y="country",
    ax=axes[0, 1]
)

axes[0, 1].set_title(
    "Top 10 Countries"
)

axes[0, 1].set_xlabel(
    "Number of Titles"
)

axes[0, 1].set_ylabel(
    "Country"
)

# Chart 3 - Release Trend
sns.lineplot(
    data=year_counts,
    x="release_year",
    y="content_count",
    ax=axes[1, 0]
)

axes[1, 0].set_title(
    "Netflix Release Year Trend"
)

axes[1, 0].set_xlabel(
    "Release Year"
)

axes[1, 0].set_ylabel(
    "Number of Titles"
)

# Chart 4 - Genres
sns.barplot(
    data=genre_counts.head(10),
    x="content_count",
    y="genre",
    ax=axes[1, 1]
)

axes[1, 1].set_title(
    "Top 10 Genres"
)

axes[1, 1].set_xlabel(
    "Number of Titles"
)

axes[1, 1].set_ylabel(
    "Genre"
)

# Dashboard title
plt.suptitle(
    "NETFLIX BUSINESS INSIGHTS DASHBOARD",
    fontsize=20,
    fontweight="bold"
)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 18. COMPLETION MESSAGE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TASK 6 - NETFLIX BUSINESS INSIGHTS")
print("COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated Reports:")

print("1. Netflix_Country_Analysis.csv")
print("2. Netflix_Year_Analysis.csv")
print("3. Netflix_Rating_Analysis.csv")
print("4. Netflix_Genre_Analysis.csv")
print("5. Netflix_Rating_Type_Analysis.csv")
print("6. Netflix_Business_Insights_Report.csv")

print("\nFinal dashboard generated successfully.")