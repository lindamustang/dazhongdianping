# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    num = scrapy.Field()
    sug1 = scrapy.Field()
    sug2 = scrapy.Field()
    sug3 = scrapy.Field()
    star = scrapy.Field()
    tuangou = scrapy.Field()
    pass
