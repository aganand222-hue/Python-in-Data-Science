import pandas as pd

df = pd.read_csv("employee_salary.csv")

print("Employee Name and Salary:")
print(df[["Name", "Salary"]])

print("\nEmployees with Salary Greater Than 60000:")
print(df[df["Salary"] > 60000])

print("\nEmployees with Experience Greater Than 5 Years:")
print(df[df["Experience"] > 5])

print("\nIT Department Employees:")
print(df[df["Department"] == "IT"])

print("\nEmployees Below Age 30:")
print(df[df["Age"] < 30])

print("\nEmployees Satisfying Both Conditions:")
print(df[(df["Salary"] > 50000) & (df["Experience"] > 3)])

print("S117 Shravan Ramesh Vishwakarma")