from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, extract, func, and_, or_, update, insert

from database.orm_model import Collaterals, CollateralTemplates, FundRatios, FundBenchmarkNav, FundMarketCapDetails, \
    FundPerformance, FundPortfolioDetails, FundSectorDetails, IndexPrices, MasMarketCapTypes, MasSecurities, \
    MasSectors, PerAllFunds, RatioBasis, SecuritiesFundamentals

app_engine = create_engine('mysql://wyzeup:d0m#l1dZwhz!*9Iq0y1h@ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com/app')
fs_engine = create_engine('mysql://wyzeup:d0m#l1dZwhz!*9Iq0y1h@ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com/fs')
iq_engine = create_engine('mysql://wyzeup:d0m#l1dZwhz!*9Iq0y1h@ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com/iq')

# app_engine = create_engine('mysql://pavi:root@127.0.0.1/app')
# fs_engine = create_engine('mysql://pavi:root@127.0.0.1/fs')
# iq_engine = create_engine('mysql://pavi:root@127.0.0.1/iq')

app_db = sessionmaker(bind=app_engine)
fs_db = sessionmaker(bind=fs_engine)
iq_db = sessionmaker(bind=iq_engine)

app_session = app_db()
fs_session = fs_db()
iq_session = iq_db()


def get_nav_start_date(fund_code):
    nav_start_date = app_session.query(PerAllFunds.nav_start_date).filter_by(fund_code=fund_code).all()[0][0]
    return nav_start_date


def get_benchmark_index(fund_code):
    benchmark_index_code = app_session.query(PerAllFunds.benchmark_index_code).filter_by(fund_code=fund_code).\
        all()[0][0]
    return benchmark_index_code


def get_alt_benchmark_index(fund_code):
    alt_benchmark_index_code = app_session.query(PerAllFunds.benchmark_alt_index_code).filter_by(fund_code=fund_code).\
        all()[0][0]
    return alt_benchmark_index_code


def get_index_price_as_on_date(date, index_code):
    date_month = datetime.strptime(str(date), "%Y-%m-%d").month
    date_year = datetime.strptime(str(date), "%Y-%m-%d").year
    index_price = iq_session.query(IndexPrices.index_price_close).filter(IndexPrices.index_code == index_code). \
        filter(extract('year', IndexPrices.index_price_as_on_date) == date_year). \
        filter(extract('month', IndexPrices.index_price_as_on_date) == date_month).all()[-1][0]
    return float(index_price)


def get_start_price(start_date, index_code):
    start_price = iq_session.query(IndexPrices.index_price_close).filter_by(index_code=index_code). \
        filter_by(index_price_as_on_date=start_date).all()[0][0]
    return float(start_price)


def get_cap_type(type_desc):
    market_cap_type = iq_session.query(MasMarketCapTypes.market_cap_type_code). \
        filter_by(market_cap_type_desc=type_desc).all()[0][0]
    return market_cap_type


def get_investment_style(fund_code):
    investment_style = app_session.query(PerAllFunds.investment_style).filter_by(fund_code=fund_code).all()[0][0]
    return investment_style


def get_fund_nav(fund_code, date):
    fund_nav = iq_session.query(FundBenchmarkNav.fund_nav).filter_by(fund_code=fund_code).\
        filter_by(effective_end_date=date).all()
    return fund_nav


def get_security_isin_from_db(security_name):
    security_isin = iq_session.query(MasSecurities.security_isin).filter_by(security_name=security_name).all()[0][0]
    return security_isin


def get_all_isin():
    all_isin_list = iq_session.query(MasSecurities.security_isin, MasSecurities.security_name).all()
    return all_isin_list


def get_mcap_for_security(security_isin):
    security_mcap_code = iq_session.query(MasSecurities.market_cap_type_code).filter_by(security_isin=security_isin).\
        all()[0][0]
    return security_mcap_code


def get_sector_from_portfolio(security_isin):
    sector = iq_session.query(MasSectors.sector).filter(MasSecurities.security_isin == security_isin). \
        filter(MasSectors.industry == MasSecurities.industry).all()[0][0]
    return sector


def get_collateral_code():
    collateral_code = fs_session.query(func.codeGenerator('COLLATERAL')).all()[0][0]
    return collateral_code


def get_collateral_view_code():
    collateral_view_code = fs_session.query(func.codeGenerator('COLLATERAL-VIEW')).all()[0][0]
    return collateral_view_code


def get_fund_short_code(fund_code):
    fund_short_code = app_session.query(PerAllFunds.fund_short_code).filter_by(fund_code=fund_code).all()[0][0]
    return fund_short_code


def get_default_visibility_code(fund_code):
    default_visibility_code = fs_session.query(CollateralTemplates.default_visibility_code). \
        filter_by(entity_type='FUND').filter_by(template_type_code='FINTUPLE').filter_by(entity_code=fund_code). \
        all()[0][0]
    return default_visibility_code


def get_collateral_template_code(fund_code, reporting_date):
    collateral_template_code = fs_session.query(CollateralTemplates.template_code).filter(
        CollateralTemplates.entity_code == fund_code).filter(
        CollateralTemplates.template_type_code == 'FINTUPLE').filter(
        or_(and_(reporting_date >= CollateralTemplates.effective_start_date,
                 CollateralTemplates.effective_end_date.is_(None)),
            and_(CollateralTemplates.effective_start_date >= reporting_date,
                 CollateralTemplates.effective_end_date <= reporting_date))).all()[0][0]
    return collateral_template_code


def get_pe_ratio(security_isin_list):
    pe_ratio_list = []
    for security in security_isin_list:
        pe_ratio = iq_session.query(SecuritiesFundamentals.pe_ratio). \
            filter_by(security_isin=security.security_isin).order_by(SecuritiesFundamentals.as_on_date.desc()). \
            limit(1).all()
        if any(pe_ratio) is False:
            pe_ratio_body = {"security_isin": security.security_isin, "pe_ratio": 0}
        elif pe_ratio[0][0] is None:
            pe_ratio_body = {"security_isin": security.security_isin, "pe_ratio": 0}
        else:
            pe_ratio_body = {"security_isin": security.security_isin, "pe_ratio": pe_ratio[0][0]}
        pe_ratio_list.append(pe_ratio_body)
    return pe_ratio_list


def get_fund_ratio_mcap(security_isin_list):
    fund_ratio_mcap_list = []
    for security in security_isin_list:
        fund_ratio_mcap = iq_session.query(SecuritiesFundamentals.market_cap). \
            filter_by(security_isin=security.security_isin).order_by(SecuritiesFundamentals.as_on_date.desc()). \
            limit(1).all()
        if any(fund_ratio_mcap) is False:
            fund_ratio_mcap_body = {"security_isin": security.security_isin, "market_cap": 0}
        elif fund_ratio_mcap[0][0] is None:
            fund_ratio_mcap_body = {"security_isin": security.security_isin, "market_cap": 0}
        else:
            fund_ratio_mcap_body = {"security_isin": security.security_isin, "market_cap": fund_ratio_mcap[0][0]}
        fund_ratio_mcap_list.append(fund_ratio_mcap_body)
    return fund_ratio_mcap_list


def get_all_1m_perf(fund_code):
    fund_return = iq_session.query(FundPerformance.perf_1m).filter_by(fund_code=fund_code).all()
    fund_return_list = []
    for return_value in fund_return:
        if return_value[0] is None:
            fund_return_list.append(0)
        else:
            fund_return_list.append(float(return_value[0]))
    return fund_return_list


def get_risk_free_rate():
    risk_free_rate = iq_session.query(RatioBasis.risk_free_return_rate).all()[0][0]
    return float(risk_free_rate)


def is_nav_exist(fund_code, effective_end_date):
    is_nav = iq_session.query(FundBenchmarkNav).filter_by(fund_code=fund_code). \
        filter_by(effective_end_date=effective_end_date).count()
    return is_nav


def is_fund_performance_exist(fund_code, effective_end_date):
    is_fund_performance = iq_session.query(FundPerformance).filter_by(fund_code=fund_code). \
        filter_by(effective_end_date=effective_end_date).count()
    return is_fund_performance


def is_market_cap_exist(fund_code, end_date, type_market_cap):
    is_market_cap = iq_session.query(FundMarketCapDetails).filter_by(fund_code=fund_code). \
        filter_by(end_date=end_date).filter_by(type_market_cap=type_market_cap).count()
    return is_market_cap


def is_fund_portfolio_exist(fund_code, end_date, security_isin):
    is_fund_portfolio = iq_session.query(FundPortfolioDetails).filter_by(fund_code=fund_code). \
        filter_by(end_date=end_date).filter_by(security_isin=security_isin).count()
    return is_fund_portfolio


def is_fund_sector_exist(fund_code, end_date, sector_type_name):
    is_fund_sector = iq_session.query(FundSectorDetails).filter_by(fund_code=fund_code).filter_by(end_date=end_date). \
        filter_by(sector_type_name=sector_type_name).count()
    return is_fund_sector


def is_collaterals_exist(fund_code, reporting_date):
    is_collateral = fs_session.query(Collaterals).filter_by(entity_code=fund_code). \
        filter_by(reporting_date=reporting_date).count()
    return is_collateral


def is_fund_ratio_exist(fund_code, reporting_date):
    is_fund_ratio = iq_session.query(FundRatios).filter_by(fund_code=fund_code). \
        filter_by(reporting_date=reporting_date).count()
    return is_fund_ratio


def update_islatest(fund_code, previous_1m_end_date):
    islatest_update = update(FundPerformance).where(FundPerformance.fund_code == fund_code). \
        where(FundPerformance.effective_end_date == previous_1m_end_date).values(isLatest=None)
    iq_engine.execute(islatest_update)


def put_fund_benchmark_nav(nav_data):
    if is_nav_exist(nav_data.fund_code, nav_data.effective_end_date):
        nav_query = update(FundBenchmarkNav).where(FundBenchmarkNav.fund_code == nav_data.fund_code). \
            where(FundBenchmarkNav.effective_end_date == nav_data.effective_end_date). \
            values(fund_code=nav_data.fund_code, benchmark_index_code=nav_data.benchmark_index_code,
                   alt_benchmark_index_code=nav_data.alt_benchmark_index_code, fund_nav=nav_data.fund_nav,
                   benchmark_nav=nav_data.benchmark_nav, alt_benchmark_nav=nav_data.alt_benchmark_nav,
                   effective_end_date=nav_data.effective_end_date)
    else:
        nav_query = insert(FundBenchmarkNav). \
            values(fund_code=nav_data.fund_code, benchmark_index_code=nav_data.benchmark_index_code,
                   alt_benchmark_index_code=nav_data.alt_benchmark_index_code, fund_nav=nav_data.fund_nav,
                   benchmark_nav=nav_data.benchmark_nav, alt_benchmark_nav=nav_data.alt_benchmark_nav,
                   effective_end_date=nav_data.effective_end_date)
    iq_engine.execute(nav_query)


def put_fund_performance(fund_perf_data, benchmark_perf_data, alt_benchmark_perf_data):
    if is_fund_performance_exist(fund_perf_data.fund_code, fund_perf_data.effective_end_date):
        fund_perf_query = update(FundPerformance).where(FundPerformance.fund_code == fund_perf_data.fund_code). \
            where(FundPerformance.effective_end_date == fund_perf_data.effective_end_date).values(
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
        fund_perf_query = insert(FundPerformance).values(
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
    iq_engine.execute(fund_perf_query)


def put_market_cap(market_cap_data):
    if market_cap_data:
        for data in market_cap_data:
            if is_market_cap_exist(data.fund_code, data.end_date, data.type_market_cap) is 1:
                market_cap_query = update(FundMarketCapDetails).\
                    where(FundMarketCapDetails.fund_code == data.fund_code).\
                    where(FundMarketCapDetails.end_date == data.end_date).\
                    where(FundMarketCapDetails.type_market_cap == data.type_market_cap).values(
                    fund_code=data.fund_code, type_market_cap=data.type_market_cap, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            else:
                market_cap_query = insert(FundMarketCapDetails).values(
                    fund_code=data.fund_code, type_market_cap=data.type_market_cap, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            iq_engine.execute(market_cap_query)


def put_fund_portfolio(portfolio_data):
    if portfolio_data:
        for data in portfolio_data:
            if is_fund_portfolio_exist(data.fund_code, data.end_date, data.security_isin):
                fund_portfolio = update(FundPortfolioDetails).where(FundPortfolioDetails.fund_code == data.fund_code). \
                    where(FundPortfolioDetails.end_date == data.end_date).where(
                    FundPortfolioDetails.security_isin == data.security_isin).values(
                    fund_code=data.fund_code, security_isin=data.security_isin, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            else:
                fund_portfolio = insert(FundPortfolioDetails).values(
                    fund_code=data.fund_code, security_isin=data.security_isin, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            iq_engine.execute(fund_portfolio)


def put_fund_sector(sector_data):
    if sector_data:
        for data in sector_data:
            if is_fund_sector_exist(data.fund_code, data.end_date, data.sector_type_name):
                fund_sector = update(FundSectorDetails).where(FundSectorDetails.fund_code == data.fund_code). \
                    where(FundSectorDetails.end_date == data.end_date).where(
                    FundSectorDetails.sector_type_name == data.sector_type_name).values(
                    fund_code=data.fund_code, sector_type_name=data.sector_type_name, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            else:
                fund_sector = insert(FundSectorDetails).values(
                    fund_code=data.fund_code, sector_type_name=data.sector_type_name, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            iq_engine.execute(fund_sector)


def put_fund_ratios(fund_ratio_data):
    if is_fund_ratio_exist(fund_ratio_data.fund_code, fund_ratio_data.reporting_date):
        fund_ratio = update(FundRatios).where(FundRatios.fund_code == fund_ratio_data.fund_code). \
            where(FundRatios.reporting_date == fund_ratio_data.reporting_date).values(
            fund_code=fund_ratio_data.fund_code, reporting_date=fund_ratio_data.reporting_date,
            top5_pe_ratio=fund_ratio_data.top5_pe_ratio, top10_pe_ratio=fund_ratio_data.top10_pe_ratio,
            top5_market_cap=fund_ratio_data.top5_market_cap, top10_market_cap=fund_ratio_data.top10_market_cap,
            standard_deviation=fund_ratio_data.standard_deviation, median=fund_ratio_data.median,
            sigma=fund_ratio_data.sigma, sortino_ratio=fund_ratio_data.sortino_ratio,
            negative_excess_returns_risk_free=fund_ratio_data.negative_excess_returns_risk_free,
            fund_alpha=fund_ratio_data.fund_alpha, updated_ts=fund_ratio_data.updated_ts,
            updated_by=fund_ratio_data.updated_by)
    else:
        fund_ratio = insert(FundRatios).values(
            fund_code=fund_ratio_data.fund_code, reporting_date=fund_ratio_data.reporting_date,
            top5_pe_ratio=fund_ratio_data.top5_pe_ratio, top10_pe_ratio=fund_ratio_data.top10_pe_ratio,
            top5_market_cap=fund_ratio_data.top5_market_cap, top10_market_cap=fund_ratio_data.top10_market_cap,
            standard_deviation=fund_ratio_data.standard_deviation, median=fund_ratio_data.median,
            sigma=fund_ratio_data.sigma, sortino_ratio=fund_ratio_data.sortino_ratio,
            negative_excess_returns_risk_free=fund_ratio_data.negative_excess_returns_risk_free,
            fund_alpha=fund_ratio_data.fund_alpha, updated_ts=fund_ratio_data.updated_ts,
            updated_by=fund_ratio_data.updated_by)
    iq_engine.execute(fund_ratio)


def put_collaterals(collateral_data):
    if not is_collaterals_exist(collateral_data.entity_code, collateral_data.reporting_date):
        collateral = insert(Collaterals).values(
            collateral_code=collateral_data.collateral_code, view_code=collateral_data.view_code,
            collateral_type_code=collateral_data.collateral_type_code, entity_type=collateral_data.entity_type,
            entity_code=collateral_data.entity_code, collateral_title=collateral_data.collateral_title,
            visibility_code=collateral_data.visibility_code, template_code=collateral_data.template_code,
            collateral_date=collateral_data.collateral_date, collateral_status=collateral_data.collateral_status,
            reporting_date=collateral_data.reporting_date, effective_start_date=collateral_data.effective_start_date,
            is_premium=collateral_data.is_premium, is_published=collateral_data.is_published,
            is_data_changed=collateral_data.is_data_changed, published_ts=collateral_data.published_ts,
            created_ts=collateral_data.created_ts, created_by=collateral_data.created_by)
        fs_engine.execute(collateral)


fs_session.commit()
iq_session.commit()

app_session.close()
fs_session.close()
iq_session.close()
