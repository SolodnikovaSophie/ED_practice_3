#Исследовать структуру html-файлов, чтобы произвести парсинг всех данных.
# В каждом файле содержится информация об одном или нескольких объектах из случайной предметной области.
# Перечень всех характеристик объекта может меняться (у отдельного объекта могут отсутствовать некоторые характеристики).
# Полученные данные собрать и записать в json. Выполните также ряд операций с данными:

#- отсортируйте значения по одному из доступных полей
# -выполните фильтрацию по другому полю (запишите результат отдельно)
# - для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
# - для одного текстового поля посчитайте частоту меток

from bs4 import BeautifulSoup
import re
import math
import collections
import json
import pandas as pd

#Определим функцию, которая поможет считывать большое количество html-файлов


def handle_file(file_name):

    items = list()
    with open(file_name, encoding= "utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text,'html.parser')
        products = site.find_all("div", attrs={'class': 'product-item'})
        #print(len(products))

        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = product.find_all("img")[0]['src']
            item['title'] = product.find_all('span')[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace("₽", "").replace(" ", "").strip())
            item['bonus'] = int(product.strong.get_text().replace("+ начислим ", "").replace("бонусов", "").strip())

            props = product.ul.find_all("li")
            for prop in props:
                item[prop['type']] = prop.get_text().strip()
            #print(item)
            items.append(item)
    return items

items = []
for i in range(1, 69):
    file_name = f"2_3_data/{i}.html"
    items += handle_file(file_name)

print(len(items))

items_sort = sorted(items, key=lambda x: x['price'], reverse=True)
#print(items[1:100])

filtered_items = []
for product in items:
    if product ['price'] < 350000:
        filtered_items.append((product))

json_items = json.dumps(items)

with open("res_2_3_var95.json", "w", encoding="utf-8") as f:
    f.write(json_items)

# Посчитаем для одного выбранного числового поля статистические характеристики (сумма, мин/макс, среднее и т.д.)
# В качестве целевого поля выберем рейтинг

result = []

df = pd.DataFrame(items)
#print(df)
pd.set_option('display.float_format', '{:.1f}'.format)

res = df['bonus'].agg(['sum', 'max', 'min', 'mean', 'median', 'average']).to_dict()
result.append(res)

#print(result)

# Для одного текстового поля посчитайте частоту меток

book = [item['title'] for item in items]
ss = collections.Counter(product)
result.append(ss)
#print(result)


with open('result_2_3_var95.json', 'w', encoding = 'utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

with open("result_2.json", "w", encoding = 'utf-8') as file:
    file.write(json.dumps(result, ensure_ascii=False))