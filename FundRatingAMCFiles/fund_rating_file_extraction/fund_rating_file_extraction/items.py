# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FundRatingFileExtractionItem(scrapy.Item):
    amc_url = scrapy.Field()
    files = scrapy.Field()