import scrapy
from scrapy.http import HtmlResponse
# from lesson_06.jobparser.items import JobparserItem
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]  # нужно, чтобы паук на сторонник сайты не ушел
    start_urls = ["https://lipetsk.hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name\
                   &search_field=description&enable_snippets=false&text=python&L_save_area=true",
                  "https://lipetsk.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name\
                   &search_field=description&enable_snippets=false&text=python&L_save_area=true"]

    def parse(self, response: HtmlResponse):


        # возвращаются объекты DOM, поэтому берем getll() и получаем список ссылок
        links = response.xpath("//a[@class='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
            # .follow() - метод для перехода в link, внутрь вакансии. Формирует запрос, ответ которого обрабатываем в методе vacancy_parse
            # Cвязываем с методом vacancy_parse.callback - функция, которая будет вызываться с ответом на этот запрос
            # переход на след.страницу с помощью кнопки "дальше" на сайте
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        # .get() - получаем 1-ый эл-т из списка и присваиваем переменной. Если список пустой, возвращает None.
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        # Парсинг содержимого вакансии
        name = response.xpath("//h1/text()").get()  # заголовок
        salary = response.xpath("//div[@data-qa='vacancy-salary']/span//text()").getall()  # з/п
        url = response.url
        # Упаковываем объект с помощью класса JobparserItem: объявляем свойства, кот. будут хранить в себе данные
        yield JobparserItem(name=name, salary=salary, url=url)




