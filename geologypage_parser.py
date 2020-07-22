import requests
from bs4 import BeautifulSoup
from pathlib import Path

# bad 154 - check

def save_image(url, path):
    with open(path, "wb") as f:
        f.write(requests.get(url).content)

def parse_page(url, mineral):
    results = []
    response = requests.get(url)
    if not response.ok:
        print("Error:", response.status_code)
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.select("article figure img")
    print("Images:", len(images))
    for i, image in enumerate(images):
        img_url = image.get("src")
        results.append(img_url)
        ext = img_url.split('.')[-1]
        save_image(img_url, Path("images") / f"{mineral}_{i}.{ext}")
    return results

url = "http://www.geologypage.com/minerals"
response = requests.get(url)

if not response.ok:
    print("Error!")
    quit()

soup = BeautifulSoup(response.text, "html.parser")
pages = soup.select("td.style3 > ul > li > a")
for i, page in enumerate(pages[154:]):
    #print(page.get("href"), page.text)
    page_url = page.get("href")
    print(f"Parsing page {i}/{len(pages)}... Mineral: {page.text.strip()} Url: {page_url}")
    parse_page(page_url, page.text.strip())