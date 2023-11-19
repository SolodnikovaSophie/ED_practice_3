from bs4 import BeautifulSoup
import lxml
import math
import collections
import json
import pandas as pd

def handle_file(file_name):

    items = list()
    with (open(file_name, encoding = 'utf-8') as f):
        text = ""
        for row in f.readlines():
            text += row

        root = BeautifulSoup(text, 'xml')

        for clothing in root.find_all("clothing"):
            item = dict()
            for el in clothing.contents:
                if el.name is None:
                    continue
                elif el.name == "price" or el.name == "reviews":
                    item[el.name] = int(el.get_text().strip())
                elif el.name == "rating":
                    item[el.name] = float(el.get_text().strip())
                elif el.name == "new":
                    item[el.name] = el.get_text().strip() == "+"
                elif el.name == "exclusive" or el.name == "sporty":
                    item[el.name] = el.get_text().strip() == "yes"
                else:
                    item[el.name] = el.get_text().strip()

            items.append(item)

    return items

items = []
for i in range(1, 98):
    file_name = f"4_3_data/{i}.xml"
    items += handle_file(file_name)

#print(len(items))

items_sort = sorted(items, key=lambda x: x['price'], reverse=True)
#print(items[1:100])

filtered_items = []
for clothes in items:
    if clothes ['size'] != ('S' and 'L'):
        filtered_items.append((clothes))
#print(filtered_items)

json_items = json.dumps(items)

with open("res_4_3_var95.json", "w", encoding="utf-8") as f:
    f.write(json_items)

result = []

df = pd.DataFrame(items)
#print(df)
pd.set_option('display.float_format', '{:.1f}'.format)

res = df['price'].agg(['sum', 'max', 'min', 'mean', 'median', 'average']).to_dict()
result.append(res)

#print(result)

# Для одного текстового поля посчитайте частоту меток

color = [item['color'] for item in items]
ss = collections.Counter(color)
result.append(ss)
#print(result)

with open('result_4_3_var95.json', 'w', encoding = 'utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

with open("result_4_statistical.json", "w", encoding = 'utf-8') as file:
    file.write(json.dumps(result, ensure_ascii=False))
