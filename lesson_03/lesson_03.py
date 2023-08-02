# Урок 3. Парсинг данных. HTML, Beautiful Soap

from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import json
import uuid  # библиотека для генерации id
import lesson_03_func as func



# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии в вашу базу.

# Создаем БД
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
vacancies_collection = db.vacancies_collection

# Парсим вакансии с сайта и заносим по одной в БД
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
url = 'https://lipetsk.hh.ru/search/vacancy'
# job_title = input('job-title: ')
params = {'search_field': ['name', 'company_name', 'description'],
          'enable_snippets': 'false',
          'text': 'python',  # заменить на job_title
          'page': 0}
session = requests.Session()
duplicate_vacancies = []

while True:
    response = session.get(url, headers=headers, params=params)
    if response.status_code == 404:  # учитываем 404 ошибку
        break
    # if not response.ok():  # или так
    #   break

    soup = BeautifulSoup(response.text, 'html.parser')
    vacancies = soup.find_all('div', {'class': 'serp-item'})
    if not vacancies:  # учитываем пустые страницы
        break

    for vacancy in vacancies:
        vacancy_info = {}
        info = vacancy.find('a', {'class': 'serp-item__title'})
        name = info.text
        link = info.get('href')

        # Разнесение з/п в 3 поля: min, mix и currency
        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        try:  # если з/п не указана, у NoneType нет атрибута .text, обрабатываем исключение
            salary_text = salary.text
            salary_text = salary_text.replace('\u202f', '')  # очистка от пробелов
            word_list = salary_text.split()  # делим содержимое строки на элементы в списке
            num_list = [int(num) for num in filter(
                lambda num: num.isnumeric(), word_list)]  # перебираем элементы, если цифра - преобразуем в int
        except AttributeError:
            num_list = []

        if len(num_list) == 1:
            vacancy_info['_id'] = str(uuid.uuid4())  # генерируем id
            vacancy_info['name'] = name
            vacancy_info['link'] = link
            vacancy_info['min_salary'] = num_list[0]
            vacancy_info['max_salary'] = 'None'
            vacancy_info['currency'] = salary_text[-1]
        if len(num_list) == 2:
            vacancy_info['_id'] = str(uuid.uuid4())
            vacancy_info['name'] = name
            vacancy_info['link'] = link
            vacancy_info['min_salary'] = num_list[0]
            vacancy_info['max_salary'] = num_list[1]
            vacancy_info['currency'] = salary_text[-1]
        if len(num_list) == 0:
            vacancy_info['_id'] = str(uuid.uuid4())
            vacancy_info['name'] = name
            vacancy_info['link'] = link
            vacancy_info['min_salary'] = 'None'
            vacancy_info['max_salary'] = 'None'
            vacancy_info['currency'] = 'None'

        # Заносим в БД словарь с данными вакансии

        # 2 варианта реализации:
        # Если вакансия существует, добавляем в список дубликатов, иначе заносим в БД

        # 1. Через функцию проверки наличия вакансии
        # if func.is_existed(vacancy_info, vacancies_collection) is True:
        #     duplicate_vacancies.append(vacancy_info)
        # else:
        #     func.add_unique_vacancy_to_db(vacancy_info, vacancies_collection)

        # 2. Через обработку исключения наличия дубликата
        if func.add_unique_vacancy_to_db(vacancy_info, vacancies_collection) is False:
            duplicate_vacancies.append(vacancy_info)

    print(f"Обработана страница №{params['page']}")
    params['page'] += 1

print(f'Кол-во документов в БД: {db.vacancies_collection.count_documents({})}')  # 800
print(f'Количество дубликатов: {len(duplicate_vacancies)}. id таких вакансий уже есть в БД.')


# Собираем список дублированных вакансий в json
with open('duplicate_vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(duplicate_vacancies, f)


# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
# больше введённой суммы (необходимо анализировать оба поля зарплаты, то есть цифра вводится одна,
# а запрос проверяет оба поля)
# Проверка функции в рамках 2 задания

func.get_vacancies_gt_input(vacancies_collection, 200000)
