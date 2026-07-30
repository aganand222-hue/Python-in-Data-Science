import pandas as pd

student = {
    "Amit": 85,
    "Priya": 90,
    "Rahul": 78,
    "Sneha": 88
}

series = pd.Series(student)

print("Pandas Series:")
print(series)