import re
import math
import datetime
import statistics

from scipy import optimize
from pyjarowinkler import distance

from database.db_actions import get_nav_start_date, get_benchmark_index, get_index_price_as_on_date, get_start_price, \
    get_alt_benchmark_index, get_cap_type, get_investment_style, get_fund_nav, get_mcap_for_security, \
    get_security_isin_from_db, get_all_isin, get_sector_from_portfolio, get_collateral_code, get_collateral_view_code, \
    get_fund_short_code, get_default_visibility_code, get_collateral_template_code, get_pe_ratio, get_fund_ratio_mcap, \
    get_all_1m_perf, get_risk_free_rate
from dictionary.portfolio_dictionary import portfolio_dict
from model.FundDetailsExtraction import FundMarketCapExtraction, FundPortfolioExtraction
from model.FundTablesModel import FundBenchmarkNav, FundPerformance, BenchmarkPerformance, \
    AlternateBenchmarkPerformance, FundMarketCap, FundPortfolio, FundSector, FundRatios, Collaterals
from service.DateCalculation import get_effective_start_end_date, get_1m_date, get_3m_date, get_6m_date, get_1y_date, \
    get_2y_date, get_3y_date, get_5y_date


def calc_benchmark_nav(fund_code, reporting_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)
    nav_start_date = get_nav_start_date(fund_code)
    benchmark_index = get_benchmark_index(fund_code)
    index_price = get_index_price_as_on_date(effective_end_date, benchmark_index)
    start_index_price = get_start_price(nav_start_date, benchmark_index)
    benchmark_nav = round((index_price / start_index_price), 6)
    return benchmark_nav


def calc_alt_benchmark_nav(fund_code, reporting_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)
    nav_start_date = get_nav_start_date(fund_code)
    alt_benchmark_index = get_alt_benchmark_index(fund_code)
    alt_index_price = get_index_price_as_on_date(effective_end_date, alt_benchmark_index)
    start_index_price = get_start_price(nav_start_date, alt_benchmark_index)
    alt_benchmark_nav = round((alt_index_price / start_index_price), 6)
    return alt_benchmark_nav


def get_market_cap_type_code(market_cap_values):
    market_cap_type_code = None
    large_exposure = small_exposure = mid_exposure = 0
    if not market_cap_values:
        market_cap_type_code = None
    elif market_cap_values is not None:
        if len(market_cap_values) == 1:
            if market_cap_values.type_market_cap == 'Cash':
                market_cap_type_code = None
        else:
            for obj in market_cap_values:
                if obj.exposure is None:
                    market_cap_values.remove(obj)
            for cap in market_cap_values:
                if cap.type_market_cap == 'Large' or cap.type_market_cap == 'Mega':
                    large_exposure += cap.exposure * 100
                if cap.type_market_cap == 'Small' or cap.type_market_cap == 'Micro':
                    small_exposure += cap.exposure * 100
                if cap.type_market_cap == 'Mid':
                    mid_exposure += cap.exposure * 100
            if large_exposure >= 20 and mid_exposure >= 20 and small_exposure >= 20:
                market_cap_type_code = get_cap_type("Multi Cap")
            elif ((65 > large_exposure >= 25 and 65 > mid_exposure >= 25) or
                  (65 > mid_exposure >= 25 and 65 > small_exposure >= 25) or
                  (65 > small_exposure >= 25 and 65 > large_exposure >= 25)):
                if large_exposure < mid_exposure and large_exposure < small_exposure:
                    market_cap_type_code = get_cap_type("Mid-Small Cap")
                elif mid_exposure < large_exposure and mid_exposure < small_exposure:
                    market_cap_type_code = get_cap_type("Large-Small Cap")
                elif small_exposure < large_exposure and small_exposure < mid_exposure:
                    market_cap_type_code = get_cap_type("Large-Mid Cap")
            else:
                if large_exposure > mid_exposure and large_exposure > small_exposure:
                    market_cap_type_code = get_cap_type("Large Cap")
                elif mid_exposure > large_exposure and mid_exposure > small_exposure:
                    market_cap_type_code = get_cap_type("Mid Cap")
                else:
                    market_cap_type_code = get_cap_type("Small Cap")
    return market_cap_type_code


def get_fund_performance(fund_info, allocation_values, market_cap_values):
    portfolio_equity_allocation = portfolio_cash_allocation = portfolio_asset_allocation = \
        portfolio_other_allocations = None
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())

    current_aum = float(fund_info.get_current_aum()) if not fund_info.get_current_aum() else None
    no_of_clients = int(fund_info.get_no_of_clients()) if fund_info.get_no_of_clients() else None
    mcap_type_code = fund_info.get_market_cap_type_code()
    market_cap_type_code = mcap_type_code if mcap_type_code else get_market_cap_type_code(market_cap_values)

    investment_style = fund_info.get_investment_style()
    investment_style_type_code = investment_style if investment_style else \
        get_investment_style(fund_info.get_fund_code())
    for obj in allocation_values:
        if obj.exposure is None:
            allocation_values.remove(obj)
    for obj in allocation_values:
        if obj.allocation == 'Equity':
            portfolio_equity_allocation = round(float(obj.exposure), 4)
        if obj.allocation == 'Cash & Equivalent':
            portfolio_cash_allocation = round(float(obj.exposure), 4)
        if obj.allocation == 'Asset':
            portfolio_asset_allocation = round(float(obj.exposure), 4)
        if obj.allocation == 'Others':
            portfolio_other_allocations = round(float(obj.exposure), 4)

    prev_1m_end_date = get_1m_date(fund_info.get_reporting_date())
    prev_3m_end_date = get_3m_date(fund_info.get_reporting_date())
    prev_6m_end_date = get_6m_date(fund_info.get_reporting_date())
    prev_1y_end_date = get_1y_date(fund_info.get_reporting_date())
    prev_2y_end_date = get_2y_date(fund_info.get_reporting_date())
    prev_3y_end_date = get_3y_date(fund_info.get_reporting_date())
    prev_5y_end_date = get_5y_date(fund_info.get_reporting_date())
    nav_start_date = get_nav_start_date(fund_info.get_fund_code())

    fund_1m_nav = get_fund_nav(fund_info.get_fund_code(), prev_1m_end_date)
    fund_3m_nav = get_fund_nav(fund_info.get_fund_code(), prev_3m_end_date)
    fund_6m_nav = get_fund_nav(fund_info.get_fund_code(), prev_6m_end_date)
    fund_1y_nav = get_fund_nav(fund_info.get_fund_code(), prev_1y_end_date)
    fund_2y_nav = get_fund_nav(fund_info.get_fund_code(), prev_2y_end_date)
    fund_3y_nav = get_fund_nav(fund_info.get_fund_code(), prev_3y_end_date)
    fund_5y_nav = get_fund_nav(fund_info.get_fund_code(), prev_5y_end_date)

    date_power_1y = effective_end_date - prev_1y_end_date
    date_power_2y = effective_end_date - prev_2y_end_date
    date_power_3y = effective_end_date - prev_3y_end_date
    date_power_5y = effective_end_date - prev_5y_end_date
    date_power_inception = effective_end_date - nav_start_date

    fund_nav = round((float(fund_1m_nav[0][0]) * (1 + fund_info.get_performance_1m())), 4)
    perf_1m = round(((fund_nav / float(fund_1m_nav[0][0])) - 1), 4) if fund_1m_nav else None
    perf_3m = round(((fund_nav / float(fund_3m_nav[0][0])) - 1), 4) if fund_3m_nav else None
    perf_6m = round(((fund_nav / float(fund_6m_nav[0][0])) - 1), 4) if fund_6m_nav else None
    perf_1y = round((((fund_nav / float(fund_1y_nav[0][0])) ** (365 / date_power_1y.days)) - 1), 4) \
        if fund_1y_nav else None
    perf_2y = round((((fund_nav / float(fund_2y_nav[0][0])) ** (365 / date_power_2y.days)) - 1), 4) \
        if fund_2y_nav else None
    perf_3y = round((((fund_nav / float(fund_3y_nav[0][0])) ** (365 / date_power_3y.days)) - 1), 4) \
        if fund_3y_nav else None
    perf_5y = round((((fund_nav / float(fund_5y_nav[0][0])) ** (365 / date_power_5y.days)) - 1), 4) \
        if fund_5y_nav else None

    if date_power_inception.days > 365:
        perf_inception = round((((fund_nav / 1) ** (365 / date_power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((fund_nav / 1) - 1), 4)

    fund_perf_data = FundPerformance()
    fund_perf_data.set_fund_code(fund_info.get_fund_code())
    fund_perf_data.set_current_aum(current_aum)
    fund_perf_data.set_no_of_clients(no_of_clients)
    fund_perf_data.set_market_cap_type_code(market_cap_type_code)
    fund_perf_data.set_investment_style_type_code(investment_style_type_code)
    fund_perf_data.set_portfolio_equity_allocation(portfolio_equity_allocation)
    fund_perf_data.set_portfolio_cash_allocation(portfolio_cash_allocation)
    fund_perf_data.set_portfolio_asset_allocation(portfolio_asset_allocation)
    fund_perf_data.set_portfolio_other_allocations(portfolio_other_allocations)
    fund_perf_data.set_perf_1m(perf_1m)
    fund_perf_data.set_perf_3m(perf_3m)
    fund_perf_data.set_perf_6m(perf_6m)
    fund_perf_data.set_perf_1y(perf_1y)
    fund_perf_data.set_perf_2y(perf_2y)
    fund_perf_data.set_perf_3y(perf_3y)
    fund_perf_data.set_perf_5y(perf_5y)
    fund_perf_data.set_perf_inception(perf_inception)
    fund_perf_data.set_isLatest('1')
    fund_perf_data.set_effective_start_date(effective_start_date)
    fund_perf_data.set_effective_end_date(effective_end_date)
    fund_perf_data.set_created_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    fund_perf_data.set_created_by('ft-automation')
    return fund_perf_data, fund_nav


def get_benchmark_performance(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())
    benchmark_index_code = get_benchmark_index(fund_info.get_fund_code())

    bm_1m_date = get_1m_date(fund_info.get_reporting_date())
    bm_3m_date = get_3m_date(fund_info.get_reporting_date())
    bm_6m_date = get_6m_date(fund_info.get_reporting_date())
    bm_1y_date = get_1y_date(fund_info.get_reporting_date())
    bm_2y_date = get_2y_date(fund_info.get_reporting_date())
    bm_3y_date = get_3y_date(fund_info.get_reporting_date())
    bm_5y_date = get_5y_date(fund_info.get_reporting_date())
    nav_start_date = get_nav_start_date(fund_info.get_fund_code())

    start_index_price = get_start_price(nav_start_date, benchmark_index_code)
    curr_price = get_index_price_as_on_date(effective_end_date, benchmark_index_code)
    bm_1m_price = get_index_price_as_on_date(bm_1m_date, benchmark_index_code)
    bm_3m_price = get_index_price_as_on_date(bm_3m_date, benchmark_index_code)
    bm_6m_price = get_index_price_as_on_date(bm_6m_date, benchmark_index_code)
    bm_1y_price = get_index_price_as_on_date(bm_1y_date, benchmark_index_code)
    bm_2y_price = get_index_price_as_on_date(bm_2y_date, benchmark_index_code)
    bm_3y_price = get_index_price_as_on_date(bm_3y_date, benchmark_index_code)
    bm_5y_price = get_index_price_as_on_date(bm_5y_date, benchmark_index_code)

    bm_date_power_1y = effective_end_date - bm_1y_date
    bm_date_power_2y = effective_end_date - bm_2y_date
    bm_date_power_3y = effective_end_date - bm_3y_date
    bm_date_power_5y = effective_end_date - bm_5y_date
    benchmark_power_inception = effective_end_date - nav_start_date

    benchmark_perf_1m = round(((curr_price / bm_1m_price) - 1), 4) if nav_start_date <= bm_1m_date else None
    benchmark_perf_3m = round(((curr_price / bm_3m_price) - 1), 4) if nav_start_date <= bm_3m_date else None
    benchmark_perf_6m = round(((curr_price / bm_6m_price) - 1), 4) if nav_start_date <= bm_6m_date else None
    benchmark_perf_1y = round((((curr_price / bm_1y_price) ** (365 / bm_date_power_1y.days)) - 1), 4) if \
        nav_start_date <= bm_1y_date else None
    benchmark_perf_2y = round((((curr_price / bm_2y_price) ** (365 / bm_date_power_2y.days)) - 1), 4) if \
        nav_start_date <= bm_2y_date else None
    benchmark_perf_3y = round((((curr_price / bm_3y_price) ** (365 / bm_date_power_3y.days)) - 1), 4) if \
        nav_start_date <= bm_3y_date else None
    benchmark_perf_5y = round((((curr_price / bm_5y_price) ** (365 / bm_date_power_5y.days)) - 1), 4) if \
        nav_start_date <= bm_5y_date else None

    if benchmark_power_inception.days > 365:
        benchmark_perf_inception = round((((curr_price / start_index_price) **
                                           (365 / benchmark_power_inception.days)) - 1), 4)
    else:
        benchmark_perf_inception = round(((curr_price / start_index_price) - 1), 4)

    benchmark_perf_data = BenchmarkPerformance()
    benchmark_perf_data.set_benchmark_index_code(benchmark_index_code)
    benchmark_perf_data.set_benchmark_perf_1m(benchmark_perf_1m)
    benchmark_perf_data.set_benchmark_perf_3m(benchmark_perf_3m)
    benchmark_perf_data.set_benchmark_perf_6m(benchmark_perf_6m)
    benchmark_perf_data.set_benchmark_perf_1y(benchmark_perf_1y)
    benchmark_perf_data.set_benchmark_perf_2y(benchmark_perf_2y)
    benchmark_perf_data.set_benchmark_perf_3y(benchmark_perf_3y)
    benchmark_perf_data.set_benchmark_perf_5y(benchmark_perf_5y)
    benchmark_perf_data.set_benchmark_perf_inception(benchmark_perf_inception)
    return benchmark_perf_data


def get_alt_benchmark_performance(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())
    alt_bm_index_code = get_alt_benchmark_index(fund_info.get_fund_code())

    alt_bm_1m_date = get_1m_date(fund_info.get_reporting_date())
    alt_bm_3m_date = get_3m_date(fund_info.get_reporting_date())
    alt_bm_6m_date = get_6m_date(fund_info.get_reporting_date())
    alt_bm_1y_date = get_1y_date(fund_info.get_reporting_date())
    alt_bm_2y_date = get_2y_date(fund_info.get_reporting_date())
    alt_bm_3y_date = get_3y_date(fund_info.get_reporting_date())
    alt_bm_5y_date = get_5y_date(fund_info.get_reporting_date())
    nav_start_date = get_nav_start_date(fund_info.get_fund_code())

    start_index_price = get_start_price(nav_start_date, alt_bm_index_code)
    curr_price = get_index_price_as_on_date(effective_end_date, alt_bm_index_code)
    alt_bm_1m_price = get_index_price_as_on_date(alt_bm_1m_date, alt_bm_index_code)
    alt_bm_3m_price = get_index_price_as_on_date(alt_bm_3m_date, alt_bm_index_code)
    alt_bm_6m_price = get_index_price_as_on_date(alt_bm_6m_date, alt_bm_index_code)
    alt_bm_1y_price = get_index_price_as_on_date(alt_bm_1y_date, alt_bm_index_code)
    alt_bm_2y_price = get_index_price_as_on_date(alt_bm_2y_date, alt_bm_index_code)
    alt_bm_3y_price = get_index_price_as_on_date(alt_bm_3y_date, alt_bm_index_code)
    alt_bm_5y_price = get_index_price_as_on_date(alt_bm_5y_date, alt_bm_index_code)

    alt_bm_date_power_1y = effective_end_date - alt_bm_1y_date
    alt_bm_date_power_2y = effective_end_date - alt_bm_2y_date
    alt_bm_date_power_3y = effective_end_date - alt_bm_3y_date
    alt_bm_date_power_5y = effective_end_date - alt_bm_5y_date
    alt_benchmark_power_inception = effective_end_date - nav_start_date

    alt_benchmark_perf_1m = round(((curr_price / alt_bm_1m_price) - 1), 4) if nav_start_date <= alt_bm_1m_date else None
    alt_benchmark_perf_3m = round(((curr_price / alt_bm_3m_price) - 1), 4) if nav_start_date <= alt_bm_3m_date else None
    alt_benchmark_perf_6m = round(((curr_price / alt_bm_6m_price) - 1), 4) if nav_start_date <= alt_bm_6m_date else None
    alt_benchmark_perf_1y = round((((curr_price / alt_bm_1y_price) ** (365 / alt_bm_date_power_1y.days)) - 1), 4) if \
        nav_start_date <= alt_bm_1y_date else None
    alt_benchmark_perf_2y = round((((curr_price / alt_bm_2y_price) ** (365 / alt_bm_date_power_2y.days)) - 1), 4) if \
        nav_start_date <= alt_bm_2y_date else None
    alt_benchmark_perf_3y = round((((curr_price / alt_bm_3y_price) ** (365 / alt_bm_date_power_3y.days)) - 1), 4) if \
        nav_start_date <= alt_bm_3y_date else None
    alt_benchmark_perf_5y = round((((curr_price / alt_bm_5y_price) ** (365 / alt_bm_date_power_5y.days)) - 1), 4) if \
        nav_start_date <= alt_bm_5y_date else None

    if alt_benchmark_power_inception.days > 365:
        alt_benchmark_perf_inception = round((((curr_price / start_index_price) **
                                               (365 / alt_benchmark_power_inception.days)) - 1), 4)
    else:
        alt_benchmark_perf_inception = round(((curr_price / start_index_price) - 1), 4)

    alt_benchmark_perf_data = AlternateBenchmarkPerformance()
    alt_benchmark_perf_data.set_alt_benchmark_index_code(alt_bm_index_code)
    alt_benchmark_perf_data.set_alt_benchmark_perf_1m(alt_benchmark_perf_1m)
    alt_benchmark_perf_data.set_alt_benchmark_perf_3m(alt_benchmark_perf_3m)
    alt_benchmark_perf_data.set_alt_benchmark_perf_6m(alt_benchmark_perf_6m)
    alt_benchmark_perf_data.set_alt_benchmark_perf_1y(alt_benchmark_perf_1y)
    alt_benchmark_perf_data.set_alt_benchmark_perf_2y(alt_benchmark_perf_2y)
    alt_benchmark_perf_data.set_alt_benchmark_perf_3y(alt_benchmark_perf_3y)
    alt_benchmark_perf_data.set_alt_benchmark_perf_5y(alt_benchmark_perf_5y)
    alt_benchmark_perf_data.set_alt_benchmark_perf_inception(alt_benchmark_perf_inception)
    return alt_benchmark_perf_data


def get_fund_benchmark_nav(fund_perf_data, fund_nav, benchmark_perf_data, alt_benchmark_perf_data):
    fund_nav_data = FundBenchmarkNav()
    fund_nav_data.set_fund_code(fund_perf_data.get_fund_code())
    fund_nav_data.set_benchmark_index_code(benchmark_perf_data.get_benchmark_index_code())
    fund_nav_data.set_alt_benchmark_index_code(alt_benchmark_perf_data.get_alt_benchmark_index_code())
    fund_nav_data.set_fund_nav(fund_nav)
    fund_nav_data.set_benchmark_nav(calc_benchmark_nav(fund_perf_data.get_fund_code(),
                                                       fund_perf_data.get_effective_end_date()))
    fund_nav_data.set_alt_benchmark_nav(calc_alt_benchmark_nav(fund_perf_data.get_fund_code(),
                                                               fund_perf_data.get_effective_end_date()))
    fund_nav_data.set_effective_end_date(fund_perf_data.get_effective_end_date())
    return fund_nav_data


def get_security_isin(security_name):
    if portfolio_dict.__contains__(security_name):
        stock_name = portfolio_dict[security_name]
    else:
        stock_name = security_name
    isin_details = get_security_isin_from_db(stock_name.replace("'", " "))
    if len(isin_details) == 0:
        stock = stock_name.replace(".", " ").replace("'", " ")
        cleaned_stock_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', stock).lower()
        security_details = get_all_isin()
        max_ratio = 0
        max_index = 0
        for value in range(len(security_details)):
            name = security_details[value][1].replace(".", " ").replace("'", " ")
            cleaned_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', name).lower()
            ratio = distance.get_jaro_distance(cleaned_stock_name, cleaned_name, winkler=True, scaling=0.1)
            if ratio > 0 and max_ratio < ratio:
                max_ratio = ratio
                max_index = value
        security_isin = security_details[max_index]
    else:
        security_isin = isin_details
    print(security_isin)
    return security_isin


def get_market_cap(fund_info, market_cap_values):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())
    for obj in market_cap_values:
        if obj.exposure is None:
            market_cap_values.remove(obj)
    market_cap_data = []
    for value in market_cap_values:
        cap_body = FundMarketCap()
        cap_body.set_fund_code(fund_info.get_fund_code())
        cap_body.set_type_market_cap(value.type_market_cap)
        cap_body.set_exposure(round(float(value.exposure), 4))
        cap_body.set_start_date(effective_start_date)
        cap_body.set_end_date(effective_end_date)
        cap_body.set_created_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cap_body.set_action_by('ft-automation')
        market_cap_data.append(cap_body)
    return market_cap_data


def get_mcap_from_portfolio(fund_info, portfolio_values):
    mcap_values = {}
    mcap_values_from_pf = []
    cap_sum = 0
    for value in portfolio_values:
        security_isin = get_security_isin(value.security_name)
        mcap_type_code = get_mcap_for_security(security_isin).capitalize()
        cap_sum += value.exposure
        if mcap_values.__contains__(mcap_type_code):
            mcap_values[mcap_type_code] += value.exposure
        else:
            mcap_values.update({mcap_type_code: value.exposure})
    for cap, exp in mcap_values.items():
        mcap_body = FundMarketCapExtraction()
        mcap_body.set_type_market_cap(cap)
        mcap_body.set_exposure(exp)
        mcap_values_from_pf.append(mcap_body)
    market_cap_data = get_market_cap(fund_info, mcap_values_from_pf)
    return market_cap_data


def get_fund_portfolio(fund_info, portfolio_values):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())
    portfolio_data = []
    for value in portfolio_values:
        portfolio_body = FundPortfolio()
        portfolio_body.set_fund_code(fund_info.get_fund_code())
        portfolio_body.set_security_isin(get_security_isin(value.security_name))
        exp = round(float(value.exposure), 4)
        exposure = None if exp == 0 else exp
        portfolio_body.set_exposure(exposure)
        portfolio_body.set_start_date(effective_start_date)
        portfolio_body.set_end_date(effective_end_date)
        portfolio_body.set_created_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        portfolio_body.set_action_by('ft-automation')
        portfolio_data.append(portfolio_body)
    return portfolio_data


def get_fund_sector_from_pf(fund_info, portfolio_values):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())
    sector_data = []
    sector_dict = {}
    exposure_sum = 0
    for value in portfolio_values:
        sector = get_sector_from_portfolio(value.security_isin)
        exposure_sum += value.exposure
        if sector_dict.__contains__(sector):
            sector_dict[sector] += value.exposure
        else:
            sector_dict.update({sector: value.exposure})
    for sector, exp in sector_dict.items():
        sector_body = FundSector()
        sector_body.set_fund_code(fund_info.get_fund_code())
        sector_body.set_sector_type_name(sector)
        sector_body.set_exposure(round(exp, 4))
        sector_body.set_start_date(effective_start_date)
        sector_body.set_end_date(effective_end_date)
        sector_body.set_created_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        sector_body.set_action_by('ft-automation')
        sector_data.append(sector_body)
    return sector_data


def get_fund_sector_from_sector(fund_info, sector_values):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())
    sector_data = []
    for value in sector_values:
        sector_body = FundSector()
        sector_body.set_fund_code(fund_info.get_fund_code())
        sector_body.set_sector_type_name(value.sector_name)
        sector_body.set_exposure(round(value.exposure, 4))
        sector_body.set_start_date(effective_start_date)
        sector_body.set_end_date(effective_end_date)
        sector_body.set_created_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        sector_body.set_action_by('ft-automation')
        sector_data.append(sector_body)
    return sector_data


def get_collateral(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())
    fund_short_code = get_fund_short_code(fund_info.get_fund_code())
    collateral_title = fund_short_code + " Fintuple Factsheet"

    collateral_data = Collaterals()
    collateral_data.set_collateral_code(get_collateral_code())
    collateral_data.set_view_code(get_collateral_view_code())
    collateral_data.set_collateral_type_code('FACTSHEET')
    collateral_data.set_entity_type('FUND')
    collateral_data.set_entity_code(fund_info.get_fund_code())
    collateral_data.set_collateral_title(collateral_title)
    collateral_data.set_visibility_code(get_default_visibility_code(fund_info.get_fund_code()))
    collateral_data.set_template_code(get_collateral_template_code(fund_info.get_fund_code(),
                                                                   fund_info.get_reporting_date()))
    collateral_data.set_collateral_date(effective_end_date + datetime.timedelta(days=1))
    collateral_data.set_collateral_status('PUBLISHED')
    collateral_data.set_reporting_date(effective_end_date)
    collateral_data.set_effective_start_date(effective_end_date + datetime.timedelta(days=1))
    collateral_data.set_is_premium(1)
    collateral_data.set_is_published(1)
    collateral_data.set_is_data_changed(1)
    collateral_data.set_published_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    collateral_data.set_created_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    collateral_data.set_created_by('ft-automation')
    return collateral_data


def calc_top5_pe_ratio(top5_holdings):
    pe_ratio_list = get_pe_ratio(top5_holdings)
    pe_ratio_values = [float(pe_ratio['pe_ratio']) for security in top5_holdings for pe_ratio in pe_ratio_list
                       if security.security_isin == pe_ratio['security_isin']]
    exposure_values = [float(security.exposure) for security in top5_holdings]
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        if ratio == 0:
            pe_ratio_values.remove(ratio)
            exposure_values.remove(exp)
    calc_pe_ratio = [float(exp * ratio) for exp, ratio in zip(exposure_values, pe_ratio_values)]
    top5_pe_ratio = round((sum(calc_pe_ratio) / sum(exposure_values)), 4)
    return top5_pe_ratio


def calc_top10_pe_ratio(top10_holdings):
    pe_ratio_list = get_pe_ratio(top10_holdings)
    pe_ratio_values = [float(pe_ratio['pe_ratio']) for security in top10_holdings for pe_ratio in pe_ratio_list
                       if security.security_isin == pe_ratio['security_isin']]
    exposure_values = [float(security.exposure) for security in top10_holdings]
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        if ratio == 0:
            pe_ratio_values.remove(ratio)
            exposure_values.remove(exp)
    calc_pe_ratio = [float(exp * ratio) for exp, ratio in zip(exposure_values, pe_ratio_values)]
    top10_pe_ratio = round((sum(calc_pe_ratio) / sum(exposure_values)), 4)
    return top10_pe_ratio


def calc_top5_market_cap(top5_holdings):
    mcap_list = get_fund_ratio_mcap(top5_holdings)
    mcap_values = [float(market_cap['market_cap']) for security in top5_holdings for market_cap in mcap_list
                   if security.security_isin == market_cap['security_isin']]
    exposure_values = [float(security.exposure) for security in top5_holdings]
    for exp, mcap in zip(exposure_values, mcap_values):
        if mcap == 0:
            mcap_values.remove(mcap)
            exposure_values.remove(exp)
    calc_mcap = [float(exp * mcap) for exp, mcap in zip(exposure_values, mcap_values)]
    top5_market_cap = int(round(sum(calc_mcap) / sum(exposure_values)))
    return top5_market_cap


def calc_top10_market_cap(top10_holdings):
    mcap_list = get_fund_ratio_mcap(top10_holdings)
    mcap_values = [float(market_cap['market_cap']) for security in top10_holdings for market_cap in mcap_list
                   if security.security_isin == market_cap['security_isin']]
    exposure_values = [float(security.exposure) for security in top10_holdings]
    for exp, mcap in zip(exposure_values, mcap_values):
        if mcap == 0:
            mcap_values.remove(mcap)
            exposure_values.remove(exp)
    calc_mcap = [float(exp * mcap) for exp, mcap in zip(exposure_values, mcap_values)]
    top10_market_cap = int(round(sum(calc_mcap) / sum(exposure_values)))
    return top10_market_cap


def get_negative_excess_return(fund_return_list, risk_free):
    negative_excess_return_list = []
    for return_value in fund_return_list:
        if (return_value - risk_free) > 0:
            negative_excess_return_list.append(0)
        else:
            negative_excess_return_list.append((return_value - risk_free) ** 2)
    negative_excess_returns_risk_free = round(sum(negative_excess_return_list), 4)
    return negative_excess_returns_risk_free


def xnpv(rate, annualized_values):
    return sum([av / (1 + rate) ** ((t - annualized_values[0][0]).days / 365.0) for (t, av) in annualized_values])


def get_annualized_return(fund_code, effective_end_date, fund_nav):
    nav_start_date = get_nav_start_date(fund_code)
    start_date_nav = -1
    start_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(str(effective_end_date), "%Y-%m-%d").date()
    annualized_values = [(datetime.date(start_date.year, start_date.month, start_date.day), start_date_nav),
                         (datetime.date(end_date.year, end_date.month, end_date.day), fund_nav)]
    annualized_return = optimize.newton(lambda r: xnpv(r, annualized_values), 0.1)
    return annualized_return


def get_fund_ratios(fund_info, portfolio_values, fund_nav, portfolio_sum, benchmark_perf_1m):
    top5_pe_ratio = top10_pe_ratio = top5_market_cap = top10_market_cap = None
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info.get_reporting_date())
    portfolio_details = []
    for value in portfolio_values:
        pf_isin_body = FundPortfolioExtraction()
        pf_isin_body.set_security_isin(get_security_isin(value.security_name))
        pf_isin_body.set_exposure(value.exposure)
        portfolio_details.append(pf_isin_body)
    if portfolio_sum > 0:
        sorted_exposure = sorted(portfolio_details, key=lambda i: i.exposure, reverse=True)
        sorted_pf_values = [i for i in sorted_exposure if not (i.security_isin == 'CASH')]
        top5_holdings = sorted_pf_values[0:5]
        top10_holdings = sorted_pf_values[0:10]
        pe5_ratio = calc_top5_pe_ratio(top5_holdings)
        top5_pe_ratio = None if (pe5_ratio == 0) else pe5_ratio
        pe10_ratio = calc_top10_pe_ratio(top10_holdings)
        top10_pe_ratio = None if (pe10_ratio == 0) else pe10_ratio
        market5_cap = calc_top5_market_cap(top5_holdings)
        top5_market_cap = None if (market5_cap == 0) else market5_cap
        market10_cap = calc_top10_market_cap(top10_holdings)
        top10_market_cap = None if (market10_cap == 0) else market10_cap
    fund_return_list = get_all_1m_perf(fund_info.get_fund_code())
    fund_return_list.append(fund_info.get_performance_1m())
    standard_deviation = round(statistics.stdev(fund_return_list), 4)
    median = round(statistics.median(fund_return_list), 4)
    risk_free = get_risk_free_rate()
    negative_excess_returns_risk_free = get_negative_excess_return(fund_return_list, risk_free)
    sigma = round(math.sqrt(negative_excess_returns_risk_free / 12), 4)
    annualized_return = get_annualized_return(fund_info.get_fund_code(), effective_end_date, fund_nav)
    sortino_ratio = round(((annualized_return - risk_free) / sigma), 4)
    fund_alpha = round(((float(fund_info.get_performance_1m()) - float(benchmark_perf_1m)) * 100), 4)
    fund_ratio_data = FundRatios()
    fund_ratio_data.set_fund_code(fund_info.get_fund_code())
    fund_ratio_data.set_reporting_date(fund_info.get_reporting_date())
    fund_ratio_data.set_top5_pe_ratio(top5_pe_ratio)
    fund_ratio_data.set_top10_pe_ratio(top10_pe_ratio)
    fund_ratio_data.set_top5_market_cap(top5_market_cap)
    fund_ratio_data.set_top10_market_cap(top10_market_cap)
    fund_ratio_data.set_standard_deviation(standard_deviation)
    fund_ratio_data.set_median(median)
    fund_ratio_data.set_sigma(sigma)
    fund_ratio_data.set_sortino_ratio(sortino_ratio)
    fund_ratio_data.set_negative_excess_returns_risk_free(negative_excess_returns_risk_free)
    fund_ratio_data.set_fund_alpha(fund_alpha)
    fund_ratio_data.set_updated_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    fund_ratio_data.set_updated_by('ft-automation')
    return fund_ratio_data


def table_records(fund_info, allocation_values, market_cap_values, portfolio_values, sector_values):
    portfolio_sum = 0
    for value in portfolio_values:
        if value.exposure:
            portfolio_sum += value.exposure
    portfolio_sum = round(portfolio_sum * 100)
    # Performance details
    fund_perf_data, fund_nav = get_fund_performance(fund_info, allocation_values, market_cap_values)
    benchmark_perf_data = get_benchmark_performance(fund_info)
    alt_benchmark_perf_data = get_alt_benchmark_performance(fund_info)
    fund_nav_data = get_fund_benchmark_nav(fund_perf_data, fund_nav, benchmark_perf_data, alt_benchmark_perf_data)
    # Market Cap details
    if market_cap_values:
        market_cap_data = get_market_cap(fund_info, market_cap_values)
    elif not market_cap_values and portfolio_sum == 100:
        market_cap_data = get_mcap_from_portfolio(fund_info, portfolio_values)
    else:
        market_cap_data = None
    # Portfolio details
    portfolio_data = get_fund_portfolio(fund_info, portfolio_values) if portfolio_values else None
    # Sector details
    if portfolio_sum == 100:
        sector_data = get_fund_sector_from_pf(fund_info, portfolio_data)
    elif portfolio_sum < 100:
        sector_data = get_fund_sector_from_sector(fund_info, sector_values)
    else:
        sector_data = None
    # Ratios details
    fund_ratio_data = get_fund_ratios(fund_info, portfolio_values, fund_nav, portfolio_sum,
                                      benchmark_perf_data.get_benchmark_perf_1m())
    # Collateral details
    collateral_data = get_collateral(fund_info)
    fund_data = {'nav': fund_nav_data, 'fund_perf': fund_perf_data, 'benchmark_perf': benchmark_perf_data,
                 'alt_benchmark_perf': alt_benchmark_perf_data, 'market_cap': market_cap_data,
                 'portfolio': portfolio_data, 'sector': sector_data, 'ratios': fund_ratio_data,
                 'collaterals': collateral_data}
    return fund_data
