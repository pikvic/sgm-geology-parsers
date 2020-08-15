import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json

def save_image(url, path):
    with open(path, "wb") as f:
        f.write(requests.get(url).content)

def parse_page(url, mineral):
    result = None
    response = requests.get(url)
    if not response.ok:
        print("Error:", response.status_code)
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    uses = soup.select("#ctl00_ContentPlaceHolder1_lblUses")
    if uses:
        result = {'mineral': mineral, 'uses': uses[0].text}
    return result

root = 'https://www.minerals.net/'
url = 'https://www.minerals.net/MineralMain.aspx'
response = requests.get(url)

if not response.ok:
    print("Error!")
    quit()

soup = BeautifulSoup(response.text, "html.parser")
pages = soup.select("#ctl00_ContentPlaceHolder1_DataList1 td a")

print("Pages found:", len(pages))
minerals = []

for i, page in enumerate(pages):
    
    page_url = root + page.get("href")
    name = page.text.strip().capitalize()
    print(f"Parsing page {i + 1}/{len(pages)}... Mineral: {name} Url: {page_url}")
    mineral = parse_page(page_url, name)
    minerals.append(mineral)

filename = Path() / 'uses' / 'minerals_net' / 'uses.json'
with open(filename, 'wt') as f:
    json.dump(minerals, f)
