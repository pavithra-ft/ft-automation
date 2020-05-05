# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FpProfilesItem(scrapy.Item):
    name = scrapy.Field()
    designation = scrapy.Field()
    company = scrapy.Field()
    city = scrapy.Field()
    mailid = scrapy.Field()
    mobile = scrapy.Field()
    amfi_arn = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()


class FpLinkedInItem(scrapy.Item):
    link = scrapy.Field()
