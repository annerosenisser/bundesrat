# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeetingsItem(scrapy.Item):
    id = scrapy.Field()
    date = scrapy.Field()
    year =  scrapy.Field()
    committees = scrapy.Field()
    AV = scrapy.Field()
    AIS = scrapy.Field()
    AA = scrapy.Field()
    EU = scrapy.Field()
    Fz = scrapy.Field()
    FJ =  scrapy.Field()
    G = scrapy.Field()
    In = scrapy.Field()
    K = scrapy.Field()
    R = scrapy.Field()
    Wo = scrapy.Field()
    U = scrapy.Field()
    Vk = scrapy.Field()
    V = scrapy.Field()
    Wi = scrapy.Field()
    other = scrapy.Field()
    fdf = scrapy.Field()
    title = scrapy.Field()

