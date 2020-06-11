from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, DOUBLE, DATE, VARCHAR, BIGINT

Base = declarative_base()


class IndexPerformance(Base):
    __tablename__ = 'index_performance'
    ip_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    index_code = Column(VARCHAR)
    standard_deviation = Column(DOUBLE)
    pe_ratio = Column(DOUBLE)
    top_sector_name = Column(VARCHAR)
    top_sector_exposure = Column(DOUBLE)
    top_holding_isin = Column(VARCHAR)
    top_holding_exposure = Column(DOUBLE)
    perf_1m = Column(DOUBLE)
    perf_3m = Column(DOUBLE)
    perf_6m = Column(DOUBLE)
    perf_1y = Column(DOUBLE)
    perf_2y = Column(DOUBLE)
    perf_3y = Column(DOUBLE)
    perf_5y = Column(DOUBLE)
    perf_inception = Column(DOUBLE)
    reporting_date = Column(DATE)


class IndexPrices(Base):
    __tablename__ = 'index_prices'
    index_price_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    index_code = Column(VARCHAR)
    index_price_open = Column(DOUBLE)
    index_price_high = Column(DOUBLE)
    index_price_low = Column(DOUBLE)
    index_price_close = Column(DOUBLE)
    index_price_as_on_date = Column(DATE)
    standard_deviation = Column(DOUBLE)


class MasIndices(Base):
    __tablename__ = 'mas_indices'
    index_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    index_code = Column(VARCHAR)
    index_name = Column(VARCHAR)
    index_type = Column(VARCHAR)
    exchange_code = Column(VARCHAR)
    market_cap_type_code = Column(VARCHAR)


class MasSectors(Base):
    __tablename__ = 'mas_sectors'
    sector = Column(VARCHAR, nullable=False, primary_key=True)
    industry = Column(VARCHAR, nullable=False, primary_key=True)


class MasSecurities(Base):
    __tablename__ = 'mas_securities'
    security_isin = Column(VARCHAR, nullable=False, primary_key=True)
    security_name = Column(VARCHAR, nullable=False, primary_key=True)
    security_code = Column(VARCHAR)
    bse_security_symbol = Column(VARCHAR)
    nse_security_symbol = Column(VARCHAR)
    mse_security_symbol = Column(VARCHAR)
    industry = Column(VARCHAR)
    market_cap_type_code = Column(VARCHAR)
    market_cap_value = Column(BIGINT)
    std_deviation = Column(DOUBLE)
    alpha = Column(DOUBLE)
    beta = Column(DOUBLE)
    sortino_ratio = Column(DOUBLE)
    pe_ratio = Column(DOUBLE)
    pb_ratio = Column(DOUBLE)
    roe = Column(DOUBLE)
    eps = Column(DOUBLE)
    dividend_yield = Column(DOUBLE)
