import requests
from bs4 import BeautifulSoup

url = "https://www.wikipedia.org/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/151.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, "html.parser")

    print("\n===== FIRST 3 PARAGRAPHS =====")

    paragraphs = soup.find_all("p")

    if paragraphs:
        for i, p in enumerate(paragraphs[:3], 1):
            print("Paragraph", i, ":", p.get_text(" ", strip=True))
    else:
        print("No paragraphs found.")

    print("\n===== IMAGE URLs =====")

    images = soup.find_all("img")

    if images:
        for i, img in enumerate(images, 1):
            src = img.get("src")

            if src:
                print("Image", i, ":", src)
    else:
        print("No images found.")

    print("\n===== TOTAL LINKS =====")

    links = soup.find_all("a", href=True)

    print("Total number of links:", len(links))

    print("\n===== HEADINGS =====")

    headings = soup.find_all(["h1", "h2", "h3"])

    if headings:
        for heading in headings:
            print(heading.get_text(" ", strip=True))
    else:
        print("No headings found.")

    print("\n===== LANGUAGES =====")

    languages = soup.select(".central-featured-lang")

    if languages:
        for language in languages:

            name = language.find("strong")

            if name:
                print(name.get_text(" ", strip=True))
    else:
        print("No languages found.")

else:
    print("Failed to access Wikipedia.")
    print("Status Code:", response.status_code)

print("S117 Shravan Ramesh Vishwakarma")