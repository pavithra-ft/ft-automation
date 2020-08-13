# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItimfItem(scrapy.Item):
    # define the fields for your item here like:
    region = scrapy.Field()
    state = scrapy.Field()
    agent_no = scrapy.Field()
    agent_name = scrapy.Field()
    city = scrapy.Field()
    pin_code = scrapy.Field()
    mobile_no = scrapy.Field()
    email = scrapy.Field()
