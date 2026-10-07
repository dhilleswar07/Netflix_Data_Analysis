# ==========================================
# TASK 5 - CONTENT RATING & GENRE ANALYSIS
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


# ------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------

df = pd.read_csv("Netflix_Cleaned.csv")

print("=" * 60)
print("       NETFLIX CONTENT RATING & GENRE ANALYSIS")
print("=" * 60)

print("\nDataset Shape:", df.shape)


# ------------------------------------------
# 2. CLEAN IMPORTANT COLUMNS
# ------------------------------------------

# Remove leading/trailing spaces
df["type"] = df["type"].astype(str).str.strip()
df["rating"] = df["rating"].astype(str).str.strip()
df["listed_in"] = df["listed_in"].astype(str).str.strip()

# Standardize content type
df["type"] = df["type"].replace({
    "movie": "Movie",
    "MOVIE": "Movie",
    "Movie ": "Movie",
    "tv show": "TV Show",
    "TV SHOW": "TV Show",
    "TV Show ": "TV Show"
})

# Replace string "nan" with actual missing values
df["rating"] = df["rating"].replace("nan", pd.NA)
df["listed_in"] = df["listed_in"].replace("nan", pd.NA)

print("\n===== CONTENT TYPE COUNTS =====")
print(df["type"].value_counts(dropna=False))


# ------------------------------------------
# 3. RATING ANALYSIS
# ------------------------------------------

rating_counts = df["rating"].dropna().value_counts()

print("\n===== RATING DISTRIBUTION =====")
print(rating_counts)


# ------------------------------------------
# 4. RATING VISUALIZATION
# ------------------------------------------

if not rating_counts.empty:

    plt.figure(figsize=(12, 6))

    sns.countplot(
        data=df,
        y="rating",
        order=rating_counts.index
    )

    plt.title("Netflix Content Rating Distribution")
    plt.xlabel("Number of Titles")
    plt.ylabel("Rating")

    plt.tight_layout()
    plt.show()

else:
    print("\nNo rating data available for visualization.")


# ------------------------------------------
# 5. RATING SUMMARY
# ------------------------------------------

rating_summary = rating_counts.reset_index()

rating_summary.columns = [
    "Rating",
    "Number_of_Titles"
]


# ------------------------------------------
# 6. GENRE ANALYSIS
# ------------------------------------------

genre_df = df.copy()

# Remove missing genres
genre_df = genre_df.dropna(subset=["listed_in"])

# Split multiple genres
genre_df["listed_in"] = genre_df["listed_in"].str.split(",")

# Create separate row for every genre
genre_df = genre_df.explode("listed_in")

# Remove extra spaces
genre_df["listed_in"] = genre_df["listed_in"].str.strip()

# Remove empty values
genre_df = genre_df[
    genre_df["listed_in"].notna()
    & (genre_df["listed_in"] != "")
]

genre_counts = genre_df["listed_in"].value_counts()

print("\n===== TOP 20 GENRES =====")
print(genre_counts.head(20))


# ------------------------------------------
# 7. TOP 10 GENRES
# ------------------------------------------

top_10_genres = genre_counts.head(10)

if not top_10_genres.empty:

    plt.figure(figsize=(12, 6))

    sns.barplot(
        x=top_10_genres.values,
        y=top_10_genres.index
    )

    plt.title("Top 10 Netflix Genres")
    plt.xlabel("Number of Titles")
    plt.ylabel("Genre")

    plt.tight_layout()
    plt.show()

else:
    print("\nNo genre data available.")


# ------------------------------------------
# 8. GENRE SUMMARY
# ------------------------------------------

genre_summary = genre_counts.reset_index()

genre_summary.columns = [
    "Genre",
    "Number_of_Titles"
]


# ------------------------------------------
# 9. RATING VS CONTENT TYPE
# ------------------------------------------

rating_type = (
    df.dropna(subset=["rating", "type"])
    .groupby(["rating", "type"])
    .size()
    .reset_index(name="Number_of_Titles")
)

print("\n===== RATING VS CONTENT TYPE =====")
print(rating_type)


# ------------------------------------------
# 10. RATING VS CONTENT TYPE VISUALIZATION
# ------------------------------------------

if not rating_type.empty:

    plt.figure(figsize=(14, 7))

    sns.countplot(
        data=df.dropna(subset=["rating", "type"]),
        y="rating",
        hue="type",
        order=rating_counts.index
    )

    plt.title("Netflix Ratings: Movies vs TV Shows")
    plt.xlabel("Number of Titles")
    plt.ylabel("Rating")

    plt.legend(title="Content Type")

    plt.tight_layout()
    plt.show()

else:
    print("\nNo rating/type data available.")


# ------------------------------------------
# 11. RATING PERCENTAGE
# ------------------------------------------

rating_type_percentage = pd.crosstab(
    df["rating"],
    df["type"],
    normalize="columns"
) * 100

print("\n===== RATING PERCENTAGE BY CONTENT TYPE =====")
print(rating_type_percentage.round(2))


# ------------------------------------------
# 12. HEATMAP
# ------------------------------------------

if not rating_type_percentage.empty:

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        rating_type_percentage,
        annot=True,
        fmt=".1f"
    )

    plt.title("Rating Distribution by Content Type (%)")
    plt.xlabel("Content Type")
    plt.ylabel("Rating")

    plt.tight_layout()
    plt.show()

else:
    print("\nNo data available for heatmap.")


# ------------------------------------------
# 13. MOST COMMON RATING
# ------------------------------------------

if not rating_counts.empty:

    most_common_rating = rating_counts.idxmax()
    most_common_rating_count = rating_counts.max()

    print("\nMost Common Rating:")
    print(most_common_rating)

    print("Number of Titles:")
    print(most_common_rating_count)

else:

    most_common_rating = "N/A"
    most_common_rating_count = 0

    print("\nNo rating data available.")


# ------------------------------------------
# 14. MOST COMMON GENRE
# ------------------------------------------

if not genre_counts.empty:

    most_common_genre = genre_counts.idxmax()
    most_common_genre_count = genre_counts.max()

    print("\nMost Common Genre:")
    print(most_common_genre)

    print("Number of Titles:")
    print(most_common_genre_count)

else:

    most_common_genre = "N/A"
    most_common_genre_count = 0

    print("\nNo genre data available.")


# ------------------------------------------
# 15. MOVIE RATING
# ------------------------------------------

movie_ratings = (
    df[
        df["type"].str.lower().str.strip() == "movie"
    ]["rating"]
    .dropna()
    .value_counts()
)

if not movie_ratings.empty:

    top_movie_rating = movie_ratings.idxmax()

    print("\nMost Common Movie Rating:")
    print(top_movie_rating)

else:

    top_movie_rating = "N/A"

    print("\nNo Movie rating data found.")


# ------------------------------------------
# 16. TV SHOW RATING
# ------------------------------------------

tv_ratings = (
    df[
        df["type"].str.lower().str.strip().isin(
            ["tv show", "tv shows"]
        )
    ]["rating"]
    .dropna()
    .value_counts()
)

if not tv_ratings.empty:

    top_tv_rating = tv_ratings.idxmax()

    print("\nMost Common TV Show Rating:")
    print(top_tv_rating)

else:

    top_tv_rating = "N/A"

    print("\nNo TV Show rating data found.")


# ------------------------------------------
# 17. CONTENT TYPE SUMMARY
# ------------------------------------------

print("\n===== CONTENT TYPE SUMMARY =====")

content_type_counts = df["type"].value_counts()

print(content_type_counts)


# ------------------------------------------
# 18. BUSINESS INSIGHTS
# ------------------------------------------

print("\n" + "=" * 60)
print("             TASK 5 BUSINESS INSIGHTS")
print("=" * 60)

print(
    f"\n1. Most common rating: {most_common_rating}"
)

print(
    f"2. Most common genre: {most_common_genre}"
)

print(
    f"3. Most common Movie rating: {top_movie_rating}"
)

print(
    f"4. Most common TV Show rating: {top_tv_rating}"
)

print(
    "\n5. Rating analysis helps identify the primary "
    "audience segments targeted by Netflix."
)

print(
    "6. Genre analysis identifies the most represented "
    "content categories."
)

print(
    "7. Comparing Movies and TV Shows reveals differences "
    "in content targeting."
)


# ------------------------------------------
# 19. EXPORT RESULTS
# ------------------------------------------

rating_summary.to_csv(
    "Netflix_Rating_Analysis.csv",
    index=False
)

genre_summary.to_csv(
    "Netflix_Genre_Analysis.csv",
    index=False
)

rating_type.to_csv(
    "Netflix_Rating_Type_Analysis.csv",
    index=False
)

content_type_counts.reset_index().rename(
    columns={
        "type": "Content_Type",
        "count": "Number_of_Titles"
    }
).to_csv(
    "Netflix_Content_Type_Analysis.csv",
    index=False
)


# ------------------------------------------
# 20. FINAL STATUS
# ------------------------------------------

print("\n" + "=" * 60)
print("             TASK 5 COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nFiles created successfully:")

print("1. Netflix_Rating_Analysis.csv")
print("2. Netflix_Genre_Analysis.csv")
print("3. Netflix_Rating_Type_Analysis.csv")
print("4. Netflix_Content_Type_Analysis.csv")

print("\n" + "=" * 60)