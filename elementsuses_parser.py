import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json

elements = []

root = "https://interestingengineering.com/real-life-use-every-element-periodic-table"

response = requests.get(root)
if not response.ok:
    print("Error:", response.status_code)
    quit()
soup = BeautifulSoup(response.text, "html.parser")

blocks = soup.select('.content-text > p')
h2s = soup.select('.content-text > h2')

elements = []
uses = []
for block in blocks:
    if block.select('strong:contains("Where")'):
        uses.append(block.text.replace("Where It's Used:", '').strip())

for h2 in h2s:
    if not h2.select('img') and h2.text != 'Guide':
        elements.append(h2.text.lower())

results = []

for i, (name, use) in enumerate(zip(elements, uses)):
    results.append({'id': i + 1, 'element': name, 'uses': use})

filename = Path() / 'uses' / 'elements' / 'reallife_elements_uses.json'
with open(filename, 'wt') as f:
    json.dump(results, f)