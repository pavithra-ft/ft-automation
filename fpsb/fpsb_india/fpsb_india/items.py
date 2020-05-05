# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FpsbIndiaItem(scrapy.Item):
    name = scrapy.Field()
    designation = scrapy.Field()
    company = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    address_city = scrapy.Field()
    address_state = scrapy.Field()
    address_pincode = scrapy.Field()
    mobile = scrapy.Field()
    resident_contact = scrapy.Field()
    business_contact = scrapy.Field()
    mailid1 = scrapy.Field()
    mailid2 = scrapy.Field()
    employment_nature = scrapy.Field()
    fpsb_number = scrapy.Field()
    profile = scrapy.Field()
