from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, DOUBLE, DATE, LONGTEXT, TIMESTAMP, TINYINT, VARCHAR

Base = declarative_base()


class SecurityRating(Base):
    __tablename__ = 'security_rating'
    sr_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_code = Column(VARCHAR)
    security_isin = Column(VARCHAR)
    reporting_date = Column(DATE)
    exposure = Column(DOUBLE)
    market_value = Column(DOUBLE)
    rating_type = Column(VARCHAR)
    rating_symbol = Column(VARCHAR)
    rating_grade = Column(VARCHAR)
    rating_score = Column(DOUBLE)
    total_turnover = Column(DOUBLE)
    liquidity_grade = Column(TINYINT)
    liquidity_score = Column(DOUBLE)
    maturity_years = Column(DOUBLE)
    maturity_score = Column(DOUBLE)
    maturity_date = Column(DATE)
    created_ts = Column(TIMESTAMP)
    created_by = Column(VARCHAR)


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


class PerAllFunds(Base):
    __tablename__ = 'per_all_funds'
    paf_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_code = Column(VARCHAR, unique=True)
    inst_code = Column(VARCHAR)
    fund_name = Column(VARCHAR)
    fund_type = Column(VARCHAR)
    is_visible = Column(TINYINT)
    created_ts = Column(TIMESTAMP)
    created_by = Column(VARCHAR)


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
    put_option_description = Column(LONGTEXT)
    call_option_description = Column(LONGTEXT)
    credit_rating_agency = Column(VARCHAR)
    credit_rating = Column(VARCHAR)
    date_of_rating = Column(DATE)
    reporting_date = Column(DATE)


class FundRating(Base):
    __tablename__ = 'fund_rating'
    fr_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_code = Column(VARCHAR)
    reporting_date = Column(DATE)
    current_aum = Column(DOUBLE)
    nav_units = Column(DOUBLE)
    nav_adj_aum_rating = Column(TINYINT)
    credit_risk_score = Column(DOUBLE)
    liquidity_score = Column(DOUBLE)
    maturity_score = Column(DOUBLE)
    transition_score = Column(DOUBLE)
    fund_score = Column(DOUBLE)
    created_ts = Column(TIMESTAMP)
    created_by = Column(VARCHAR)


class FundWeights(Base):
    __tablename__ = 'fund_weights'
    fw_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_type = Column(VARCHAR)
    rating_type = Column(VARCHAR)
    nav_weight = Column(DOUBLE)
    credit_weight = Column(DOUBLE)
    liquidity_weight = Column(DOUBLE)
    maturity_weight = Column(DOUBLE)
    created_ts = Column(TIMESTAMP)
    created_by = Column(VARCHAR)
