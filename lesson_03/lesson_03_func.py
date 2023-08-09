# Урок 3. Парсинг данных. HTML, Beautiful Soap
from pymongo.errors import DuplicateKeyError

# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии в вашу базу.


def add_unique_vacancy_to_db(vacancy_info, vacancies_collection):
    """Добавляет уникальную вакансию в базу данных.
    Если вакансия существует, возвращает False"""
    result = True
    try:
        vacancies_collection.insert_one(vacancy_info)
    except DuplicateKeyError:
        print(f"Document with id {vacancy_info.get('_id')} already exists")
        result = False
    return result


def is_existed(vacancy_info, vacancies_collection):
    """Проверяет наличие вакансии в БД.
    True - вакансия есть,
    False - нет"""
    vacancy_id = vacancy_info.get('_id')
    result = vacancies_collection.find_one({'_id': vacancy_id})
    if result is not None:
        return True
    else:
        return False


# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
# больше введённой суммы (необходимо анализировать оба поля зарплаты, то есть цифра вводится одна,
# а запрос проверяет оба поля)


def get_vacancies_gt_input(vacancies_collection, salary_input):
    """Получить вакансии с з/п больше введенной суммы
    c анализом по двум полям"""

    docs = vacancies_collection.find({'$and': [{'min_salary': {'$gt': salary_input}},
                                               {'max_salary': {'$gt': salary_input}}]})
    for doc in docs:
        print(doc)
