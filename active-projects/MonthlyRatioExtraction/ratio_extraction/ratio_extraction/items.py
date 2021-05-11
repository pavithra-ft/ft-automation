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
