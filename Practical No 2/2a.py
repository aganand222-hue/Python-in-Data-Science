# 1. Create nested tuple with studentss
student1 = ("Shravan", 120)
student2 = ("Krish", 121)
student3 = ("Anand", 122)
nested_tuple = (student1, student2, student3)
print("Nested Tuple:", nested_tuple)
# 2. Indexing
print("First student tuple:", nested_tuple[0])
print("Name of second student:", nested_tuple[1][0])
# 3. Negative indexing
print("Last Student tuple (negative index):", nested_tuple[-1])
print("Name of last student:", nested_tuple[-1][0])
# 4. Loop through the nested tuple
print("\nAll Students:")
for student in nested_tuple:
    print(f"Student Name: {student[0]}, Code: {student[1]}")
reversed_tuple = nested_tuple[::-1]
print("\nReversed Tuple:", reversed_tuple)
# 6. Slice the tuple (first two students)
sliced_tuple = nested_tuple[0:2]
print("Sliced Tuple (first two students):", sliced_tuple)
# 7. Concatenate another students tuple
student4 = ("Joshua", 123)
updated_tuple = nested_tuple + (student4,)
print("After Concatenation:", updated_tuple)
# 8. Demonstrate immutability
try:
    nested_tuple[0][1] = 999 # Trying to change subject code
except TypeError as e:
    print("\nTuple Immutability Test: Error occurred ->", e)
