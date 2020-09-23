# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    domain = scrapy.Field(default=None)
    url = scrapy.Field(default=None)
    title = scrapy.Field(default=None)
    summary = scrapy.Field(default=None)
    author = scrapy.Field(default=None)
    body = scrapy.Field(default=None)
    date_posted = scrapy.Field(default=None)
    date_extracted = scrapy.Field(serializer='str', default=None)
    words_count = scrapy.Field(default=None)