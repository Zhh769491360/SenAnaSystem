# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyShortItem(scrapy.Item):
    commentPos = scrapy.Field()
    commentNeg = scrapy.Field()
    commentMid = scrapy.Field()

class ScrapyLongItem(scrapy.Item):
    commentPos = scrapy.Field()
    commentNeg = scrapy.Field()
    commentMid = scrapy.Field()

class ScrapyGetIdItem(scrapy.Item):
    id = scrapy.Field()