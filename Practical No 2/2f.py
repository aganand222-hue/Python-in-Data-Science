# a. Find the largest number in a list
numbers = [120, 121, 122, 123, 124]
largest = max(numbers)
print("a. Largest number:", largest)

# b. Remove duplicates from a list
duplicate_list = [1, 2, 3, 2, 4, 1, 5]
unique_list = list(set(duplicate_list))
print("b. List after removing duplicates:", unique_list)

# c. Count how many even numbers are in a list
num_list = [10, 15, 20, 25, 30, 35, 40]
even_count = 0

for num in num_list:
    if num % 2 == 0:
        even_count += 1

print("c. Number of even numbers:", even_count)

# d. Input 5 numbers and store them in a list
user_numbers = []

print("d. Enter 5 numbers:")
for i in range(5):
    num = int(input(f"Enter number {i+1}: "))
    user_numbers.append(num)

print("   List entered by user:", user_numbers)

# e. Function to return the average of all numbers in a list
def calculate_average(lst):
    return sum(lst) / len(lst)

average = calculate_average(numbers)
print("e. Average of numbers list:", average)

# f. Convert a string into a list of characters using list()
text = "Shravan"
char_list = list(text)
print("f. String converted to list:", char_list)

# g. Join all elements of a list into a single string using join()
words = ["Shravan", "Ramesh", "Vishwakarma"]
joined_string = " ".join(words)
print("g. Joined string:", joined_string)
