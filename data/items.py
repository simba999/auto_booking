# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DataItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    company = scrapy.Field()
    email = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    country = scrapy.Field()
    address = scrapy.Field()
    address2 = scrapy.Field()
    headquarter_phone = scrapy.Field()
    contact_phone = scrapy.Field()
    updated = scrapy.Field()
    link = scrapy.Field()
