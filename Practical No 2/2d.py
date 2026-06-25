# Create a tuple
student = ("Shravan", 120)
# Try to modify an element in the tuple
try:
    student[1] = 222 # Attempt to change the subject code
except TypeError as e:
    print("Tuple is immutable! Error:", e)
