# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CourseItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    type = scrapy.Field()
    students = scrapy.Field()


class ShiyanlouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
