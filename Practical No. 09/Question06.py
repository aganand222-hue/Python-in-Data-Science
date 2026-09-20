import pandas as pd

df = pd.read_csv("employee_data.csv")

def performance_level(score):
    if score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Very Good"
    elif score >= 70:
        return "Good"
    else:
        return "Needs Improvement"

df["Performance_Level"] = df["Performance"].apply(performance_level)

def salary_category(salary):
    if salary >= 70000:
        return "High"
    elif salary >= 50000:
        return "Medium"
    else:
        return "Low"

df["Salary_Category"] = df["Salary"].apply(salary_category)

print("Updated Employee Dataset:")
print(df)

print("S117 Shravan Ramesh Vishwakarma")