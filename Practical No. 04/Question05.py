import numpy as np

arr = np.array([15, 42, 67, 23, 67, 10, 55])

# Find maximum value
max_value = np.max(arr)

# Filter array to return only maximum values
filtered_arr = arr[arr == max_value]

print("Original Array:", arr)
print("Maximum Value:", max_value)
print("Filtered Array:", filtered_arr)
print("S117 Shravan Ramesh Vishwakarma")