import pandas as pd

df = pd.read_csv("product_sales.csv")

print("Average Revenue:")
print(df["Revenue"].mean())

print("\nMaximum Revenue:")
print(df["Revenue"].max())

print("\nMinimum Revenue:")
print(df["Revenue"].min())

print("\nMedian Revenue:")
print(df["Revenue"].median())

print("\nStandard Deviation of Revenue:")
print(df["Revenue"].std())

print("\nAverage Quantity Sold:")
print(df["Quantity"].mean())

print("\nNumber of Products:")
print(df["Product"].count())

print("\nProducts with Revenue Above 200000:")
print((df["Revenue"] > 200000).sum())

print("S117 Shravan Ramesh Vishwakarma")