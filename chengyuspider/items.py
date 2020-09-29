# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChengyuspiderItem(scrapy.Item):
    """
    定义Item
    """
    chengyu = scrapy.Field()
    url = scrapy.Field()
    pronunce = scrapy.Field()
    meanings = scrapy.Field()
    from_where = scrapy.Field()
