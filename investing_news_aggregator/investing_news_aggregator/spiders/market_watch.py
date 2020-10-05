from datetime import datetime
import scrapy

from ..items import Article


class MarketWatchSpider(scrapy.Spider):
    name = 'marketwatch'
    allowed_domains = ['marketwatch.com']
    start_urls = [
        'https://www.marketwatch.com/latest-news'
    ]

    filename = name + '_' + datetime.now().date().strftime("%m%d%Y")
    custom_settings = {"FEEDS": {f"results/{filename}.jl": {"format":"jl"}}}

    def parse(self, response):
        item = Article()
        headlines = response.xpath('//div[@class="element element--article "]')
        for headline in headlines:
            temp = headline.xpath('div[@class="article__content"]')
            item['title'] = temp.xpath('h3/a/text()').get()
            item['summary'] = temp.xpath('p/text()').get()
            item['url'] = temp.xpath('h3/a/@href').get()
            item['date_extracted'] = datetime.now()
            item['thumbnail_url'] = headline.xpath('figure[@class="article__figure"]/a/img/@data-srcset').getall()

            # Somehow LOSE div[@class="article__details"] during the iteration through headlines eventhough the elements are static???
            # item['date_posted'] = datetime.strptime(temp.xpath('div/span/@data-est').get(), '%Y-%m-%dT%H:%M:%S')
            # item['author'] = temp.xpath('div/span[@class="article__author"]/text()').get().replace('by ', '')
            yield item
        
        # "See More" to load more articles is javascript function trigger
