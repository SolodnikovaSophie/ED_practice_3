from bs4 import BeautifulSoup
import re
import math
import collections
import json
import pandas as pd

#Определим функцию, которая поможет считывать большое количество html-файлов


def handle_file(file_name):

     with open(file_name, encoding= "utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        item = dict()

        site = BeautifulSoup(text, 'html.parser')
        genre_row = site.html.body.div.div.span.get_text()
        item['genre'] = genre_row.strip().split(":")[1].strip()
        item['title'] = site.find_all("h1")[0].get_text().strip()
        item['author'] = site.find_all("p")[0].get_text().strip()
        item['pages'] = int(site.find_all("span", attrs= {'class': 'pages'})[0].get_text().split(":")[1].strip().split()[0])
        item['year'] = site.find_all("span", attrs={'class': 'year'})[0].get_text().split("в")[1].strip().split("в")[-1]
        item['isbn'] = site.find_all("span", string = re.compile("ISBN"))[0].get_text().split(":")[1]
        item['description'] = site.find_all("p")[1].get_text().replace("Описание", "").strip()
        item['img_url'] = site.find_all("img")[0]['src']
        item['rating'] = site.find_all("span", string= re.compile("Рейтинг:"))[0].get_text().split(":")[1].strip()
        item['views'] = site.find_all("span", string=re.compile("Просмотры:"))[0].get_text().split(":")[1].strip()

        return item

items = []
for i in range(1, 999):
    file_name = f"1_3_data/{i}.html"
    items.append(handle_file(file_name))

#print(items)

items_sort = sorted(items, key=lambda x: x['views'], reverse=True)

filtered_items = []
for book in items:
    if book ['genre'] != 'любовный роман':
        filtered_items.append((book))


json_items = json.dumps(items)

with open("res_1_3_var95.json", "w", encoding="utf-8") as f:
    f.write(json_items)


# Посчитаем для одного выбранного числового поля статистические характеристики (сумма, мин/макс, среднее и т.д.)
# В качестве целевого поля выберем рейтинг

result = []

df = pd.DataFrame(items)
#print(df)
pd.set_option('display.float_format', '{:.1f}'.format)

res = df['pages'].agg(['sum', 'max', 'min', 'mean', 'median', 'average']).to_dict()
result.append(res)

#print(result)

# Для одного текстового поля посчитайте частоту меток

book = [item['author'] for item in items]
ss = collections.Counter(book)
result.append(ss)
#print(result)


with open('result_1_3_var95.json', 'w', encoding = 'utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

with open("result.json", "w", encoding = 'utf-8') as file:
    file.write(json.dumps(result, ensure_ascii=False))


# print(item.get("year"))
# print(item.get("pages"))
# print(item.get("author"))
# print(item.get("title"))
# print(item.get("genre"))
#print(item['description'])
#print(item.get("img_url"))
#print(item.get('rating'))
# print(item.get('views'))
#print((item))
