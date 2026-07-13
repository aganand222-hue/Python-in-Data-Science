from bs4 import BeautifulSoup

# Open the HTML file
with open("sample.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Retrieve the title
print("Title:", soup.title.string)

# Retrieve all headings (h1)
for heading in soup.find_all("h1"):
    print("Heading:", heading.text)

# Retrieve all paragraphs
for para in soup.find_all("p"):
    print("Paragraph:", para.text)