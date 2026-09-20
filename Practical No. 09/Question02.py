import pandas as pd

df = pd.read_csv("student_performance.csv")

print("Student Performance Dataset:")
print(df)

print("\nFirst 10 Records:")
print(df.head(10))

print("\nNumber of Students:")
print(len(df))

print("\nColumn Names:")
print(df.columns)

print("\nAverage Marks:")
print(df["Marks"].mean())

print("\nAverage Attendance:")
print(df["Attendance"].mean())

print("\nAverage Study Hours:")
print(df["Study_Hours"].mean())

print("S117 Shravan Ramesh Vishwakarma")