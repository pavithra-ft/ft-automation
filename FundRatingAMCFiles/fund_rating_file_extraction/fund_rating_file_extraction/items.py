# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FundRatingFileExtractionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    amc_url = scrapy.Field()
    files = scrapy.Field()

