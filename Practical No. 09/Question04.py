import pandas as pd

df = pd.read_csv("sales.csv")

print("Sales in Ascending Order:")
print(df.sort_values("Sales"))

print("\nSales in Descending Order:")
print(df.sort_values("Sales", ascending=False))

print("\nQuantity in Descending Order:")
print(df.sort_values("Units", ascending=False))

print("\nTop 5 Sales Records:")
print(df.sort_values("Sales", ascending=False).head(5))

print("\nBottom 3 Sales Records:")
print(df.sort_values("Sales").head(3))

print("S117 Shravan Ramesh Vishwakarma")