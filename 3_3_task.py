from bs4 import BeautifulSoup
import lxml
import math
import collections
import json
import pandas as pd

def handle_file(file_name):

    items = list()
    with open(file_name, encoding = 'utf-8') as f:
        text = ""
        for row in f.readlines():
            text += row

        site = BeautifulSoup(text, 'xml')
        item = dict()
        item['name'] = site.find_all("name")[0].get_text().strip()
        item['constellation'] = site.find_all("constellation")[0].get_text().strip()
        item['spectral-class'] = site.find_all("spectral-class")[0].get_text().strip()
        item['radius'] = int(site.find_all("radius")[0].get_text().strip())
        item['rotation'] = site.find_all("rotation")[0].get_text().strip()
        item['age'] = site.find_all("age")[0].get_text().strip()
        item['distance'] = site.find_all("distance")[0].get_text().strip()
        item['absolute-magnitude'] = site.find_all("absolute-magnitude")[0].get_text().strip()

        return item

items = []
for i in range(1, 500):
    file_name = f"3_3_data/{i}.xml"
    items.append(handle_file(file_name))

#print(items)


items_sort = sorted(items, key=lambda x: x['radius'], reverse=True)

filtered_items = []
for star in items:
    if star ['constellation'] == 'Близнецы':
        filtered_items.append((star))

json_items = json.dumps(items)

with open("filtered_result_3_3_var95.json", "w", encoding="utf-8") as f:
    f.write(json_items)

# Посчитаем для одного выбранного числового поля статистические характеристики (сумма, мин/макс, среднее и т.д.)
# В качестве целевого поля выберем рейтинг

result = []

df = pd.DataFrame(items)
#print(df)
pd.set_option('display.float_format', '{:.1f}'.format)

res = df['radius'].agg(['sum', 'max', 'min', 'mean', 'median', 'average']).to_dict()
result.append(res)

#print(result)

# Для одного текстового поля посчитайте частоту меток

star = [item['name'] for item in items]
ss = collections.Counter(star)
result.append(ss)
#print(result)


with open('result_3_3_var95.json', 'w', encoding = 'utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

with open("result_3.json", "w", encoding = 'utf-8') as file:
    file.write(json.dumps(result, ensure_ascii=False))



