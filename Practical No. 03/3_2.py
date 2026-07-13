from bs4 import BeautifulSoup

with open("example.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")
text = soup.get_text()

word = input("Enter the word to search: ")

if word.lower() in text.lower():
    print(f"The word '{word}' was found.")
else:
    print(f"The word '{word}' was not found.")