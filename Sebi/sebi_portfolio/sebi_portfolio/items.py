# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DiscretionaryItem(scrapy.Item):
    s_no = scrapy.Field()
    types_of_clients = scrapy.Field()
    no_of_investors = scrapy.Field()
    listed = scrapy.Field()
    unlisted = scrapy.Field()
    plain_debt = scrapy.Field()
    stru_debt = scrapy.Field()
    eq_derivative = scrapy.Field()
    mutual_funds = scrapy.Field()
    others = scrapy.Field()
    total = scrapy.Field()
    month = scrapy.Field()
    code = scrapy.Field()
    year = scrapy.Field()
    amc_name = scrapy.Field()


class DiscParticularsItem(scrapy.Item):
    gross_sale = scrapy.Field()
    gross_purchase = scrapy.Field()
    pf_turnover_ratio = scrapy.Field()
    performance_of_pf = scrapy.Field()
    value_of_assets = scrapy.Field()
    month = scrapy.Field()
    code = scrapy.Field()
    year = scrapy.Field()
    amc_name = scrapy.Field()


class NonDiscretionaryItem(scrapy.Item):
    s_no = scrapy.Field()
    types_of_clients = scrapy.Field()
    no_of_investors = scrapy.Field()
    listed = scrapy.Field()
    unlisted = scrapy.Field()
    plain_debt = scrapy.Field()
    stru_debt = scrapy.Field()
    eq_derivative = scrapy.Field()
    mutual_funds = scrapy.Field()
    others = scrapy.Field()
    total = scrapy.Field()
    month = scrapy.Field()
    code = scrapy.Field()
    year = scrapy.Field()
    amc_name = scrapy.Field()


class NonDiscParticularsItem(scrapy.Item):
    gross_sale = scrapy.Field()
    gross_purchase = scrapy.Field()
    pf_turnover_ratio = scrapy.Field()
    performance_of_pf = scrapy.Field()
    value_of_assets = scrapy.Field()
    month = scrapy.Field()
    code = scrapy.Field()
    year = scrapy.Field()
    amc_name = scrapy.Field()
