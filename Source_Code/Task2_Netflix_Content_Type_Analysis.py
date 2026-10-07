import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# ==========================================
# TASK 2 - NETFLIX CONTENT TYPE ANALYSIS
# ==========================================

# Load cleaned dataset
df = pd.read_csv(r"E:\Netflix_Data_Analysis\Datasets\Netflix_Cleaned.csv")

print("=" * 50)
print("NETFLIX CONTENT TYPE ANALYSIS")
print("=" * 50)

# ------------------------------------------
# 1. Count Movies and TV Shows
# ------------------------------------------

content_counts = df["type"].value_counts()

print("\nNumber of Movies and TV Shows:")
print(content_counts)


# ------------------------------------------
# 2. Calculate Percentages
# ------------------------------------------

content_percentage = (
    df["type"]
    .value_counts(normalize=True) * 100
)

print("\nPercentage Distribution:")
print(content_percentage.round(2))


# ------------------------------------------
# 3. Create Summary Table
# ------------------------------------------

content_summary = pd.DataFrame({
    "Content Type": content_counts.index,
    "Number of Titles": content_counts.values,
    "Percentage": content_percentage.round(2).values
})

print("\nSummary:")
display(content_summary)


# ------------------------------------------
# 4. Bar Chart
# ------------------------------------------

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="type"
)

plt.title("Netflix Movies vs TV Shows")
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")

plt.show()


# ------------------------------------------
# 5. Pie Chart
# ------------------------------------------

plt.figure(figsize=(7, 7))

plt.pie(
    content_counts.values,
    labels=content_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Netflix Content Type Distribution")

plt.show()


# ------------------------------------------
# 6. Find Most Common Type
# ------------------------------------------

most_common_type = content_counts.idxmax()
most_common_count = content_counts.max()

print("\nMost Common Content Type:", most_common_type)
print("Number of Titles:", most_common_count)


# ------------------------------------------
# 7. Compare Movies and TV Shows
# ------------------------------------------

movie_count = content_counts.get("Movie", 0)
tv_show_count = content_counts.get("TV Show", 0)

difference = abs(movie_count - tv_show_count)

print("\nMovies:", movie_count)
print("TV Shows:", tv_show_count)
print("Difference:", difference)


# ------------------------------------------
# 8. Business Insight
# ------------------------------------------

print("\n========== TASK 2 INSIGHT ==========")

if movie_count > tv_show_count:
    print(
        f"Movies are more common than TV Shows "
        f"by {difference} titles."
    )
elif tv_show_count > movie_count:
    print(
        f"TV Shows are more common than Movies "
        f"by {difference} titles."
    )
else:
    print(
        "Movies and TV Shows have the same number "
        "of titles."
    )