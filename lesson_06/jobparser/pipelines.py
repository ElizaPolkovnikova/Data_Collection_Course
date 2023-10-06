# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient
from connection import get_connection_to_my_cluster as c
import pymongo
from pymongo.errors import DuplicateKeyError
import regex


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        # client = c.get_connection_to_my_cluster()
        self.mongo_base = client['jobs']  # создаем БД

    def process_item(self, item, spider):
        collection = self.db[spider.name]  # создаем коллекцию по имени паука
        new_item = self.create_new_item(item)
        try:
            collection.insert_one(new_item)
        except DuplicateKeyError:
            print(f"Document with _id {new_item.get('_id')} already exists")
        return new_item

    @staticmethod
    def create_new_item(item):
        new_item = item.deepcopy()
        del new_item['salary']
        new_item['salary_min'] = None
        new_item['salary_max'] = None
        new_item['salary_cur'] = None
        if item['salary']:
            salary = [el.replace(u'\xa0', '') for el in item['salary']]
            for ind, el in enumerate(salary):
                if el.isdigit():
                    if salary[ind - 1].strip() == 'от':
                        new_item['salary_min'] = int(el)
                    elif salary[ind - 1].strip() == 'до':
                        new_item['salary_max'] = int(el)
            new_item['salary_cur'] = regex.findall(r'\p{Sc}', ''.join(item['salary']))[0]
        return new_item

