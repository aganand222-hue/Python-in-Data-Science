import pandas as pd

marks = pd.Series([45, 60, 75, 82, 39, 91])

print("Original Series:")
print(marks)

filtered = marks[marks > 50]

print("\nFiltered Series (Marks > 50):")
print(filtered)