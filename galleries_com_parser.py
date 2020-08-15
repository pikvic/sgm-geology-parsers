import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json


def parse_page(url, mineral):
    result = None
    response = requests.get(url)
    if not response.ok:
        print("Error:", response.status_code)
        return None
    soup = BeautifulSoup(response.text, "html5lib")
    uses = soup.select('li:contains("Uses")')
    if uses:
        return {'mineral': mineral, 'uses': uses[0].text.replace("Uses:", '').strip().capitalize()}
    
    uses = soup.select('li:contains("USES")')
    if uses:
        return {'mineral': mineral, 'uses': uses[0].text.replace("USES:", '').strip().capitalize()}
    
    
    
root = 'http://www.galleries.com'
url = 'http://www.galleries.com/Minerals_By_Name'
response = requests.get(url)

if not response.ok:
    print("Error!")
    quit()

soup = BeautifulSoup(response.text, "html.parser")
pages = soup.select("dd > b > a")

print("Pages found:", len(pages))
minerals = []

for i, page in enumerate(pages):
    page_url = root + page.get("href")
    name = page.text.strip().capitalize()
    print(f"Parsing page {i + 1}/{len(pages)}... Mineral: {name} Url: {page_url}")
    mineral = parse_page(page_url, name)
    if mineral:
        minerals.append(mineral)


filename = Path() / 'uses' / 'gallerie_com' / 'uses.json'
with open(filename, 'wt') as f:
    json.dump(minerals, f)
