# scrapy crawl hhru
from scrapy.crawler import CrawlerProcess  # Класс. Отвечает за процесс сбора данных
from scrapy.utils.reactor import install_reactor  # Функция. Включает асинхронизацию
from scrapy.utils.log import configure_logging  # Функция.Запуск и инициализация системы логирования

# Функция. Собирает настройки в структуру, которую пропишет внутрь свойств паука
# и запустит паука с параметрами этих настроек
from scrapy.utils.project import get_project_settings

from lesson_06.jobparser.spiders.hhru import HhruSpider  # Импортируем паука

if __name__ == '__main__':
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    configure_logging()
    process = CrawlerProcess(get_project_settings())  # функция найдет файл settings.py
    process.crawl(HhruSpider)  # добавляем исполнителя к процессу
    process.start()
