import pandas as pd

df = pd.read_csv("movie_ratings.csv")

print("Number of Movies in Each Genre:")
print(df.groupby("Genre")["Movie"].count())

print("\nAverage Rating by Genre:")
print(df.groupby("Genre")["Rating"].mean())

print("\nMaximum Rating by Genre:")
print(df.groupby("Genre")["Rating"].max())

print("\nMinimum Rating by Genre:")
print(df.groupby("Genre")["Rating"].min())

print("\nAverage Release Year by Genre:")
print(df.groupby("Genre")["Year"].mean())

print("S117 Shravan Ramesh Vishwakarma")