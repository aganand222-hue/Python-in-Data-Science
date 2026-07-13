text_to_search = input("Enter the text: ")

search_word = input("Enter the word to search for: ")

if search_word in text_to_search:
    print(f"The word '{search_word}' was found in the text.")
else:
    print(f"The word '{search_word}' was NOT found in the text.")