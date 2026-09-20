import pandas as pd

df = pd.read_csv("attendance.csv")

print("Original Dataset:")
print(df)

print("\nMissing Values:")
print(df.isnull())

print("\nCount of Missing Values:")
print(df.isnull().sum())

marks_mean = df["Marks"].mean()

df["Marks"] = df["Marks"].fillna(marks_mean)

attendance_mean = df["Attendance"].mean()

df["Attendance"] = df["Attendance"].fillna(attendance_mean)

print("\nCleaned Dataset:")
print(df)

print("S117 Shravan Ramesh Vishwakarma")