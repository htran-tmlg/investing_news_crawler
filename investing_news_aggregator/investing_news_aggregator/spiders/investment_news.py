import scrapy
from datetime import datetime

from ..items import Article


class InvestmentNewsSpider(scrapy.Spider):
    name = 'investmentnews'
    allowed_domains = ['investmentnews.com']
    start_urls = ['https://www.investmentnews.com/news-list']

    filename = name + '_' + datetime.now().date().strftime("%m%d%Y")
    custom_settings = {"FEEDS": {f"results/{filename}.jl": {"format":"jl"}}}

    def parse(self, response):
        item = Article()
        headlines = response.xpath('//div[@class="listingItem"]')
        for headline in headlines:
            temp = headline.xpath('div[@class="row"]/div[@class="col-md-8"]/div')
            item['title'] = temp.xpath('h3/a/text()').get()
            item['summary'] = temp.xpath('p/text()').get()
            item['url'] = temp.xpath('h3/a/@href').get()
            item['date_posted'] = datetime.strptime(temp.xpath('div/div/ul/li[@class="bon-car-meta-date"]/text()').get(), '%B %d, %Y')
            item['date_extracted'] = datetime.now()
            item['thumbnail_url'] = headline.xpath('div[@class="row"]/div[@class="col-md-4 newsListingImageContainer"]/a/img/@src').get()
            yield item

        next_url = response.xpath('//div[@class="col-lg-2 col-sm-6 pagenumbers-next-container"]/a/@href').get()
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)
