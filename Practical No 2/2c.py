# Original list
original_list = ["Shravan", "Rohit", "Saadan", "Anand"]
# Method 1: Using slicing
copy1 = original_list[:]
# Method 2: Using list() constructor
copy2 = list(original_list)
# Method 3: Using copy() method
copy3 = original_list.copy()
# Print all lists
print("Original List:", original_list)
print("Copy using slicing:", copy1)
print("Copy using list():", copy2)
print("Copy using copy():", copy3)
