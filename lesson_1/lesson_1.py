# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint

url = 'https://api.github.com/users'
user = 'ElizaPolkovnikova'
response = requests.get(f'{url}/{user}/repos')
j_data = response.json()
# pprint(j_data)

# print(type(j_data))  # получили список

for el in j_data:  # перебираем словари в списке, выводим значения по ключу 'name'
    print(el['name'])

