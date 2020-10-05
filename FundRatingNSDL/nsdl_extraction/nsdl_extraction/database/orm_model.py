from ..settings import CONNECTION_STRING
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DOUBLE, DATE, TINYINT

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(CONNECTION_STRING, pool_pre_ping=True, pool_size=32, max_overflow=64)


class SecurityPrices(Base):
    __tablename__ = 'security_prices'
    sp_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    security_isin = Column(VARCHAR)
    coupon_rate = Column(DOUBLE)
    maturity_date = Column(DATE)
    last_traded_price = Column(DOUBLE)
    average_weighted_price = Column(DOUBLE)
    weighted_avg_yield = Column(DOUBLE)
    turnover = Column(DOUBLE)
    credit_rating = Column(VARCHAR)
    number_of_trade = Column(TINYINT)
    reporting_date = Column(DATE)


class PrimaryIssuance(Base):
    __tablename__ = 'primary_issuance'
    pi_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    security_isin = Column(VARCHAR)
    issue_size = Column(DOUBLE)
    issue_price = Column(DOUBLE)
    issue_allotment_date = Column(DATE)
    interest_payment_frequency = Column(VARCHAR)
    first_interest_payment_date = Column(DATE)
    maturity_date = Column(DATE)
    put_option_description = Column(VARCHAR)
    call_option_description = Column(VARCHAR)
    credit_rating_agency = Column(VARCHAR)
    credit_rating = Column(VARCHAR)
    date_of_rating = Column(DATE)
    reporting_date = Column(DATE)


class MasSecurities(Base):
    __tablename__ = 'mas_securities'
    security_isin = Column(VARCHAR, nullable=False, primary_key=True)
    security_name = Column(VARCHAR, nullable=False, primary_key=True)
    exchange_code = Column(VARCHAR)
    security_type = Column(VARCHAR)
    security_code = Column(VARCHAR)
    bse_security_symbol = Column(VARCHAR)
    nse_security_symbol = Column(VARCHAR)
    mse_security_symbol = Column(VARCHAR)
    industry = Column(VARCHAR)
