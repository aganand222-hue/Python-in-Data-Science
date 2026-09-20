import pandas as pd

df = pd.read_csv("students.csv")

print("Complete Dataset:")
print(df)

print("\nFirst 5 Records:")
print(df.head(5))

print("\nLast 5 Records:")
print(df.tail(5))

print("\nNumber of Rows and Columns:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nDataset Information:")
df.info()

print("\nStatistical Information:")
print(df.describe())

print("S117 Shravan Ramesh Vishwakarma")