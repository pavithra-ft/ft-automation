from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, DOUBLE, DATE, LONGTEXT, TEXT, TIMESTAMP, TINYINT, VARCHAR, BIGINT

Base = declarative_base()


class PerAllFunds(Base):
    __tablename__ = 'per_all_funds'
    fpid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_code = Column(VARCHAR, unique=True)
    inst_code = Column(VARCHAR)
    fund_name = Column(VARCHAR)
    fund_short_code = Column(VARCHAR)
    fund_type_code = Column(VARCHAR)
    fund_subtype_type = Column(VARCHAR)
    inception_date = Column(DATE)
    nav_start_date = Column(DATE)
    fund_status = Column(VARCHAR)
    close_date = Column(DATE)
    fund_segment_type_code = Column(VARCHAR)
    min_inv_amount = Column(DOUBLE)
    benchmark_index_code = Column(VARCHAR)
    benchmark_alt_index_code = Column(VARCHAR)
    fund_portfolio_type_code = Column(VARCHAR)
    fund_description = Column(LONGTEXT)
    objective = Column(LONGTEXT)
    investment_style = Column(VARCHAR)
    investment_philosophy = Column(LONGTEXT)
    is_visible = Column(TINYINT)
    created_ts = Column(TIMESTAMP)
    created_by = Column(VARCHAR)


class CollateralTemplates(Base):
    __tablename__ = 'collateral_templates'
    t_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    template_code = Column(VARCHAR, unique=True)
    template_type_code = Column(VARCHAR)
    entity_type = Column(VARCHAR)
    entity_code = Column(VARCHAR)
    template_url = Column(VARCHAR)
    is_default = Column(TINYINT)
    effective_start_date = Column(DATE)
    effective_end_date = Column(DATE)


class Collaterals(Base):
    __tablename__ = 'collaterals'
    collateral_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    collateral_code = Column(VARCHAR, unique=True)
    view_code = Column(VARCHAR, unique=True)
    auth_code = Column(VARCHAR, unique=True)
    collateral_type_code = Column(VARCHAR)
    entity_type = Column(VARCHAR)
    entity_code = Column(VARCHAR)
    collateral_title = Column(TEXT)
    external_url = Column(VARCHAR)
    visibility_code = Column(VARCHAR)
    template_code = Column(VARCHAR)
    collateral_date = Column(DATE)
    collateral_status = Column(VARCHAR)
    reporting_date = Column(DATE)
    effective_start_date = Column(DATE)
    effective_end_date = Column(DATE)
    is_premium = Column(TINYINT, default=0)
    is_published = Column(TINYINT)
    is_data_changed = Column(TINYINT, default=1)
    published_ts = Column(TIMESTAMP)
    created_ts = Column(TIMESTAMP)
    created_by = Column(VARCHAR)


class FundBenchmarkNav(Base):
    __tablename__ = 'fund_benchmark_nav'
    fbn_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_code = Column(VARCHAR)
    benchmark_index_code = Column(VARCHAR)
    alt_benchmark_index_code = Column(VARCHAR)
    fund_nav = Column(DOUBLE)
    benchmark_nav = Column(DOUBLE)
    alt_benchmark_nav = Column(DOUBLE)
    effective_end_date = Column(DATE)


class FundMarketCapDetails(Base):
    __tablename__ = 'fund_market_cap_details'
    mcapId = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_code = Column(VARCHAR)
    type_market_cap = Column(VARCHAR)
    exposure = Column(DOUBLE)
    start_date = Column(DATE)
    end_date = Column(DATE)
    created_ts = Column(TIMESTAMP)
    action_by = Column(VARCHAR)


class FundPerformance(Base):
    __tablename__ = 'fund_performance'
    fpid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_code = Column(VARCHAR)
    current_aum = Column(DOUBLE)
    no_of_clients = Column(DOUBLE)
    market_cap_type_code = Column(VARCHAR)
    portfolio_equity_allocation = Column(DOUBLE)
    portfolio_cash_allocation = Column(DOUBLE)
    portfolio_asset_allocation = Column(DOUBLE)
    portfolio_other_allocations = Column(DOUBLE)
    perf_1m = Column(DOUBLE)
    perf_3m = Column(DOUBLE)
    perf_6m = Column(DOUBLE)
    perf_1y = Column(DOUBLE)
    perf_2y = Column(DOUBLE)
    perf_3y = Column(DOUBLE)
    perf_5y = Column(DOUBLE)
    perf_inception = Column(DOUBLE)
    benchmark_perf_1m = Column(DOUBLE)
    benchmark_perf_3m = Column(DOUBLE)
    benchmark_perf_6m = Column(DOUBLE)
    benchmark_perf_1y = Column(DOUBLE)
    benchmark_perf_2y = Column(DOUBLE)
    benchmark_perf_3y = Column(DOUBLE)
    benchmark_perf_5y = Column(DOUBLE)
    benchmark_perf_inception = Column(DOUBLE)
    alt_benchmark_perf_1m = Column(DOUBLE)
    alt_benchmark_perf_3m = Column(DOUBLE)
    alt_benchmark_perf_6m = Column(DOUBLE)
    alt_benchmark_perf_1y = Column(DOUBLE)
    alt_benchmark_perf_2y = Column(DOUBLE)
    alt_benchmark_perf_3y = Column(DOUBLE)
    alt_benchmark_perf_5y = Column(DOUBLE)
    alt_benchmark_perf_inception = Column(DOUBLE)
    isLatest = Column(INTEGER)
    effective_start_date = Column(DATE)
    effective_end_date = Column(DATE)
    created_ts = Column(TIMESTAMP)
    created_by = Column(VARCHAR)


class FundPortfolioDetails(Base):
    __tablename__ = 'fund_portfolio_details'
    fpid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_code = Column(VARCHAR)
    security_isin = Column(VARCHAR)
    exposure = Column(DOUBLE)
    start_date = Column(DATE)
    end_date = Column(DATE)
    created_ts = Column(TIMESTAMP)
    action_by = Column(VARCHAR)


class FundRatios(Base):
    __tablename__ = 'fund_ratios'
    ratio_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_code = Column(INTEGER)
    reporting_date = Column(DATE)
    top5_pe_ratio = Column(DOUBLE)
    top10_pe_ratio = Column(DOUBLE)
    top5_market_cap = Column(BIGINT)
    top10_market_cap = Column(BIGINT)
    standard_deviation = Column(DOUBLE)
    median = Column(DOUBLE)
    sigma = Column(DOUBLE)
    sortino_ratio = Column(DOUBLE)
    negative_excess_returns_risk_free = Column(DOUBLE)
    fund_alpha = Column(DOUBLE)
    fund_beta = Column(DOUBLE)
    updated_ts = Column(TIMESTAMP)
    updated_by = Column(VARCHAR)


class FundSectorDetails(Base):
    __tablename__ = 'fund_sector_details'
    fsd_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    fund_code = Column(VARCHAR)
    sector_type_name = Column(VARCHAR)
    exposure = Column(DOUBLE)
    start_date = Column(DATE)
    end_date = Column(DATE)
    created_ts = Column(TIMESTAMP)
    action_by = Column(VARCHAR)


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


class MasMarketCapTypes(Base):
    __tablename__ = 'mas_market_cap_types'
    mc_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    market_cap_type_code = Column(VARCHAR, unique=True)
    market_cap_type_desc = Column(VARCHAR)


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


class RatioBasis(Base):
    __tablename__ = 'ratio_basis'
    risk_free_return_rate = Column(DOUBLE, nullable=False, primary_key=True)


class SecuritiesFundamentals(Base):
    __tablename__ = 'securities_fundamentals'
    sf_id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    security_id = Column(VARCHAR)
    security_isin = Column(VARCHAR)
    as_on_date = Column(DATE)
    market_cap = Column(BIGINT)
    pe_ratio = Column(DOUBLE)
