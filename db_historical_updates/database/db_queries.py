import database.orm_model as model
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, extract, func, and_, or_, update, insert

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


def get_fund_dates(fund_code):
    fund_dates_details = (iq_session.query(model.FundPerformance.effective_end_date).filter_by(fund_code=fund_code).
                          order_by(model.FundPerformance.effective_end_date).all())
    fund_dates_list = []
    for date in fund_dates_details:
        fund_dates_list.append(date)
    return fund_dates_list


def get_collateral_code():
    collateral_code = fs_session.query(func.codeGenerator('COLLATERAL')).all()[0][0]
    return collateral_code


def get_collateral_view_code():
    collateral_view_code = fs_session.query(func.codeGenerator('COLLATERAL-VIEW')).all()[0][0]
    return collateral_view_code


def get_fund_short_code(fund_code):
    fund_short_code = app_session.query(model.PerAllFunds.fund_short_code).filter_by(fund_code=fund_code).all()[0][0]
    return fund_short_code


def get_default_visibility_code(fund_code):
    default_visibility_code = (fs_session.query(model.CollateralTemplates.default_visibility_code).
                               filter_by(entity_type='FUND').filter_by(template_type_code='FINTUPLE').
                               filter_by(entity_code=fund_code).all()[0][0])
    return default_visibility_code


def get_collateral_template_code(fund_code, reporting_date):
    collateral_template_code = (fs_session.query(model.CollateralTemplates.template_code).
                                filter(model.CollateralTemplates.entity_code == fund_code).
                                filter(model.CollateralTemplates.template_type_code == 'FINTUPLE').
                                filter(or_(and_(reporting_date >= model.CollateralTemplates.effective_start_date,
                                                model.CollateralTemplates.effective_end_date.is_(None)),
                                           and_(model.CollateralTemplates.effective_start_date >= reporting_date,
                                                model.CollateralTemplates.effective_end_date <= reporting_date))).
                                all()[0][0])
    return collateral_template_code


def get_benchmark_info(fund_code):
    benchmark_info = (app_session.query().with_entities(model.PerAllFunds.nav_start_date,
                                                        model.PerAllFunds.benchmark_index_code).
                      filter_by(fund_code=fund_code).all())[0]
    return benchmark_info


def get_alt_benchmark_info(fund_code):
    alt_benchmark_info = (app_session.query().with_entities(model.PerAllFunds.nav_start_date,
                                                            model.PerAllFunds.benchmark_alt_index_code).
                          filter_by(fund_code=fund_code).all())[0]
    return alt_benchmark_info


def get_nav_dates(fund_code):
    nav_dates_query = (iq_session.query(model.FundBenchmarkNav.effective_end_date).filter_by(fund_code=fund_code).
                       order_by(model.FundBenchmarkNav.effective_end_date).all())
    nav_dates_list = [date[0] for date in nav_dates_query]
    return nav_dates_list


def get_start_price(start_date, index_code):
    start_index_price = float(iq_session.query(model.IndexPrices.index_price_close).filter_by(index_code=index_code).
                              filter_by(index_price_as_on_date=start_date).all()[0][0])
    return start_index_price


def get_index_price_as_on_date(date, index_code):
    date_month = datetime.strptime(str(date), "%Y-%m-%d").month
    date_year = datetime.strptime(str(date), "%Y-%m-%d").year
    index_price = (iq_session.query(model.IndexPrices.index_price_close).
                   filter(model.IndexPrices.index_code == index_code).
                   filter(extract('year', model.IndexPrices.index_price_as_on_date) == date_year).
                   filter(extract('month', model.IndexPrices.index_price_as_on_date) == date_month).all())[0]
    return index_price


def get_portfolio_dates(fund_code):
    portfolio_date_details = (iq_session.query(model.FundPortfolioDetails.end_date.distinct().label('end_date')).
                              filter_by(fund_code=fund_code).all())
    portfolio_date_list = [date for date in portfolio_date_details]
    return portfolio_date_list


def get_portfolio_details(fund_code, reporting_date):
    portfolio_details = (iq_session.query().with_entities(model.FundPortfolioDetails.security_isin,
                                                          model.FundPortfolioDetails.exposure).
                         filter_by(fund_code=fund_code).filter_by(end_date=reporting_date).all())
    portfolio_values = []
    for value in portfolio_details:
        value_body = {'security_isin': value[0], 'exposure': value[1]}
        portfolio_values.append(value_body)
    return portfolio_values


def get_mcap_for_security(security_isin):
    security_mcap_code = (iq_session.query(model.MasSecurities.market_cap_type_code).
                          filter_by(security_isin=security_isin).all()[0][0])
    return security_mcap_code


def get_reporting_dates(fund_code):
    reporting_dates = (iq_session.query(model.FundPerformance.effective_end_date).filter_by(fund_code=fund_code).
                       order_by(model.FundPerformance.effective_end_date).all())[0]
    reporting_dates_list = []
    for date in reporting_dates:
        reporting_dates_list.append(date[0])
    return reporting_dates_list


def get_benchmark_index(fund_code):
    benchmark_index_code = (app_session.query(model.PerAllFunds.benchmark_index_code).filter_by(fund_code=fund_code).
                            all()[0][0])
    return benchmark_index_code


def get_alt_benchmark_index(fund_code):
    alt_benchmark_index_code = (app_session.query(model.PerAllFunds.benchmark_alt_index_code).
                                filter_by(fund_code=fund_code).all()[0][0])
    return alt_benchmark_index_code


def get_nav_start_date(fund_code):
    nav_start_date = app_session.query(model.PerAllFunds.nav_start_date).filter_by(fund_code=fund_code).all()[0][0]
    return nav_start_date


def get_fund_nav(fund_code, date):
    fund_nav = (iq_session.query(model.FundBenchmarkNav.fund_nav).filter_by(fund_code=fund_code).
                filter_by(effective_end_date=date).all())
    return fund_nav


def get_investment_style(fund_code):
    investment_style = app_session.query(model.PerAllFunds.investment_style).filter_by(fund_code=fund_code).all()[0][0]
    return investment_style


def get_mcap_dates(fund_code):
    mcap_date = (iq_session.query(model.FundMarketCapDetails.end_date.distinct().label('end_date')).
                 filter_by(fund_code=fund_code).order_by(model.FundMarketCapDetails.end_date).all())[0]
    return mcap_date


def get_monthly_market_cap(fund_code, end_date):
    monthly_mcap = (iq_session.query().with_entities(model.FundMarketCapDetails.type_market_cap,
                                                     model.FundMarketCapDetails.exposure).
                    filter_by(fund_code=fund_code).filter_by(end_date=end_date).all())
    return monthly_mcap


def get_fund_code_fund_perf():
    fund_codes_query = app_session.query(model.PerAllFunds.fund_code).all()
    fund_code_list = []
    for fund in fund_codes_query:
        fund_code_list.append(fund[0])
    return fund_code_list


def get_fund_codes_fund_ratios(fund_code):
    fund_code_list = (iq_session.query().with_entities(model.FundPerformance.fund_code,
                                                       model.FundPerformance.effective_end_date).
                      filter(model.FundPerformance.fund_code == fund_code).all())
    return fund_code_list


def get_cap_type(type_desc):
    cap_type_code = (iq_session.query(model.MasMarketCapTypes.market_cap_type_code).
                     filter_by(market_cap_type_desc=type_desc).all()[0][0])
    return cap_type_code


def get_security_isin(security_name):
    security_isin = (iq_session.query(model.MasSecurities.security_isin).filter(
                     or_(security_name=security_name, bse_security_symbol=security_name)).all()[0][0])[0]
    return security_isin


def get_all_isin():
    all_isin_list = iq_session.query(model.MasSecurities.security_isin, model.MasSecurities.security_name).all()
    return all_isin_list


def get_fund_portfolio(fund_code, reporting_date):
    portfolio_details = (iq_session.query().with_entities(model.FundPortfolioDetails.security_isin,
                                                          model.FundPortfolioDetails.exposure).
                         filter_by(fund_code=fund_code).filter_by(end_date=reporting_date).all())
    return portfolio_details


def get_benchmark_perf_1m(fund_code, reporting_date):
    bm_perf_1m = (iq_session.query(model.FundPerformance.benchmark_perf_1m).filter_by(fund_code=fund_code).
                  filter_by(effective_end_date=reporting_date).all()[0][0])
    return float(bm_perf_1m)


def get_all_fund_return(fund_code, reporting_date):
    fund_return_details = (iq_session.query(model.FundPerformance.perf_1m).
                           filter(model.FundPerformance.fund_code == fund_code).
                           filter(model.FundPerformance.effective_end_date <= reporting_date).all())
    fund_return_list = []
    for return_value in fund_return_details:
        if return_value[0] is None:
            fund_return_list.append(0)
        else:
            fund_return_list.append(float(return_value[0]))
    return fund_return_list


def get_pe_ratio(security_isin_list):
    pe_ratio_list = []
    for security in security_isin_list:
        pe_ratio = (iq_session.query(model.SecuritiesFundamentals.pe_ratio).
                    filter_by(security_isin=security.security_isin).
                    order_by(model.SecuritiesFundamentals.as_on_date.desc()).limit(1).all())[0]
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
        fund_ratio_mcap = (iq_session.query(model.SecuritiesFundamentals.market_cap).
                           filter_by(security_isin=security.security_isin).
                           order_by(model.SecuritiesFundamentals.as_on_date.desc()).limit(1).all())[0]
        if any(fund_ratio_mcap) is False:
            fund_ratio_mcap_body = {"security_isin": security.security_isin, "market_cap": 0}
        elif fund_ratio_mcap[0][0] is None:
            fund_ratio_mcap_body = {"security_isin": security.security_isin, "market_cap": 0}
        else:
            fund_ratio_mcap_body = {"security_isin": security.security_isin, "market_cap": fund_ratio_mcap[0][0]}
        fund_ratio_mcap_list.append(fund_ratio_mcap_body)
    return fund_ratio_mcap_list


def get_risk_free_rate():
    risk_free_rate = iq_session.query(model.RatioBasis.risk_free_return_rate).all()[0][0]
    return float(risk_free_rate)


def get_sector_from_portfolio(security_isin):
    sector = (iq_session.query(model.MasSectors.sector).filter(model.MasSecurities.security_isin == security_isin).
              filter(model.MasSectors.industry == model.MasSecurities.industry).all())
    return sector


def get_mas_indices():
    mas_indices_query = iq_session.query(func.distinct(model.MasIndices.index_code)).all()
    mas_indices = [index[0] for index in mas_indices_query]
    return mas_indices


def get_index_start_date(index_code):
    start_date = (iq_session.query(model.IndexPrices.index_price_as_on_date).filter_by(index_code=index_code).
                  order_by(model.IndexPrices.index_price_as_on_date.asc()).limit(1).all()[0][0])[0]
    return start_date


def get_index_start_price(index_code, start_date):
    start_index_price = (iq_session.query(model.IndexPrices.index_price_close).filter_by(index_code=index_code).
                         filter_by(index_price_as_on_date=start_date).all()[0][0])[0]
    return float(start_index_price)


def is_collaterals_exist(fund_code, reporting_date):
    is_collateral = (fs_session.query(model.Collaterals).filter_by(entity_code=fund_code).
                     filter_by(reporting_date=reporting_date).count())
    return is_collateral


def is_market_cap_exist(fund_code, end_date, type_market_cap):
    is_market_cap = (iq_session.query(model.FundMarketCapDetails).filter_by(fund_code=fund_code).
                     filter_by(end_date=end_date).filter_by(type_market_cap=type_market_cap).count())
    return is_market_cap


def is_fund_performance_exist(fund_code, effective_end_date):
    is_fund_performance = (iq_session.query(model.FundPerformance).filter_by(fund_code=fund_code).
                           filter_by(effective_end_date=effective_end_date).count())
    return is_fund_performance


def is_fund_portfolio_exist(fund_code, end_date, security_isin):
    is_fund_portfolio = (iq_session.query(model.FundPortfolioDetails).filter_by(fund_code=fund_code).
                         filter_by(end_date=end_date).filter_by(security_isin=security_isin).count())
    return is_fund_portfolio


def is_fund_ratio_exist(fund_code, reporting_date):
    is_fund_ratio = (iq_session.query(model.FundRatios).filter_by(fund_code=fund_code).
                     filter_by(reporting_date=reporting_date).count())
    return is_fund_ratio


def is_fund_sector_exist(fund_code, end_date, sector_type_name):
    is_fund_sector = (iq_session.query(model.FundSectorDetails).filter_by(fund_code=fund_code).
                      filter_by(end_date=end_date).filter_by(sector_type_name=sector_type_name).count())
    return is_fund_sector


def is_index_performance_exist(index_code, reporting_date):
    is_index_performance = (iq_session.query(model.IndexPerformance).filter_by(index_code=index_code).
                            filter_by(reporting_date=reporting_date).count())[0]
    return is_index_performance


def put_collaterals_data(collateral_data):
    collateral_query = insert(model.Collaterals).values(
        collateral_code=collateral_data.collateral_code, view_code=collateral_data.view_code,
        collateral_type_code=collateral_data.collateral_type_code, entity_type=collateral_data.entity_type,
        entity_code=collateral_data.entity_code, collateral_title=collateral_data.collateral_title,
        visibility_code=collateral_data.visibility_code, template_code=collateral_data.template_code,
        collateral_date=collateral_data.collateral_date, collateral_status=collateral_data.collateral_status,
        reporting_date=collateral_data.reporting_date, effective_start_date=collateral_data.effective_start_date,
        is_premium=collateral_data.is_premium, is_published=collateral_data.is_published,
        is_data_changed=collateral_data.is_data_changed, published_ts=collateral_data.published_ts,
        created_ts=collateral_data.created_ts, created_by=collateral_data.created_by)
    fs_engine.execute(collateral_query)


def put_market_cap_data(marketcap_data):
    for data in marketcap_data:
        if is_market_cap_exist(data.fund_code, data.end_date, data.type_market_cap):
            market_cap_query = update(model.FundMarketCapDetails).where(
                model.FundMarketCapDetails.fund_code == data.fund_code).where(
                model.FundMarketCapDetails.end_date == data.end_date).where(
                model.FundMarketCapDetails.type_market_cap == data.type_market_cap).values(
                type_market_cap=data.type_market_cap, exposure=data.exposure)
        else:
            market_cap_query = insert(model.FundMarketCapDetails).values(
                fund_code=data.fund_code, type_market_cap=data.type_market_cap, exposure=data.exposure,
                start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                action_by=data.action_by)
        iq_engine.execute(market_cap_query)


def put_new_fund_nav_data(fund_bm_data):
    fund_bm_nav_query = insert(model.FundBenchmarkNav).values(
        fund_code=fund_bm_data.fund_code, benchmark_index_code=fund_bm_data.benchmark_index_code,
        alt_benchmark_index_code=fund_bm_data.alt_benchmark_index_code, fund_nav=fund_bm_data.fund_nav,
        benchmark_nav=fund_bm_data.benchmark_nav, alt_benchmark_nav=fund_bm_data.alt_benchmark_nav,
        effective_end_date=fund_bm_data.effective_end_date)
    iq_engine.execute(fund_bm_nav_query)


def put_fund_nav(fund_code, fund_nav, date):
    fund_nav_query = update(model.FundBenchmarkNav).where(model.FundBenchmarkNav.fund_code == fund_code).where(
        model.FundBenchmarkNav.effective_end_date == date).values(fund_nav=fund_nav)
    iq_engine.execute(fund_nav_query)


def put_fund_bm_nav(fund_code, benchmark_nav, date):
    bm_nav_query = update(model.FundBenchmarkNav).where(model.FundBenchmarkNav.fund_code == fund_code).where(
        model.FundBenchmarkNav.effective_end_date == date).values(benchmark_nav=benchmark_nav)
    iq_engine.execute(bm_nav_query)


def put_fund_alt_bm_nav(fund_code, alt_benchmark_nav, date):
    alt_bm_nav_query = update(model.FundBenchmarkNav).where(model.FundBenchmarkNav.fund_code == fund_code).where(
        model.FundBenchmarkNav.effective_end_date == date).values(alt_benchmark_nav=alt_benchmark_nav)
    iq_engine.execute(alt_bm_nav_query)


def put_benchmark_performance(fund_code, reporting_date, benchmark_perf_data):
    benchmark_perf_query = update(model.FundPerformance).where(model.FundPerformance.fund_code == fund_code).where(
        model.FundPerformance.effective_end_date == reporting_date).values(
        benchmark_perf_1m=benchmark_perf_data.benchmark_perf_1m,
        benchmark_perf_3m=benchmark_perf_data.benchmark_perf_3m,
        benchmark_perf_6m=benchmark_perf_data.benchmark_perf_6m,
        benchmark_perf_1y=benchmark_perf_data.benchmark_perf_1y,
        benchmark_perf_2y=benchmark_perf_data.benchmark_perf_2y,
        benchmark_perf_3y=benchmark_perf_data.benchmark_perf_3y,
        benchmark_perf_5y=benchmark_perf_data.benchmark_perf_5y,
        benchmark_perf_inception=benchmark_perf_data.benchmark_perf_inception)
    iq_engine.execute(benchmark_perf_query)


def put_alt_benchmark_performance(fund_code, reporting_date, alt_benchmark_perf_data):
    benchmark_perf_query = update(model.FundPerformance).where(model.FundPerformance.fund_code == fund_code).where(
        model.FundPerformance.effective_end_date == reporting_date).values(
        alt_benchmark_perf_1m=alt_benchmark_perf_data.alt_benchmark_perf_1m,
        alt_benchmark_perf_3m=alt_benchmark_perf_data.alt_benchmark_perf_3m,
        alt_benchmark_perf_6m=alt_benchmark_perf_data.alt_benchmark_perf_6m,
        alt_benchmark_perf_1y=alt_benchmark_perf_data.alt_benchmark_perf_1y,
        alt_benchmark_perf_2y=alt_benchmark_perf_data.alt_benchmark_perf_2y,
        alt_benchmark_perf_3y=alt_benchmark_perf_data.alt_benchmark_perf_3y,
        alt_benchmark_perf_5y=alt_benchmark_perf_data.alt_benchmark_perf_5y,
        alt_benchmark_perf_inception=alt_benchmark_perf_data.alt_benchmark_perf_inception)
    iq_engine.execute(benchmark_perf_query)


def update_islatest(fund_code, previous_1m_end_date):
    update_islatest = update(model.FundPerformance).where(model.FundPerformance.fund_code == fund_code).where(
        model.FundPerformance.effective_end_date == previous_1m_end_date).values(isLatest=None)
    iq_engine.execute(update_islatest)


def put_fund_performance(fund_perf_data, benchmark_perf_data, alt_benchmark_perf_data):
    if is_fund_performance_exist(fund_perf_data.fund_code, fund_perf_data.effective_end_date):
        fund_perf_query = update(model.FundPerformance).where(
            model.FundPerformance.fund_code == fund_perf_data.fund_code).where(
            model.FundPerformance.effective_end_date == fund_perf_data.effective_end_date).values(
            investment_style_type_code=fund_perf_data.investment_style_type_code, perf_1m=fund_perf_data.perf_1m,
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
            alt_benchmark_perf_inception=alt_benchmark_perf_data.alt_benchmark_perf_inception)
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
    iq_engine.execute(fund_perf_query)


def put_mcap_type_code_fundperf(market_cap):
    mcap_type_code_query = update(model.FundPerformance).where(
        model.FundPerformance.fund_code == market_cap['fund_code']).where(
        model.FundPerformance.effective_end_date == market_cap['date']).values(
        market_cap_type_code=market_cap['market_cap_type_code'])
    iq_engine.execute(mcap_type_code_query)


def put_fund_portfolio(portfolio_data):
    if portfolio_data:
        if is_fund_portfolio_exist(portfolio_data.fund_code, portfolio_data.end_date, portfolio_data.security_isin):
            fund_portfolio = update(model.FundPortfolioDetails).where(
                model.FundPortfolioDetails.fund_code == portfolio_data.fund_code).where(
                model.FundPortfolioDetails.end_date == portfolio_data.end_date).where(
                model.FundPortfolioDetails.security_isin == portfolio_data.security_isin).values(
                security_isin=portfolio_data.security_isin, exposure=portfolio_data.exposure)
        else:
            fund_portfolio = insert(model.FundPortfolioDetails).values(
                fund_code=portfolio_data.fund_code, security_isin=portfolio_data.security_isin,
                exposure=portfolio_data.exposure, start_date=portfolio_data.start_date,
                end_date=portfolio_data.end_date, created_ts=portfolio_data.created_ts,
                action_by=portfolio_data.action_by)
        iq_engine.execute(fund_portfolio)


def put_fund_ratios(fund_ratio_data):
    if not is_fund_ratio_exist(fund_ratio_data.fund_code, fund_ratio_data.reporting_date):
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
    else:
        fund_ratio = update(model.FundRatios).where(model.FundRatios.fund_code == fund_ratio_data.fund_code).where(
            model.FundRatios.reporting_date == fund_ratio_data.reporting_date).values(
            fund_code=fund_ratio_data.fund_code, reporting_date=fund_ratio_data.reporting_date,
            full_pe_ratio=fund_ratio_data.full_pe_ratio, top5_pe_ratio=fund_ratio_data.top5_pe_ratio,
            top10_pe_ratio=fund_ratio_data.top10_pe_ratio, full_market_cap=fund_ratio_data.full_market_cap,
            top5_market_cap=fund_ratio_data.top5_market_cap, top10_market_cap=fund_ratio_data.top10_market_cap,
            standard_deviation=fund_ratio_data.standard_deviation, median=fund_ratio_data.median,
            sigma=fund_ratio_data.sigma, sortino_ratio=fund_ratio_data.sortino_ratio,
            negative_excess_returns_risk_free=fund_ratio_data.negative_excess_returns_risk_free,
            fund_alpha=fund_ratio_data.fund_alpha, updated_ts=fund_ratio_data.updated_ts,
            updated_by=fund_ratio_data.updated_by)
    iq_engine.execute(fund_ratio)


def put_fund_sector(sector_data):
    if sector_data:
        for data in sector_data:
            if is_fund_sector_exist(data.fund_code, data.end_date, data.sector_type_name):
                fund_sector = update(model.FundSectorDetails).where(
                    model.FundSectorDetails.fund_code == data.fund_code).where(
                    model.FundSectorDetails.end_date == data.end_date).where(
                    model.FundSectorDetails.sector_type_name == data.sector_type_name).values(
                    fund_code=data.fund_code, sector_type_name=data.sector_type_name, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            else:
                fund_sector = insert(model.FundSectorDetails).values(
                    fund_code=data.fund_code, sector_type_name=data.sector_type_name, exposure=data.exposure,
                    start_date=data.start_date, end_date=data.end_date, created_ts=data.created_ts,
                    action_by=data.action_by)
            iq_engine.execute(fund_sector)


def put_index_performance(index_data):
    if is_index_performance_exist(index_data.index_code, index_data.reporting_date):
        index_perf = update(model.IndexPerformance).where(
            model.IndexPerformance.index_code == index_data.index_code).where(
            model.IndexPerformance.reporting_date == index_data.reporting_date).values(
            index_code=index_data.index_code, standard_deviation=index_data.standard_deviation,
            pe_ratio=index_data.pe_ratio, top_sector_name=index_data.top_sector_name,
            top_sector_exposure=index_data.top_sector_exposure, top_holding_isin=index_data.top_holding_isin,
            top_holding_exposure=index_data.top_holding_exposure, perf_1m=index_data.perf_1m,
            perf_3m=index_data.perf_3m, perf_6m=index_data.perf_6m, perf_1y=index_data.perf_1y,
            perf_2y=index_data.perf_2y, perf_3y=index_data.perf_3y, perf_5y=index_data.perf_5y,
            perf_inception=index_data.perf_inception, reporting_date=index_data.reporting_date)
    else:
        index_perf = insert(model.IndexPerformance).values(
            index_code=index_data.index_code, standard_deviation=index_data.standard_deviation,
            pe_ratio=index_data.pe_ratio, top_sector_name=index_data.top_sector_name,
            top_sector_exposure=index_data.top_sector_exposure, top_holding_isin=index_data.top_holding_isin,
            top_holding_exposure=index_data.top_holding_exposure, perf_1m=index_data.perf_1m,
            perf_3m=index_data.perf_3m, perf_6m=index_data.perf_6m, perf_1y=index_data.perf_1y,
            perf_2y=index_data.perf_2y, perf_3y=index_data.perf_3y, perf_5y=index_data.perf_5y,
            perf_inception=index_data.perf_inception, reporting_date=index_data.reporting_date)
    iq_engine.execute(index_perf)


def put_mas_securities_mcap(security_isin, market_cap_type_code, market_cap_value):
    mas_sec_query = update(model.MasSecurities).where(model.MasSecurities.security_isin == security_isin).values(
        market_cap_type_code=market_cap_type_code, market_cap_value=market_cap_value)
    iq_engine.execute(mas_sec_query)


def put_sec_fundamental_data(sf_data):
    sf_query = insert(model.SecuritiesFundamentals).values(
        security_id=sf_data['security_id'], security_isin=sf_data['security_isin'], as_on_date=sf_data['as_on_date'],
        market_cap=sf_data['market_cap'], pe_ratio=sf_data['pe_ratio'])
    iq_engine.execute(sf_query)


def put_current_aum(fund_code, current_aum, reporting_date):
    aum_query = update(model.FundPerformance).where(model.FundPerformance.fund_code == fund_code).where(
        model.FundPerformance.effective_end_date == reporting_date).values(current_aum=current_aum)
    iq_engine.execute(aum_query)


def put_no_of_clients(fund_code, no_of_clients, reporting_date):
    no_of_clients_query = update(model.FundPerformance).where(model.FundPerformance.fund_code == fund_code).where(
        model.FundPerformance.effective_end_date == reporting_date).values(no_of_clients=no_of_clients)
    iq_engine.execute(no_of_clients_query)


def put_allocations(fund_code, allocation_values, reporting_date):
    allocation_query = update(model.FundPerformance).where(model.FundPerformance.fund_code == fund_code).where(
        model.FundPerformance.effective_end_date == reporting_date).values(
        portfolio_equity_allocation=round(allocation_values['equity_allocation'], 4),
        portfolio_cash_allocation=allocation_values['cash_allocation'])
    iq_engine.execute(allocation_query)


def put_equity_allocation(allocation_data):
    allocation_query = update(model.FundPerformance).where(
        model.FundPerformance.fund_code == allocation_data.fund_code).where(
        model.FundPerformance.effective_end_date == allocation_data.effective_end_date).values(
        portfolio_equity_allocation=allocation_data.portfolio_equity_allocation)
    iq_engine.execute(allocation_query)


def put_cash_allocation(allocation_data):
    allocation_query = update(model.FundPerformance).where(
        model.FundPerformance.fund_code == allocation_data.fund_code).where(
        model.FundPerformance.effective_end_date == allocation_data.effective_end_date).values(
        portfolio_cash_allocation=allocation_data.portfolio_cash_allocation)
    iq_engine.execute(allocation_query)
