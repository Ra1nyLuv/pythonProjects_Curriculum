import scrapy

class PtuItem(scrapy.Item):
    menu = scrapy.Field()
    url = scrapy.Field()