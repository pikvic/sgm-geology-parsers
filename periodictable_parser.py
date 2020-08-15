import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json


def save_image(url, path):
    with open(path, "wb") as f:
        f.write(requests.get(url).content)

def parse_page(url, page):
    result = None
    response = requests.get(url)
    if not response.ok:
        print("Error:", response.status_code)
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    name = soup.select("span.element_header")[0].text.strip().lower()
    uses = soup.select(".acc_blk > div.accordian_block:nth-child(3) > div.accordian_details")[0].text.strip()
    result = {'id': page, 'element': name, 'uses': uses}
    return result

elements = []

root = "https://www.rsc.org/periodic-table/element/"
pages = list(range(1, 119))

#pages = [1, 2]
results = []

for i, page in enumerate(pages):
    url = root + str(page)
    print(f"Parsing page {i + 1}/{len(pages)}... Url: {url}")
    res = parse_page(url, page)
    results.append(res)

filename = Path() / 'uses' / 'elements' / 'elements_uses.json'
with open(filename, 'wt') as f:
    json.dump(results, f)