from datetime import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider, Rule
from scrapy.loader import ItemLoader
from ..items import Article


class MarketWatchSpider(Spider):
    name = 'market_watch'
    allowed_domains = ['quotes.toscrape.com', 'marketwatch.com']
    start_urls = [
        'https://www.marketwatch.com/latest-news'
        # 'http://quotes.toscrape.com'
    ]

    # rules = (
    #     Rule(LinkExtractor(allow=r'/page/d+'), callback='parse', follow=True),
    # )

    def parse(self, response):
        # item = Article()
        # quotes = response.xpath('//div[@class="quote"]')
        # for quote in quotes:
        #     item['title'] = quote.xpath('span[@class="text"]/text()').get()
        #     yield item

        # url = response.xpath('//li[@class="next"]/a/@href').get()
        # if url is not None:
        #     yield response.follow(url, callback=self.parse)

        if response.status == 200:
            item = Article()
            articles = response.xpath('//div[@class="collection__elements j-scrollElement"]')
            for article in articles:
                content = article.xpath('//div[@class="element element--article"]/div[@class="article__content"]')
                item['url'] = content.xpath('//h3[@class="article__headline"]/a[@class="link"]/@href').getall()
                item['title'] = content.xpath('//h3[@class="article__headline"]/a[@class="link"]/text()').getall()
                item['summary'] = content.xpath('//p[@class="article__summary"]/text()').getall()
                item['date_posted'] = content.xpath('//div[@class="article__details"]/span[@class="article__timestamp"]/@data-est').getall()
                # item['date_extracted'] = datetime.now()
                # item['words_count'] = response.xpath(f'//input[@id="sid"]/@value').get()
                yield item
        else:
            self.logger.warning('No item received for %s', response.url)