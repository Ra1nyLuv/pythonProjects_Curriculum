import scrapy


class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itcast.cn"]
    start_urls = ["https://itcast.cn"]

    def parse(self, response):
        
        with open("itcast.html", "wb") as f:   
            f.write(response.body)
