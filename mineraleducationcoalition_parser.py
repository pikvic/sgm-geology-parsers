import requests
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from time import sleep
import json

def save_image(url, path):
    with open(path, "wb") as f:
        f.write(requests.get(url).content)


def parse_page(url, mineral):
    response = requests.get(url)
    if not response.ok:
        print("Error:", response.status_code)
        return None
    soup = BeautifulSoup(response.text, "html.parser")
   
    images = soup.select(".acf-image-gallery a")
    uses = soup.select('article h3:contains("Uses") ~ p')
    print("Images:", len(images), "Uses:", len(uses))
    # for i, image in enumerate(images):
    #     img_url = image.get("href")
    #     ext = img_url.split('.')[-1]
    #     save_image(img_url, Path("images") / 'mineralseducationcoalition' /  f"{mineral}_{i}.{ext}")

    text = []
    for use in uses:
        text.append(use.text.strip())
    text = '\n'.join(text)

    result = {'mineral': mineral, 'uses': text}
    return result

url = 'https://mineralseducationcoalition.org/mining-minerals-information/minerals-database/?tax=mineral-category,0;&pa=10'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=options)
browser.get(url)
sleep(3)
generated_html = browser.page_source
browser.quit()

soup = BeautifulSoup(generated_html, "html.parser")
pages = soup.select("a.minerals-article")
print("Pages found:", len(pages))
#pages = pages[:2]
minerals = []
for i, page in enumerate(pages):
    page_url = page.get("href")
    name = page.find("h2").text.strip().replace('/', ' ')
    print(f"Parsing page {i + 1}/{len(pages)}... Mineral: {name} Url: {page_url}")
    mineral = parse_page(page_url, name)
    minerals.append(mineral)
    
filename = Path() / 'uses' / 'mineralseducationcoalition' / 'uses.json'
with open(filename, 'wt') as f:
    json.dump(minerals, f)