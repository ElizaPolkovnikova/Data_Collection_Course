# Урок 4. X-path
# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru. Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# 2. Сложить собранные новости в БД

import requests
from lxml import html
from pprint import pprint
import pymongo
from pymongo import MongoClient
import uuid  # библиотека для генерации id
import lesson_03_func as func
import connection as c
import json

# Работа с БД (создаем клиента и коллекцию в БД)
client = c.get_connection_to_my_cluster()
# client = MongoClient('127.0.0.1', 27017)
db = client['bd_education_new']
news_collection = db.news_collection
# news_collection.create_index([('link', pymongo.TEXT)], unique=True)  # создаем индекс по ссылке

# Парсим новости и по одной добавляем в БД
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
response = requests.get('https://news.mail.ru/economics/', headers=headers)
dom = html.fromstring(response.text)  # Преобразование тела документа из строки response.text в дерево элементов (DOM)


items = dom.xpath("//div[contains(@class, 'js-ago-wrapper')]")
duplicate_news = []  # список для новостей, не прошедших проверку на уникальность по ссылке или id
n = 1

for item in items:
    piece_of_news = {}
    source = item.xpath(".//span[@class='newsitem__param']/text()")  # 20 шт
    name = item.xpath(".//a[contains(@class,'newsitem__title')]//text()")  # 20 шт
    link = item.xpath(".//a[contains(@class,'newsitem__title')]/@href")  # 20 шт
    date = item.xpath(".//span[@class='newsitem__param js-ago']/text()")  # 20 шт

    piece_of_news['_id'] = str(uuid.uuid4())  # генерация id
    piece_of_news['source'] = source[0]
    piece_of_news['name'] = name[0]
    piece_of_news['link'] = link[0]
    piece_of_news['date'] = date[0]
    if func.add_unique_obj_to_db(piece_of_news, news_collection) is False:
        # Если документ уже есть в БД, добавляем в список дубликатов
        duplicate_news.append(piece_of_news)
    print(f'Обработана новость {n}')
    n += 1

print(f'Кол-во документов в БД: {db.news_collection.count_documents({})}')  # 20
print(f'Количество дубликатов: {len(duplicate_news)}. id или ссылка таких объектов уже есть в БД.')


# Проверка добавления документа с одинаковым id

# for piece_of_news in news_collection.find({"_id": "fb2f05af-b35c-4f90-8e02-2aa911513825"}):
#     if func.add_unique_obj_to_db(piece_of_news, news_collection) is False:
#         # Если документ уже есть в БД, добавляем в список дубликатов
#         duplicate_news.append(piece_of_news)
#
# print(duplicate_news)


# Собираем список дублированных новостей в json
with open('duplicate_news.json', 'w', encoding='utf-8') as f:
    json.dump(duplicate_news, f)

client.close()
