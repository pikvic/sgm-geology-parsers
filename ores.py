import json
from pathlib import Path

elements_file = Path('uses/elements.json')
minerals_file = Path('uses/minerals.json')

elements = json.loads(open(elements_file, 'rt').read())
minerals = json.loads(open(minerals_file, 'rt').read())

ores = []

for mineral in minerals:
    ore = False
    for use in mineral['uses']:
        if ' ore ' in use.lower():
            ore = True
            break
    if ore:
        ores.append(mineral)

print(len(ores))