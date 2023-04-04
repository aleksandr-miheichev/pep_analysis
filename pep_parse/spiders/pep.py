import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    """
    Класс Scrapy Spider, который собирает информацию о PEP с peps.python.org.
    """
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        """
        Основной метод парсера, который обрабатывает начальный ответ.

        Аргументы:
            - response: объект HTTP-ответа Scrapy, содержащий содержимое
              страницы.
        Возвращает:
            - Генератор, создающий запросы Scrapy для каждой ссылки на
              документ PEP.
        """
        for link_pep_document in response.css(
                'section#numerical-index a[href^="pep-"]'
        ):
            yield response.follow(link_pep_document, callback=self.parse_pep)

    def parse_pep(self, response):
        """
        Разбирает страницу документа PEP для извлечения номера, названия и
        статуса PEP.

        Аргументы:
            - response: объект HTTP-ответа Scrapy, содержащий содержимое
              страницы документа PEP.
        Возвращает:
            - Генератор, который выдает данные PEP в виде объектов
              PepParseItem.
        """
        h1_text = response.css('h1.page-title::text')
        data = {
            'number': int(h1_text.re_first(r'PEP (\d+)')),
            'name': h1_text.re_first(r'PEP \d+ – (.+)'),
            'status': response.css('abbr::text').get(),
        }
        yield PepParseItem(data)
