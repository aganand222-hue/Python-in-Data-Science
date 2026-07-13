with open("sample.txt", "r") as file:
    text = file.read()

word = input("Enter the word to search: ")

if word.lower() in text.lower():
    print(f"The word '{word}' was found.")
else:
    print(f"The word '{word}' was not found.")