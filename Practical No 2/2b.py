# Original nested tuple of students
nested_tuple = (
("Shravan", 120),
("Rohit", 122),
("Anand", 121)
)
# Sorting the nested tuple by students code (index 1)
sorted_students = sorted(nested_tuple, key=lambda x: x[1])
# Display the sorted result
print("Sorted Studentss (by subject code):", sorted_students)
