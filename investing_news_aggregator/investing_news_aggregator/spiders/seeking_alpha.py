import scrapy
import urllib.parse
from datetime import datetime, timedelta
from pytz import timezone

from ..items import Article


class SeekingAlphaSpider(scrapy.Spider):
    name = 'seekingalpha'
    allowed_domains = ['seekingalpha.com']
    start_urls = ['https://seekingalpha.com/market-news/']
    today = datetime.now()
    yesterday = today + timedelta(days=-1)
    my_timezone = timezone('US/Pacific')

    filename = name + '_' + today.date().strftime("%m%d%Y")
    custom_settings = {"FEEDS": {f"results/{filename}.jl": {"format":"jl"}}}

    def parse(self, response):
        item = Article()
        headlines = response.xpath('//li[@class="item"]')
        for headline in headlines:
            item['title'] = headline.xpath('h4/a/text()').get()
            item['url'] = urllib.parse.urljoin(f'https://www.{self.allowed_domains[0]}', headline.xpath('h4/a/@href').get())
            date_posted = headline.xpath('div[@class="share-line"]/span[@class="item-date"]/text()').get()
            if 'Today' in date_posted:
                date = self.my_timezone.localize(self.today)
                date = date.astimezone(self.my_timezone)
                item['date_posted'] = date
            elif 'Yesterday' in date_posted:
                date = self.my_timezone.localize(self.yesterday)
                date = date.astimezone(self.my_timezone)
                item['date_posted'] = date
            item['date_extracted'] = datetime.now()
            yield item

        next_url = response.xpath('//li[@class="next"]/a/@href').get()
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)
