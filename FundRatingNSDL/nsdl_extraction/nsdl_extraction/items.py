# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NsdlTradeDataItem(scrapy.Item):
    reporting_date = scrapy.Field()
    security_isin = scrapy.Field()
    coupon_rate = scrapy.Field()
    maturity_date = scrapy.Field()
    last_traded_price = scrapy.Field()
    average_weighted_price = scrapy.Field()
    weighted_avg_yield = scrapy.Field()
    turnover = scrapy.Field()
    credit_rating = scrapy.Field()
    number_of_trade = scrapy.Field()


class NsdlIssuanceDataItem(scrapy.Item):
    reporting_date = scrapy.Field()
    security_isin = scrapy.Field()
    security_description = scrapy.Field()
    issue_size = scrapy.Field()
    issue_price = scrapy.Field()
    issue_allotment_date = scrapy.Field()
    interest_payment_frequency = scrapy.Field()
    first_interest_payment_date = scrapy.Field()
    maturity_date = scrapy.Field()
    put_option_description = scrapy.Field()
    call_option_description = scrapy.Field()
    credit_rating_agency = scrapy.Field()
    credit_rating = scrapy.Field()
    date_of_rating = scrapy.Field()


class NsdlSecurityItem(scrapy.Item):
    security_isin = scrapy.Field()
    security_name = scrapy.Field()
    exchange_code = scrapy.Field()
    security_type = scrapy.Field()
    security_code = scrapy.Field()
    bse_security_symbol = scrapy.Field()
    nse_security_symbol = scrapy.Field()
    mse_security_symbol = scrapy.Field()
    industry = scrapy.Field()
