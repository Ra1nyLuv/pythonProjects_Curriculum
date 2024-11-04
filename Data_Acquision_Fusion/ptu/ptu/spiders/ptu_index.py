import scrapy
from ptu.items import PtuItem

class PtuIndexSpider(scrapy.Spider):
    name = 'ptu_index'
    allowed_domains = ['www.ptu.edu.cn']
    start_urls = ['http://www.ptu.edu.cn/index.htm']

    def parse(self, response):
        # 选择包含目标元素的div
        ind_01_div = response.xpath('//div[@class="ind-01"]')

        # 遍历每个li元素
        for li in ind_01_div.xpath('.//ul[@class="mid-nav clear"]/li'):
            # 提取超链接
            link = li.xpath('.//a/@href').get()
            # 提取标题文本
            title = li.xpath('.//div[@class="tit"]/text()').get()

            # 创建item对象
            item = PtuItem()
            item['menu'] = title
            item['url'] = response.urljoin(link)  # 将相对路径转换为绝对路径

            # 返回item对象
            yield item