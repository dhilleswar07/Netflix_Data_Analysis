# ==========================================
# TASK 4 - TREND ANALYSIS BY RELEASE YEAR
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


# ------------------------------------------
# 1. LOAD CLEANED DATASET
# ------------------------------------------

df = pd.read_csv("Netflix_Cleaned.csv")

print("=" * 60)
print("       NETFLIX TREND ANALYSIS BY RELEASE YEAR")
print("=" * 60)

print("\nDataset Shape:", df.shape)


# ------------------------------------------
# 2. CALCULATE YEARLY CONTENT RELEASES
# ------------------------------------------

year_counts = (
    df["release_year"]
    .value_counts()
    .sort_index()
)

year_analysis = year_counts.reset_index()

year_analysis.columns = [
    "Release_Year",
    "Content_Count"
]

print("\nYearly Content Releases:")
print(year_analysis.head())


# ------------------------------------------
# 3. CREATE RECENT YEAR DATA
# ------------------------------------------

recent_years = year_analysis[
    year_analysis["Release_Year"] >= 2000
]


# ------------------------------------------
# 4. OVERALL TREND
# ------------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    year_analysis["Release_Year"],
    year_analysis["Content_Count"],
    marker="o"
)

plt.title("Netflix Content Releases by Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

plt.show()


# ------------------------------------------
# 5. RECENT TREND
# ------------------------------------------

plt.figure(figsize=(14, 6))

sns.lineplot(
    data=recent_years,
    x="Release_Year",
    y="Content_Count",
    marker="o"
)

plt.title("Netflix Content Release Trend Since 2000")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

plt.show()


# ------------------------------------------
# 6. FIND PEAK YEAR
# ------------------------------------------

peak_year = year_counts.idxmax()
peak_count = year_counts.max()

print("\nPeak Release Year:", peak_year)
print("Number of Titles:", peak_count)


# ------------------------------------------
# 7. FIND LOWEST YEAR
# ------------------------------------------

lowest_year = year_counts.idxmin()
lowest_count = year_counts.min()

print("\nLowest Release Year:", lowest_year)
print("Number of Titles:", lowest_count)


# ------------------------------------------
# 8. MOVIES VS TV SHOWS
# ------------------------------------------

year_type = (
    df.groupby(["release_year", "type"])
    .size()
    .reset_index(name="Content_Count")
)

recent_year_type = year_type[
    year_type["release_year"] >= 2000
]

plt.figure(figsize=(14, 7))

sns.lineplot(
    data=recent_year_type,
    x="release_year",
    y="Content_Count",
    hue="type",
    marker="o"
)

plt.title("Movies vs TV Shows Release Trend Since 2000")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")

plt.legend(title="Content Type")

plt.show()


# ------------------------------------------
# 9. YEAR-TO-YEAR CHANGE
# ------------------------------------------

year_analysis["Yearly_Change"] = (
    year_analysis["Content_Count"].diff()
)

year_analysis["Growth_Percentage"] = (
    year_analysis["Content_Count"].pct_change() * 100
)


# ------------------------------------------
# 10. TOP 10 RELEASE YEARS
# ------------------------------------------

top_release_years = (
    df["release_year"]
    .value_counts()
    .head(10)
)

print("\n===== TOP 10 RELEASE YEARS =====")
print(top_release_years)


# ------------------------------------------
# 11. TOP 10 RELEASE YEARS CHART
# ------------------------------------------

plt.figure(figsize=(12, 6))

sns.barplot(
    x=top_release_years.values,
    y=top_release_years.index.astype(str)
)

plt.title("Top 10 Years by Netflix Content Releases")
plt.xlabel("Number of Titles")
plt.ylabel("Release Year")

plt.show()


# ------------------------------------------
# 12. BUSINESS INSIGHTS
# ------------------------------------------

print("\n" + "=" * 60)
print("             TASK 4 BUSINESS INSIGHTS")
print("=" * 60)

print(
    f"\n1. Peak release year: {peak_year}"
)

print(
    f"2. Titles released in peak year: {peak_count}"
)

print(
    f"3. Lowest release year: {lowest_year}"
)

print(
    f"4. Titles released in lowest year: {lowest_count}"
)

print(
    "\n5. Release-year analysis helps identify "
    "content production trends over time."
)

print(
    "6. Movies and TV Shows can be compared to "
    "understand changes in Netflix's content mix."
)


# ------------------------------------------
# 13. EXPORT RESULTS
# ------------------------------------------

year_analysis.to_csv(
    "Netflix_Year_Analysis.csv",
    index=False
)

print("\nTask 4 results saved as:")
print("Netflix_Year_Analysis.csv")

print("\nTASK 4 COMPLETED SUCCESSFULLY!")