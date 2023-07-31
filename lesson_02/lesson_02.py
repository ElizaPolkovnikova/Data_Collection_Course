from bs4 import BeautifulSoup
import requests
from pprint import pprint
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
url = 'https://lipetsk.hh.ru/search/vacancy'
# job_title = input('job-title: ')


params = {'search_field': ['name', 'company_name', 'description'],
          'enable_snippets': 'false',
          'text': 'python',  # заменить на job_title
          'page': 0}

session = requests.Session()
vacancies_list = []

while True:
    response = session.get(url, headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    vacancies = soup.find_all('div', {'class': 'serp-item'})
    # if not vacancies:
    #     break
    if response.status_code == 404:
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
            vacancy_info['name'] = name
            vacancy_info['link'] = link
            vacancy_info['min_salary'] = num_list[0]
            vacancy_info['max_salary'] = 'None'
            vacancy_info['currency'] = salary_text[-1]
        if len(num_list) == 2:
            vacancy_info['name'] = name
            vacancy_info['link'] = link
            vacancy_info['min_salary'] = num_list[0]
            vacancy_info['max_salary'] = num_list[1]
            vacancy_info['currency'] = salary_text[-1]
        if len(num_list) == 0:
            vacancy_info['name'] = name
            vacancy_info['link'] = link
            vacancy_info['min_salary'] = 'None'
            vacancy_info['max_salary'] = 'None'
            vacancy_info['currency'] = 'None'

        vacancies_list.append(vacancy_info)
    print(f"Обработана страница №{params['page']}")
    params['page'] += 1

# pprint(vacancies_list)

df = pd.DataFrame(data=vacancies_list)
df.to_csv(r'/Users/elizavetapolkovnikova/Git_Projects/Data_Collection_Course/lesson_02/df_lesson_02.csv', index=False)

# print(df.count())  # 800 строк (40 страниц по 20 объектов)





