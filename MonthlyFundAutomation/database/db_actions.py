import database.orm_model as model
from envparse import env
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from config.base_logger import sql_logger
from sqlalchemy import create_engine, extract, func, and_, or_, update, insert

app_engine = create_engine('mysql://' + env('DEV_USER') + ':' + env('DEV_PASS') + '@' + env('DEV_HOST') + '/app')
fs_engine = create_engine('mysql://' + env('DEV_USER') + ':' + env('DEV_PASS') + '@' + env('DEV_HOST') + '/fs')
iq_engine = create_engine('mysql://' + env('DEV_USER') + ':' + env('DEV_PASS') + '@' + env('DEV_HOST') + '/iq')

app_db = sessionmaker(bind=app_engine)
fs_db = sessionmaker(bind=fs_engine)
iq_db = sessionmaker(bind=iq_engine)

app_session = app_db()
fs_session = fs_db()
iq_session = iq_db()


def get_nav_start_date(fund_code):
    """

    :param fund_code: Fund code of the Fund
    :return: NAV start date of the given fund_code fetched from Per_all_funds
    """
    sql_logger.info('Get : nav_start_date')
    nav_start_date = app_session.query(model.PerAllFunds.nav_start_date).filter_by(fund_code=fund_code).all()[0][0]
    sql_logger.info('Fetched : nav_start_date')
    return nav_start_date


def get_benchmark_index(fund_code):
    """

    :param fund_code: Fund code of the fund
    :return: Benchmark index code of the given fund_code
    """
    sql_logger.info('Get : benchmark_index_code')
    benchmark_index_code = app_session.query(model.PerAllFunds.benchmark_index_code).filter_by(fund_code=fund_code).\
        all()[0][0]
    sql_logger.info('Fetched : benchmark_index_code')
    return benchmark_index_code


def get_alt_benchmark_index(fund_code):
    """

    :param fund_code: Fund code of the fund
    :return: Alternate benchmark index code of the given fund_code
    """
    sql_logger.info('Get : alt_benchmark_index_code')
    alt_benchmark_index_code = app_session.query(model.PerAllFunds.benchmark_alt_index_code).\
        filter_by(fund_code=fund_code).all()[0][0]
    sql_logger.info('Fetched : alt_benchmark_index_code')
    return alt_benchmark_index_code


def get_index_price_as_on_date(date, index_code):
    """

    :param date: Date
    :param index_code: Benchmark index code/Alternate benchmark index code of the fund
    :return: Index close price of the given index code on the specified date
    """
    sql_logger.info('Get : index_price ' + '(' + str(date) + ')')
    date_month = datetime.strptime(str(date), "%Y-%m-%d").month
    date_year = datetime.strptime(str(date), "%Y-%m-%d").year
    index_price = iq_session.query(model.IndexPrices.index_price_close).\
        filter(model.IndexPrices.index_code == index_code). \
        filter(extract('year', model.IndexPrices.index_price_as_on_date) == date_year). \
        filter(extract('month', model.IndexPrices.index_price_as_on_date) == date_month).all()
    sql_logger.info('Fetched : index_price')
    return index_price


def get_start_price(start_date, index_code):
    """

    :param start_date: NAV start date of the Fund
    :param index_code: Benchmark index code/Alternate benchmark index code of the fund
    :return: Index close price of the given index code on the specified date
    """
    sql_logger.info('Get : start_price')
    start_price = iq_session.query(model.IndexPrices.index_price_close).filter_by(index_code=index_code). \
        filter_by(index_price_as_on_date=start_date).all()[0][0]
    sql_logger.info('Fetched : start_price')
    return float(start_price)


def get_cap_type(type_desc):
    """

    :param type_desc: Market cap type - String
    :return: Market cap type - Code
    """
    sql_logger.info('Get : market_cap_type ' + '(' + type_desc + ')')
    market_cap_type = iq_session.query(model.MasMarketCapTypes.market_cap_type_code). \
        filter_by(market_cap_type_desc=type_desc).all()[0][0]
    sql_logger.info('Fetched : market_cap_type')
    return market_cap_type


def get_investment_style(fund_code):
    """

    :param fund_code: Fund code of the Fund
    :return: Investment style of the Fund
    """
    sql_logger.info('Get : investment_style')
    investment_style = app_session.query(model.PerAllFunds.investment_style).filter_by(fund_code=fund_code).all()[0][0]
    sql_logger.info('Fetched : investment_style')
    return investment_style


def get_fund_nav(fund_code, date):
    """

    :param fund_code: Fund code of the Fund
    :param date: Date
    :return: Fund NAV of the given fund code on the specified date
    """
    sql_logger.info('Get : fund_nav ' + '(' + str(date) + ')')
    fund_nav = iq_session.query(model.FundBenchmarkNav.fund_nav).filter_by(fund_code=fund_code).\
        filter_by(effective_end_date=date).all()
    sql_logger.info('Fetched : fund_nav')
    return fund_nav


def get_security_isin_from_db(security_name):
    """

    :param security_name: Security name taken from the Portfolio holdings of the Fund
    :return: Security ISIN of the specified security name
    """
    sql_logger.info('Get : security_isin ' + '(' + security_name + ')')
    security_isin = iq_session.query(model.MasSecurities.security_isin).\
        filter_by(security_name=security_name).all()[0][0]
    sql_logger.info('Fetched : security_isin')
    return security_isin


def get_all_isin():
    """

    :return: All Security ISIN with their corresponding Security names
    """
    sql_logger.info('Get : all_isin_list')
    all_isin_list = iq_session.query(model.MasSecurities.security_isin, model.MasSecurities.security_name).all()
    sql_logger.info('Fetched : all_isin_list')
    return all_isin_list


def get_mcap_for_security(security_isin):
    """

    :param security_isin: ISIN of the security
    :return: Market cap type code of the given security
    """
    sql_logger.info('Get : security_mcap_code ' + '(' + security_isin + ')')
    security_mcap_code = iq_session.query(model.MasSecurities.market_cap_type_code).\
        filter_by(security_isin=security_isin).all()[0][0]
    sql_logger.info('Fetched : security_mcap_code')
    return security_mcap_code


def get_sector_from_portfolio(security_isin):
    """

    :param security_isin: ISIN of the security
    :return: Sector of the given security
    """
    sql_logger.info('Get : sector ' + '(' + security_isin + ')')
    sector = iq_session.query(model.MasSectors.sector).filter(model.MasSecurities.security_isin == security_isin). \
        filter(model.MasSectors.industry == model.MasSecurities.industry).all()[0][0]
    sql_logger.info('Fetched : sector')
    return sector


def get_collateral_code():
    """

    :return: Collateral code generated by the SQL Functions
    """
    sql_logger.info('Get : collateral_code')
    collateral_code = fs_session.query(func.codeGenerator('COLLATERAL')).all()[0][0]
    sql_logger.info('Fetched : collateral_code')
    return collateral_code


def get_collateral_view_code():
    """

    :return: Collateral view code generated by the SQL Functions
    """
    sql_logger.info('Get : collateral_view_code')
    collateral_view_code = fs_session.query(func.codeGenerator('COLLATERAL-VIEW')).all()[0][0]
    sql_logger.info('Fetched : collateral_view_code')
    return collateral_view_code


def get_fund_short_code(fund_code):
    """

    :param fund_code: Fund code of the Fund
    :return: Fund short code of the Fund
    """
    sql_logger.info('Get : fund_short_code')
    fund_short_code = app_session.query(model.PerAllFunds.fund_short_code).filter_by(fund_code=fund_code).all()[0][0]
    sql_logger.info('Fetched : fund_short_code')
    return fund_short_code


def get_default_visibility_code(fund_code):
    """

    :param fund_code: Fund code of the Fund
    :return: Default visibility code of the given fund code
    """
    sql_logger.info('Get : default_visibility_code')
    default_visibility_code = fs_session.query(model.CollateralTemplates.default_visibility_code). \
        filter_by(entity_type='FUND').filter_by(template_type_code='FINTUPLE').filter_by(entity_code=fund_code). \
        all()[0][0]
    sql_logger.info('Fetched : default_visibility_code')
    return default_visibility_code


def get_collateral_template_code(fund_code, reporting_date):
    """

    :param fund_code: Fund code of the Fund
    :param reporting_date: Reporting date of the Fund
    :return: Template code of the given fund code
    """
    sql_logger.info('Get : collateral_template_code')
    collateral_template_code = fs_session.query(model.CollateralTemplates.template_code).filter(
        model.CollateralTemplates.entity_code == fund_code).filter(
        model.CollateralTemplates.template_type_code == 'FINTUPLE').filter(
        or_(and_(reporting_date >= model.CollateralTemplates.effective_start_date,
                 model.CollateralTemplates.effective_end_date.is_(None)),
            and_(model.CollateralTemplates.effective_start_date >= reporting_date,
                 model.CollateralTemplates.effective_end_date <= reporting_date))).all()[0][0]
    sql_logger.info('Fetched : collateral_template_code')
    return collateral_template_code


def get_pe_ratio(security_isin_list):
    """

    :param security_isin_list: A list of Security ISIN and their corresponding exposures
    :return: A list of Security ISIN and it's corresponding PE ratio
    """
    sql_logger.info('Get : pe_ratio_list')
    pe_ratio_list = []
    for security in security_isin_list:
        pe_ratio = iq_session.query(model.SecuritiesFundamentals.pe_ratio). \
            filter_by(security_isin=security.security_isin).order_by(model.SecuritiesFundamentals.as_on_date.desc()). \
            limit(1).all()
        if any(pe_ratio) is False:
            pe_ratio_body = {"security_isin": security.security_isin, "pe_ratio": 0}
        elif pe_ratio[0][0] is None:
            pe_ratio_body = {"security_isin": security.security_isin, "pe_ratio": 0}
        else:
            pe_ratio_body = {"security_isin": security.security_isin, "pe_ratio": pe_ratio[0][0]}
        pe_ratio_list.append(pe_ratio_body)
    sql_logger.info('Fetched : pe_ratio_list')
    return pe_ratio_list


def get_fund_ratio_mcap(security_isin_list):
    """

    :param security_isin_list: A list of Security ISIN and their corresponding exposures
    :return: A list of Security ISIN and it's corresponding Market cap
    """
    sql_logger.info('Get : fund_ratio_mcap_list')
    fund_ratio_mcap_list = []
    for security in security_isin_list:
        fund_ratio_mcap = iq_session.query(model.SecuritiesFundamentals.market_cap). \
            filter_by(security_isin=security.security_isin).order_by(model.SecuritiesFundamentals.as_on_date.desc()). \
            limit(1).all()
        if any(fund_ratio_mcap) is False:
            fund_ratio_mcap_body = {"security_isin": security.security_isin, "market_cap": 0}
        elif fund_ratio_mcap[0][0] is None:
            fund_ratio_mcap_body = {"security_isin": security.security_isin, "market_cap": 0}
        else:
            fund_ratio_mcap_body = {"security_isin": security.security_isin, "market_cap": fund_ratio_mcap[0][0]}
        fund_ratio_mcap_list.append(fund_ratio_mcap_body)
    sql_logger.info('Fetched : fund_ratio_mcap_list')
    return fund_ratio_mcap_list


def get_all_1m_perf(fund_code):
    """

    :param fund_code: Fund code of the Fund
    :return: A list of 1 month performance for all the reporting dates of the given fund code
    """
    sql_logger.info('Get : fund_return_list')
    fund_return = iq_session.query(model.FundPerformance.perf_1m).filter_by(fund_code=fund_code).all()
    fund_return_list = []
    for return_value in fund_return:
        if return_value[0] is None:
            fund_return_list.append(0)
        else:
            fund_return_list.append(float(return_value[0]))
    sql_logger.info('Fetched : fund_return_list')
    return fund_return_list


def get_risk_free_rate():
    """

    :return: Risk free return rate
    """
    sql_logger.info('Get : risk_free_rate')
    risk_free_rate = iq_session.query(model.RatioBasis.risk_free_return_rate).all()[0][0]
    sql_logger.info('Fetched : risk_free_rate')
    return float(risk_free_rate)


def is_nav_exist(fund_code, effective_end_date):
    """

    :param fund_code: Fund code of the Fund
    :param effective_end_date: Reporting date of the Fund
    :return: The count of records for the given fund code and date
    """
    sql_logger.info('Get : is_nav')
    is_nav = iq_session.query(model.FundBenchmarkNav).filter_by(fund_code=fund_code). \
        filter_by(effective_end_date=effective_end_date).count()
    sql_logger.info('Fetched : is_nav')
    return is_nav


def is_fund_performance_exist(fund_code, effective_end_date):
    """

    :param fund_code: Fund code of the Fund
    :param effective_end_date: Reporting date of the Fund
    :return: The count of records for the given fund code and date
    """
    sql_logger.info('Get : is_fund_performance')
    is_fund_performance = iq_session.query(model.FundPerformance).filter_by(fund_code=fund_code). \
        filter_by(effective_end_date=effective_end_date).count()
    sql_logger.info('Fetched : is_fund_performance')
    return is_fund_performance


def is_market_cap_exist(fund_code, end_date, type_market_cap):
    """

    :param fund_code: Fund code of the Fund
    :param end_date: Reporting date of the Fund
    :param type_market_cap: Market cap type
    :return: The count of records for the given fund code, date and the market cap type
    """
    sql_logger.info('Get : is_market_cap ' + '(' + type_market_cap + ')')
    is_market_cap = iq_session.query(model.FundMarketCapDetails).filter_by(fund_code=fund_code). \
        filter_by(end_date=end_date).filter_by(type_market_cap=type_market_cap).count()
    sql_logger.info('Fetched : is_market_cap')
    return is_market_cap


def is_fund_portfolio_exist(fund_code, end_date, security_isin):
    """

    :param fund_code: Fund code of the Fund
    :param end_date: Reporting date of the Fund
    :param security_isin: ISIN of a security
    :return: The count of records for the given fund code, date and security ISIN
    """
    sql_logger.info('Get : is_fund_portfolio ' + '(' + security_isin + ')')
    is_fund_portfolio = iq_session.query(model.FundPortfolioDetails).filter_by(fund_code=fund_code). \
        filter_by(end_date=end_date).filter_by(security_isin=security_isin).count()
    sql_logger.info('Fetched : is_fund_portfolio')
    return is_fund_portfolio


def is_fund_sector_exist(fund_code, end_date, sector_type_name):
    """

    :param fund_code: Fund code of the Fund
    :param end_date: Reporting date of the Fund
    :param sector_type_name: Setor type
    :return: The count of records for the given fund code, date and sector type
    """
    sql_logger.info('Get : is_fund_sector ' + '(' + sector_type_name + ')')
    is_fund_sector = iq_session.query(model.FundSectorDetails).filter_by(fund_code=fund_code).\
        filter_by(end_date=end_date).filter_by(sector_type_name=sector_type_name).count()
    sql_logger.info('Fetched : is_fund_sector')
    return is_fund_sector


def is_collaterals_exist(fund_code, reporting_date):
    """

    :param fund_code: Fund code of the Fund
    :param reporting_date: Reporting date of the Fund
    :return: The count of records for the given fund code and date
    """
    sql_logger.info('Get : is_collateral')
    is_collateral = fs_session.query(model.Collaterals).filter_by(entity_code=fund_code). \
        filter_by(reporting_date=reporting_date).count()
    sql_logger.info('Fetched : is_collateral')
    return is_collateral


def is_fund_ratio_exist(fund_code, reporting_date):
    """

    :param fund_code: Fund code of the Fund
    :param reporting_date: Reporting date of the Fund
    :return: The count of records for the given fund code and date
    """
    sql_logger.info('Get : is_fund_ratio')
    is_fund_ratio = iq_session.query(model.FundRatios).filter_by(fund_code=fund_code). \
        filter_by(reporting_date=reporting_date).count()
    sql_logger.info('Fetched : is_fund_ratio')
    return is_fund_ratio


def update_is_latest(fund_code, previous_1m_end_date):
    """
    Updates the is_Latest value of the previous month to 0

    :param fund_code: Fund code of the Fund
    :param previous_1m_end_date: Reporting date of the previous month
    """
    sql_logger.info('Update - isLatest')
    islatest_update = update(model.FundPerformance).where(model.FundPerformance.fund_code == fund_code). \
        where(model.FundPerformance.effective_end_date == previous_1m_end_date).values(isLatest=None)
    iq_engine.execute(islatest_update)
    sql_logger.info('Updated - isLatest')


def put_fund_benchmark_nav(nav_data):
    """
    Adds a new record/Updates the values if already exists

    :param nav_data: Fund benchmark NAV record of the Fund for the reporting date
    """
    sql_logger.info('Update/Insert - fund_benchmark_nav')
    if is_nav_exist(nav_data.fund_code, nav_data.effective_end_date):
        nav_query = update(model.FundBenchmarkNav).where(model.FundBenchmarkNav.fund_code == nav_data.fund_code). \
            where(model.FundBenchmarkNav.effective_end_date == nav_data.effective_end_date). \
            values(fund_code=nav_data.fund_code, benchmark_index_code=nav_data.benchmark_index_code,
                   alt_benchmark_index_code=nav_data.alt_benchmark_index_code, fund_nav=nav_data.fund_nav,
                   benchmark_nav=nav_data.benchmark_nav, alt_benchmark_nav=nav_data.alt_benchmark_nav,
                   effective_end_date=nav_data.effective_end_date)
    else:
        nav_query = insert(model.FundBenchmarkNav). \
            values(fund_code=nav_data.fund_code, benchmark_index_code=nav_data.benchmark_index_code,
                   alt_benchmark_index_code=nav_data.alt_benchmark_index_code, fund_nav=nav_data.fund_nav,
                   benchmark_nav=nav_data.benchmark_nav, alt_benchmark_nav=nav_data.alt_benchmark_nav,
                   effective_end_date=nav_data.effective_end_date)
    iq_session.execute(nav_query)
    sql_logger.info('Update/Insert success - fund_benchmark_nav')


def put_fund_performance(fund_perf_data, benchmark_perf_data, alt_benchmark_perf_data):
    """
    Adds a new record/Updates the values if already exists

    :param fund_perf_data: Fund performance data of the Fund for the reporting date
    :param benchmark_perf_data: Benchmark performance data of the Fund for the reporting date
    :param alt_benchmark_perf_data: Alternate Benchmark performance data of the Fund for the reporting date
    """
    sql_logger.info('Update/Insert - fund_performance')
    if is_fund_performance_exist(fund_perf_data.fund_code, fund_perf_data.effective_end_date):
        fund_perf_query = update(model.FundPerformance).\
            where(model.FundPerformance.fund_code == fund_perf_data.fund_code).\
            where(model.FundPerformance.effective_end_date == fund_perf_data.effective_end_date).values(
            fund_code=fund_perf_data.fund_code, current_aum=fund_perf_data.current_aum,
            no_of_clients=fund_perf_data.no_of_clients, market_cap_type_code=fund_perf_data.market_cap_type_code,
            investment_style_type_code=fund_perf_data.investment_style_type_code,
            portfolio_equity_allocation=fund_perf_data.portfolio_equity_allocation,
            portfolio_cash_allocation=fund_perf_data.portfolio_cash_allocation,
            portfolio_asset_allocation=fund_perf_data.portfolio_asset_allocation,
            portfolio_other_allocations=fund_perf_data.portfolio_other_allocations, perf_1m=fund_perf_data.perf_1m,
            perf_3m=fund_perf_data.perf_3m, perf_6m=fund_perf_data.perf_6m, perf_1y=fund_perf_data.perf_1y,
            perf_2y=fund_perf_data.perf_2y, perf_3y=fund_perf_data.perf_3y, perf_5y=fund_perf_data.perf_5y,
            perf_inception=fund_perf_data.perf_inception, benchmark_perf_1m=benchmark_perf_data.benchmark_perf_1m,
            benchmark_perf_3m=benchmark_perf_data.benchmark_perf_3m,
            benchmark_perf_6m=benchmark_perf_data.benchmark_perf_6m,
            benchmark_perf_1y=benchmark_perf_data.benchmark_perf_1y,
            benchmark_perf_2y=benchmark_perf_data.benchmark_perf_2y,
            benchmark_perf_3y=benchmark_perf_data.benchmark_perf_3y,
            benchmark_perf_5y=benchmark_perf_data.benchmark_perf_5y,
            benchmark_perf_inception=benchmark_perf_data.benchmark_perf_inception,
            alt_benchmark_perf_1m=alt_benchmark_perf_data.alt_benchmark_perf_1m,
            alt_benchmark_perf_3m=alt_benchmark_perf_data.alt_benchmark_perf_3m,
            alt_benchmark_perf_6m=alt_benchmark_perf_data.alt_benchmark_perf_6m,
            alt_benchmark_perf_1y=alt_benchmark_perf_data.alt_benchmark_perf_1y,
            alt_benchmark_perf_2y=alt_benchmark_perf_data.alt_benchmark_perf_2y,
            alt_benchmark_perf_3y=alt_benchmark_perf_data.alt_benchmark_perf_3y,
            alt_benchmark_perf_5y=alt_benchmark_perf_data.alt_benchmark_perf_5y,
            alt_benchmark_perf_inception=alt_benchmark_perf_data.alt_benchmark_perf_inception,
            isLatest=fund_perf_data.isLatest, effective_start_date=fund_perf_data.effective_start_date,
            effective_end_date=fund_perf_data.effective_end_date, created_ts=fund_perf_data.created_ts,
            created_by=fund_perf_data.created_by)
    else:
        fund_perf_query = insert(model.FundPerformance).values(
            fund_code=fund_perf_data.fund_code, current_aum=fund_perf_data.current_aum,
            no_of_clients=fund_perf_data.no_of_clients, market_cap_type_code=fund_perf_data.market_cap_type_code,
            investment_style_type_code=fund_perf_data.investment_style_type_code,
            portfolio_equity_allocation=fund_perf_data.portfolio_equity_allocation,
            portfolio_cash_allocation=fund_perf_data.portfolio_cash_allocation,
            portfolio_asset_allocation=fund_perf_data.portfolio_asset_allocation,
            portfolio_other_allocations=fund_perf_data.portfolio_other_allocations, perf_1m=fund_perf_data.perf_1m,
            perf_3m=fund_perf_data.perf_3m, perf_6m=fund_perf_data.perf_6m, perf_1y=fund_perf_data.perf_1y,
            perf_2y=fund_perf_data.perf_2y, perf_3y=fund_perf_data.perf_3y, perf_5y=fund_perf_data.perf_5y,
            perf_inception=fund_perf_data.perf_inception, benchmark_perf_1m=benchmark_perf_data.benchmark_perf_1m,
            benchmark_perf_3m=benchmark_perf_data.benchmark_perf_3m,
            benchmark_perf_6m=benchmark_perf_data.benchmark_perf_6m,
            benchmark_perf_1y=benchmark_perf_data.benchmark_perf_1y,
            benchmark_perf_2y=benchmark_perf_data.benchmark_perf_2y,
            benchmark_perf_3y=benchmark_perf_data.benchmark_perf_3y,
            benchmark_perf_5y=benchmark_perf_data.benchmark_perf_5y,
            benchmark_perf_inception=benchmark_perf_data.benchmark_perf_inception,
            alt_benchmark_perf_1m=alt_benchmark_perf_data.alt_benchmark_perf_1m,
            alt_benchmark_perf_3m=alt_benchmark_perf_data.alt_benchmark_perf_3m,
            alt_benchmark_perf_6m=alt_benchmark_perf_data.alt_benchmark_perf_6m,
            alt_benchmark_perf_1y=alt_benchmark_perf_data.alt_benchmark_perf_1y,
            alt_benchmark_perf_2y=alt_benchmark_perf_data.alt_benchmark_perf_2y,
            alt_benchmark_perf_3y=alt_benchmark_perf_data.alt_benchmark_perf_3y,
            alt_benchmark_perf_5y=alt_benchmark_perf_data.alt_benchmark_perf_5y,
            alt_benchmark_perf_inception=alt_benchmark_perf_data.alt_benchmark_perf_inception,
            isLatest=fund_perf_data.isLatest, effective_start_date=fund_perf_data.effective_start_date,
            effective_end_date=fund_perf_data.effective_end_date, created_ts=fund_perf_data.created_ts,
            created_by=fund_perf_data.created_by)
    iq_session.execute(fund_perf_query)
    sql_logger.info('Update/Insert success - fund_performance')


def put_market_cap(market_cap_data):
    """
    Adds a new record/Updates the values if already exists

    :param market_cap_data: Market cap record of the Fund for the reporting date
    """
    sql_logger.info('Update/Insert - fund_market_cap_details')
    if market_cap_data:
        for data in market_cap_data:
            if is_market_cap_exist(data.fund_code, data.end_date, data.type_market_cap) is 1:
                market_cap_query = update(model.FundMarketCapDetails).\
                    where(model.FundMarketCapDetails.fund_code == data.fund_code).\
                    where(model.FundMarketCapDetails.end_date == data.end_date).\
                    where(model.FundMarketCapDetails.type_market_cap == data.type_market_cap).values(
                    fund_code=data.fund_code, type_market_cap=data.type_market_cap, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            else:
                market_cap_query = insert(model.FundMarketCapDetails).values(
                    fund_code=data.fund_code, type_market_cap=data.type_market_cap, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            iq_session.execute(market_cap_query)
    sql_logger.info('Update/Insert success - fund_market_cap_details')


def put_fund_portfolio(portfolio_data):
    """
    Adds a new record/Updates the values if already exists

    :param portfolio_data: Portfolio holdings record of the Fund for the reporting date
    """
    sql_logger.info('Update/Insert - fund_portfolio_details')
    if portfolio_data:
        for data in portfolio_data:
            if is_fund_portfolio_exist(data.fund_code, data.end_date, data.security_isin):
                fund_portfolio = update(model.FundPortfolioDetails).\
                    where(model.FundPortfolioDetails.fund_code == data.fund_code).\
                    where(model.FundPortfolioDetails.end_date == data.end_date).where(
                    model.FundPortfolioDetails.security_isin == data.security_isin).values(
                    fund_code=data.fund_code, security_isin=data.security_isin, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            else:
                fund_portfolio = insert(model.FundPortfolioDetails).values(
                    fund_code=data.fund_code, security_isin=data.security_isin, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            iq_session.execute(fund_portfolio)
    sql_logger.info('Update/Insert success - fund_portfolio_details')


def put_fund_sector(sector_data):
    """
    Adds a new record/Updates the values if already exists

    :param sector_data: Sectors record of the Fund for the reporting date
    """
    sql_logger.info('Update/Insert - fund_sector_details')
    if sector_data:
        for data in sector_data:
            if is_fund_sector_exist(data.fund_code, data.end_date, data.sector_type_name):
                fund_sector = update(model.FundSectorDetails).\
                    where(model.FundSectorDetails.fund_code == data.fund_code).\
                    where(model.FundSectorDetails.end_date == data.end_date).where(
                    model.FundSectorDetails.sector_type_name == data.sector_type_name).values(
                    fund_code=data.fund_code, sector_type_name=data.sector_type_name, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            else:
                fund_sector = insert(model.FundSectorDetails).values(
                    fund_code=data.fund_code, sector_type_name=data.sector_type_name, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            iq_session.execute(fund_sector)
    sql_logger.info('Update/Insert success - fund_sector_details')


def put_fund_ratios(fund_ratio_data):
    """
    Adds a new record/Updates the values if already exists

    :param fund_ratio_data: Fund ratios record of the Fund for the reporting date
    """
    sql_logger.info('Update/Insert - fund_ratios')
    if is_fund_ratio_exist(fund_ratio_data.fund_code, fund_ratio_data.reporting_date):
        fund_ratio = update(model.FundRatios).where(model.FundRatios.fund_code == fund_ratio_data.fund_code). \
            where(model.FundRatios.reporting_date == fund_ratio_data.reporting_date).values(
            fund_code=fund_ratio_data.fund_code, reporting_date=fund_ratio_data.reporting_date,
            full_pe_ratio=fund_ratio_data.full_pe_ratio, top5_pe_ratio=fund_ratio_data.top5_pe_ratio,
            top10_pe_ratio=fund_ratio_data.top10_pe_ratio, full_market_cap=fund_ratio_data.full_market_cap,
            top5_market_cap=fund_ratio_data.top5_market_cap, top10_market_cap=fund_ratio_data.top10_market_cap,
            standard_deviation=fund_ratio_data.standard_deviation, median=fund_ratio_data.median,
            sigma=fund_ratio_data.sigma, sortino_ratio=fund_ratio_data.sortino_ratio,
            negative_excess_returns_risk_free=fund_ratio_data.negative_excess_returns_risk_free,
            fund_alpha=fund_ratio_data.fund_alpha, updated_ts=fund_ratio_data.updated_ts,
            updated_by=fund_ratio_data.updated_by)
    else:
        fund_ratio = insert(model.FundRatios).values(
            fund_code=fund_ratio_data.fund_code, reporting_date=fund_ratio_data.reporting_date,
            full_pe_ratio=fund_ratio_data.full_pe_ratio, top5_pe_ratio=fund_ratio_data.top5_pe_ratio,
            top10_pe_ratio=fund_ratio_data.top10_pe_ratio, full_market_cap=fund_ratio_data.full_market_cap,
            top5_market_cap=fund_ratio_data.top5_market_cap, top10_market_cap=fund_ratio_data.top10_market_cap,
            standard_deviation=fund_ratio_data.standard_deviation, median=fund_ratio_data.median,
            sigma=fund_ratio_data.sigma, sortino_ratio=fund_ratio_data.sortino_ratio,
            negative_excess_returns_risk_free=fund_ratio_data.negative_excess_returns_risk_free,
            fund_alpha=fund_ratio_data.fund_alpha, updated_ts=fund_ratio_data.updated_ts,
            updated_by=fund_ratio_data.updated_by)
    iq_session.execute(fund_ratio)
    sql_logger.info('Update/Insert success - fund_ratios')


def put_collaterals(collateral_data):
    """
    Adds a new record to the table

    :param collateral_data: Collaterals record of the Fund for the reporting date
    """
    sql_logger.info('Update/Insert - collaterals')
    if not is_collaterals_exist(collateral_data.entity_code, collateral_data.reporting_date):
        collateral = insert(model.Collaterals).values(
            collateral_code=collateral_data.collateral_code, view_code=collateral_data.view_code,
            collateral_type_code=collateral_data.collateral_type_code, entity_type=collateral_data.entity_type,
            entity_code=collateral_data.entity_code, collateral_title=collateral_data.collateral_title,
            visibility_code=collateral_data.visibility_code, template_code=collateral_data.template_code,
            collateral_date=collateral_data.collateral_date, collateral_status=collateral_data.collateral_status,
            reporting_date=collateral_data.reporting_date,
            effective_start_date=collateral_data.effective_start_date, is_premium=collateral_data.is_premium,
            is_published=collateral_data.is_published, is_data_changed=collateral_data.is_data_changed,
            published_ts=collateral_data.published_ts, created_ts=collateral_data.created_ts,
            created_by=collateral_data.created_by)
        fs_session.execute(collateral)
    sql_logger.info('Update/Insert success - collaterals')
