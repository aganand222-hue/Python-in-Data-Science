# a. Create a tuple with 5 different elements and print it
my_tuple = (120, 121, 122, 123, 124)
print("a. Tuple:", my_tuple)

# b. Access the first and last elements using indexing
print("b. First element:", my_tuple[0])
print("   Last element:", my_tuple[-1])

# c. Slice a tuple and print the middle 3 elements
middle_tuple = my_tuple[1:4]
print("c. Middle 3 elements:", middle_tuple)

# d. Concatenate two tuples and print the result
tuple1 = (120, 121, 122)
tuple2 = (123, 124, 125)
concat_tuple = tuple1 + tuple2
print("d. Concatenated tuple:", concat_tuple)

# e. Reverse a tuple using slicing
reversed_tuple = my_tuple[::-1]
print("e. Reversed tuple:", reversed_tuple)

# f. Count how many times an element appears in a tuple
count_tuple = (1, 2, 3, 2, 4, 2, 5)
count_element = 2
print("f. Count of", count_element, ":", count_tuple.count(count_element))

# g. Find the index of a specific element in a tuple
search_element = 4
print("g. Index of", search_element, ":", count_tuple.index(search_element))

# h. Check if an element exists in a tuple
check_element = 3
if check_element in count_tuple:
    print("h.", check_element, "exists in the tuple")
else:
    print("h.", check_element, "does not exist in the tuple")

# i. Convert a list to a tuple
my_list = [100, 200, 300, 400]
list_to_tuple = tuple(my_list)
print("i. List converted to tuple:", list_to_tuple)

# j. Sort a tuple of numbers in ascending order
unsorted_tuple = (50, 10, 40, 20, 30)
sorted_tuple = tuple(sorted(unsorted_tuple))
print("j. Sorted tuple:", sorted_tuple)

# k. Repeat a tuple 3 times using * operator
repeat_tuple = (1, 2, 3)
print("k. Tuple repeated 3 times:", repeat_tuple * 3)

# l. Check immutability property of tuples
immutable_tuple = (10, 20, 30)

try:
    immutable_tuple[0] = 100
except TypeError as e:
    print("l. Tuples are immutable.")
    print("   Error:", e)
