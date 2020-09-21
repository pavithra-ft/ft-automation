# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker
from nsdl_extraction.nsdl_extraction.database.orm_model import *
from .items import NsdlTradeDataItem, NsdlIssuanceDataItem, NsdlSecurityItem


class NsdlExtractionTradePipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item):
        if not isinstance(item, NsdlTradeDataItem):
            return item
        session = self.Session()
        item_exists = session.query(SecurityPrices).filter_by(security_isin=item['security_isin']). \
            filter_by(reporting_date=item['reporting_date']).count()
        if item_exists == 0:
            security_prices = SecurityPrices()
            security_prices.reporting_date = item['reporting_date']
            security_prices.security_isin = item['security_isin']
            security_prices.coupon_rate = item['coupon_rate']
            security_prices.maturity_date = item['maturity_date']
            security_prices.last_traded_price = item['last_traded_price']
            security_prices.avg_weighted_price = item['average_weighted_price']
            security_prices.weighted_avg_yield = item['weighted_avg_yield']
            security_prices.turnover = item['turnover']
            security_prices.credit_rating = item['credit_rating']
            try:
                session.add(security_prices)
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()
            return item


class NsdlExtractionIssuancePipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item):
        if not isinstance(item, NsdlIssuanceDataItem):
            return item
        session = self.Session()
        item_exists = session.query(PrimaryIssuance).filter_by(security_isin=item['security_isin']).\
            filter_by(reporting_date=item['reporting_date']).count()
        if item_exists == 0:
            primary_issuance = PrimaryIssuance()
            primary_issuance.reporting_date = item['reporting_date']
            primary_issuance.security_isin = item['security_isin']
            primary_issuance.issue_size = item['issue_size']
            primary_issuance.issue_price = item['issue_price']
            primary_issuance.issue_allotment_date = item['issue_allotment_date']
            primary_issuance.interest_payment_frequency = item['interest_payment_frequency']
            primary_issuance.first_interest_payment_date = item['first_interest_payment_date']
            primary_issuance.maturity_date = item['maturity_date']
            primary_issuance.put_option_description = item['put_option_description']
            primary_issuance.call_option_description = item['call_option_description']
            primary_issuance.credit_rating_agency = item['credit_rating_agency']
            primary_issuance.credit_rating = item['credit_rating']
            primary_issuance.date_of_rating = item['date_of_rating']
            try:
                session.add(primary_issuance)
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()
            return item


class NsdlSecurityPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item):
        if not isinstance(item, NsdlSecurityItem):
            return item
        session = self.Session()
        item_exists = session.query(MasSecurities).filter_by(security_isin=item['security_isin']).count()
        if item_exists == 0:
            mas_securities = MasSecurities()
            mas_securities.security_isin = item['security_isin']
            mas_securities.security_name = item['security_name']
            mas_securities.exchange_code = item['exchange_code']
            mas_securities.security_type = item['security_type']
            mas_securities.security_code = item['security_code']
            mas_securities.bse_security_symbol = item['bse_security_symbol']
            mas_securities.nse_security_symbol = item['nse_security_symbol']
            mas_securities.mse_security_symbol = item['mse_security_symbol']
            mas_securities.industry = item['industry']

            try:
                session.add(mas_securities)
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()
        return item
