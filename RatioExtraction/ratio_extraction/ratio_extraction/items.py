# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NseIndicesItem(scrapy.Item):
    pdf_url = scrapy.Field()
    files = scrapy.Field()


class BseSectorItem(scrapy.Item):
    index_code = scrapy.Field()
    sector_name = scrapy.Field()
    sector_exposure = scrapy.Field()


class SecurityRatios(scrapy.Item):
    security_name = scrapy.Field()
    market_cap = scrapy.Field()
    price_to_earnings = scrapy.Field()
    price_to_book = scrapy.Field()
    dividend_yield = scrapy.Field()
    earning_per_share = scrapy.Field()
