# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QshopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item1 = scrapy.Field()
    item2 = scrapy.Field()
    item1_ch = scrapy.Field()
    item2_ch = scrapy.Field() 
    yano = scrapy.Field()
    keyword = scrapy.Field()
    pdName = scrapy.Field()
    pdno = scrapy.Field()
    priceOriginal = scrapy.Field()
    priceNormal = scrapy.Field()
    price = scrapy.Field()
    pdsales = scrapy.Field() 
    date = scrapy.Field()

