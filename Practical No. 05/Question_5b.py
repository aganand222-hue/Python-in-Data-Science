import pandas as pd

# Read the Excel dataset
df = pd.read_excel("StressLevelDataset.xlsx")

# Display first 5 rows
print("Dataset:")
print(df.head())

# Display statistical information
print("\nStatistical Information:")
print(df.describe())