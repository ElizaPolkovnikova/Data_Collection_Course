# Урок 3. Парсинг данных. HTML, Beautiful Soap
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import uuid



# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии в вашу базу.

def add_unique_vacancy_to_db(vacancy_info, collection):
    """Добавляет уникальную вакансию в базу данных.
    Дубликаты """
    try:
        collection.insert_one(vacancy_info)
    except DuplicateKeyError:
        collection.append(vacancy_info)
        print(f"Document with id {vacancy_info.get('_id')} already exists")

# vacancy_info['_id'] = uuid.uuid4()  # генерация id


# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
# больше введённой суммы (необходимо анализировать оба поля зарплаты, то есть цифра вводится одна,
# а запрос проверяет оба поля)


def get_vacancies_gt_input(collection, salary_input):
    """Получить вакансии с з/п больше введенной суммы
    c анализом по двум полям"""

    collection.find({'$or': [{'min_salary': {'$gt': salary_input}},
                             {'max_salary': {'$gt': salary_input}}]})
