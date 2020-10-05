# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime


def serialize_time(time):
    return time.strftime("%m/%d/%Y,%H:%M:%S")


class Article(scrapy.Item):
    domain = scrapy.Field(default=None)
    url = scrapy.Field(default=None)
    title = scrapy.Field(default=None)
    summary = scrapy.Field(default=None)
    date_posted = scrapy.Field(serializer=serialize_time, default=None)
    date_extracted = scrapy.Field(serializer=serialize_time, default=None)
    thumbnail_url = scrapy.Field(default=None)
    author = scrapy.Field(default=None)
    body = scrapy.Field(default=None)
    words_count = scrapy.Field(default=None)