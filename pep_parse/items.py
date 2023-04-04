import scrapy


class PepParseItem(scrapy.Item):
    """
    Класс Scrapy Item для хранения информации о предложении по улучшению
    Python (PEP).
    """
    number = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
