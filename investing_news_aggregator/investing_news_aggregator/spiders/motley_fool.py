import scrapy
from datetime import datetime
import urllib.parse

from ..items import Article

class MotleyFoolSpider(scrapy.Spider):
    name = 'motleyfool'
    allowed_domains = ['fool.com']
    start_urls = ['https://www.fool.com/investing-news/']

    filename = name + '_' + datetime.now().date().strftime("%m%d%Y")
    custom_settings = {"FEEDS": {f"results/{filename}.jl": {"format":"jl"}}}

    def parse(self, response):
        item = Article()
        headlines = response.xpath('//a[@data-id="article-list"]')
        for headline in headlines:
            temp = headline.xpath('article/div[@class="text"]')
            item['title'] = temp.xpath('h4/text()').get()
            item['summary'] = temp.xpath('p/text()').get()
            item['url'] = urllib.parse.urljoin(f'https://www.{self.allowed_domains[0]}', headline.xpath('@href').get())
            item['author'] = temp.xpath('div/text()').get().split(' | ')[0]
            item['date_posted'] = datetime.strptime(temp.xpath('div/text()').get().split(' | ')[1], '%b %d, %Y')
            item['date_extracted'] = datetime.now()
            item['thumbnail_url'] = headline.xpath('article/div[@class="card-image"]/img/@data-src').get()
            yield item

        # pagination_ul = response.xpath('//ul[@class="pagination"]')
        # next_urls = pagination_ul.xpath('li[@class!="active"]')
        # for li in next_urls:
        #     next_url = urllib.parse.urljoin(f'https://www.{self.allowed_domains[0]}', li.xpath('a/@href').get())
        #     if next_url is not None:
        #         yield response.follow(next_url, callback=self.parse)
