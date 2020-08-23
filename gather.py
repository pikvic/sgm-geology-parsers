import json
from pathlib import Path

elements_file1 = Path('uses/elements/elements_uses.json')
elements_file2 = Path('uses/elements/reallife_elements_uses.json')
minerals_file1 = Path('uses/gallerie_com/uses.json')
minerals_file2 = Path('uses/minerals_net/uses.json')
minerals_file3 = Path('uses/mineralseducationcoalition/uses.json')

elements1 = json.loads(open(elements_file1, 'rt').read())
elements2 = json.loads(open(elements_file2, 'rt').read())

elements = []
for e1, e2 in zip(elements1, elements2):
    element = {
        'id': e1['id'],
        'element': e1['element'],
        'uses': [
            e1['uses'],
            e2['uses']
        ]
    }
    elements.append(element)

minerals = []

minerals1 = json.loads(open(minerals_file1, 'rt').read())
minerals2 = json.loads(open(minerals_file2, 'rt').read())
minerals3 = json.loads(open(minerals_file3, 'rt').read())

def upsert(mineral):
    insert = True
    if not mineral:
        return
    if minerals:
        for i in range(len(minerals)):
            if minerals[i]['mineral'] == mineral['mineral']:
                insert = False
                minerals[i]['uses'].append(mineral['uses'])
                break
    if insert:
        mineral['uses'] = [mineral['uses']]
        minerals.append(mineral)

for mineral in minerals1:
    upsert(mineral)

for mineral in minerals2:
    upsert(mineral)

for mineral in minerals3:
    upsert(mineral)


minerals_file = Path('uses/minerals.json')
elements_file = Path('uses/elements.json')

open(minerals_file, 'wt').write(json.dumps(sorted(minerals, key=lambda m: m['mineral'])))
open(elements_file, 'wt').write(json.dumps(sorted(elements, key=lambda e: e['id'])))
