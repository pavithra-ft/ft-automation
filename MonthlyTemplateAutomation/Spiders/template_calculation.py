import calendar
import datetime
import re
import math
import statistics

from scipy import optimize
from pyjarowinkler import distance
from Spiders.sector_dictionary import sector_dictionary
from Spiders.portfolio_dictionary import portfolio_dict
from dateutil.relativedelta import relativedelta
from Spiders.db_actions import get_benchmark_index, get_alt_benchmark_index, get_benchmark_nav, get_alt_benchmark_nav, \
    update_islatest, get_cap_type, get_nav_start_date, get_isin_sector, get_all_isin, get_sector_from_industry, \
    get_sector_from_portfolio, get_sectorcash_from_portfolio, get_fund_short_code, get_collateral_code, \
    get_collateral_view_code, get_collateral_template_code, collaterals_check, put_collateral_data, get_pe_ratio, \
    get_fund_ratio_mcap, get_risk_free_rate, get_all_fund_return, put_market_cap_data, put_fund_sector, \
    put_fund_portfolio, get_start_price, get_index_price_as_on_date, get_fund_nav, put_fund_ratio_data


def get_effective_start_end_date(fund_info):
    # Calculation of effective start date and end date
    start_date = datetime.datetime.strptime(fund_info['reporting_date'], '%Y-%m-%d %H:%M:%S').date()
    effective_start_date = start_date.replace(day=1)
    effective_end_date = start_date.replace(
        day=calendar.monthrange(effective_start_date.year, effective_start_date.month)[1])
    return effective_start_date, effective_end_date


def get_1m_date(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    previous_1m_date = effective_end_date - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1])
    return previous_1m_end_date


def get_3m_date(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    previous_3m_date = effective_end_date - relativedelta(months=3)
    previous_3m_end_date = previous_3m_date.replace(day=calendar.monthrange(previous_3m_date.year,
                                                                            previous_3m_date.month)[1])
    return previous_3m_end_date


def get_6m_date(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    previous_6m_date = effective_end_date - relativedelta(months=6)
    previous_6m_end_date = previous_6m_date.replace(day=calendar.monthrange(previous_6m_date.year,
                                                                            previous_6m_date.month)[1])
    return previous_6m_end_date


def get_1y_date(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    previous_1y_date = effective_end_date - relativedelta(years=1)
    previous_1y_end_date = (previous_1y_date.replace(day=calendar.monthrange(previous_1y_date.year,
                                                                             previous_1y_date.month)[1]))
    return previous_1y_end_date


def get_2y_date(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    previous_2y_date = effective_end_date - relativedelta(years=2)
    previous_2y_end_date = previous_2y_date.replace(day=calendar.monthrange(previous_2y_date.year,
                                                                            previous_2y_date.month)[1])
    return previous_2y_end_date


def get_3y_date(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    previous_3y_date = effective_end_date - relativedelta(years=3)
    previous_3y_end_date = previous_3y_date.replace(day=calendar.monthrange(previous_3y_date.year,
                                                                            previous_3y_date.month)[1])
    return previous_3y_end_date


def get_5y_date(fund_info):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    previous_5y_date = effective_end_date - relativedelta(years=5)
    previous_5y_end_date = previous_5y_date.replace(day=calendar.monthrange(previous_5y_date.year,
                                                                            previous_5y_date.month)[1])
    return previous_5y_end_date


def calc_benchmark_nav(fund_info, iq_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    previous_1m_date = get_1m_date(fund_info)
    benchmark_index = get_benchmark_index(fund_info, iq_database)
    index_price = get_index_price_as_on_date(effective_end_date, benchmark_index, iq_database)
    prev_index_price = get_index_price_as_on_date(previous_1m_date, benchmark_index, iq_database)
    if len(prev_index_price) == 0:
        previous_index_price = None
    else:
        previous_index_price = prev_index_price[0][0]
    previous_benchmark_nav = get_benchmark_nav(fund_info, previous_1m_date, iq_database)
    benchmark_return = (index_price[0][0] / previous_index_price) - 1
    benchmark_nav = round((previous_benchmark_nav * (1 + benchmark_return)), 6)
    return benchmark_nav


def calc_alt_benchmark_nav(fund_info, iq_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    alt_previous_1m_date = get_1m_date(fund_info)
    alt_benchmark_index = get_alt_benchmark_index(fund_info, iq_database)
    alt_index_price = get_index_price_as_on_date(effective_end_date, alt_benchmark_index, iq_database)
    alt_prev_index_price = get_index_price_as_on_date(alt_previous_1m_date, alt_benchmark_index, iq_database)
    if len(alt_prev_index_price) == 0:
        alt_previous_index_price = None
    else:
        alt_previous_index_price = alt_prev_index_price[0][0]
    alt_benchmark_previous_nav = get_alt_benchmark_nav(fund_info, alt_previous_1m_date, iq_database)
    alt_benchmark_return = (alt_index_price[0][0] / alt_previous_index_price) - 1
    alt_benchmark_nav = round((alt_benchmark_previous_nav * (1 + alt_benchmark_return)), 6)
    return alt_benchmark_nav


def get_market_cap_type_code(market_cap_values, iq_database):
    global market_cap_type_code
    mcap_check = not market_cap_values
    if mcap_check is True:
        market_cap_type_code = None
    elif mcap_check is False:
        if len(market_cap_values) == 1:
            if market_cap_values.__contains__('Cash'):
                del market_cap_values['Cash']
            market_cap_type_code = None
        else:
            for key in market_cap_values:
                market_cap_values[key] *= 100
            mega_value = market_cap_values['Mega'] if 'Mega' in market_cap_values.keys() else 0
            large_value = market_cap_values['Large'] if 'Large' in market_cap_values.keys() else 0
            small_value = market_cap_values['Small'] if 'Small' in market_cap_values.keys() else 0
            micro_value = market_cap_values['Micro'] if 'Micro' in market_cap_values.keys() else 0
            market_cap_values.update({"Large": mega_value + large_value})
            market_cap_values.update({"Small": small_value + micro_value})
            keys_to_remove = ["Cash", "Micro", "Mega", "ETF"]
            for key in keys_to_remove:
                if key in market_cap_values.keys():
                    del market_cap_values[key]
            large_exposure = market_cap_values['Large'] if 'Large' in market_cap_values.keys() else 0
            small_exposure = market_cap_values['Small'] if 'Small' in market_cap_values.keys() else 0
            mid_exposure = market_cap_values['Mid'] if 'Mid' in market_cap_values.keys() else 0
            if large_exposure >= 20 and mid_exposure >= 20 and small_exposure >= 20:
                market_cap_type_code = get_cap_type("Multi Cap", iq_database)
            elif ((65 > large_exposure >= 25 and 65 > mid_exposure >= 25) or
                  (65 > mid_exposure >= 25 and 65 > small_exposure >= 25) or
                  (65 > small_exposure >= 25 and 65 > large_exposure >= 25)):
                if large_exposure < mid_exposure and large_exposure < small_exposure:
                    market_cap_type_code = get_cap_type("Mid-Small Cap", iq_database)
                elif mid_exposure < large_exposure and mid_exposure < small_exposure:
                    market_cap_type_code = get_cap_type("Large-Small Cap", iq_database)
                elif small_exposure < large_exposure and small_exposure < mid_exposure:
                    market_cap_type_code = get_cap_type("Large-Mid Cap", iq_database)
            else:
                if large_exposure > mid_exposure and large_exposure > small_exposure:
                    market_cap_type_code = get_cap_type("Large Cap", iq_database)
                elif mid_exposure > large_exposure and mid_exposure > small_exposure:
                    market_cap_type_code = get_cap_type("Mid Cap", iq_database)
                else:
                    market_cap_type_code = get_cap_type("Small Cap", iq_database)
    return market_cap_type_code


def get_fund_performance(fund_info, allocation_values, market_cap_values, iq_database, app_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    current_aum = float(fund_info['current_aum']) if fund_info['current_aum'] else None
    no_of_clients = int(fund_info['no_of_clients']) if fund_info['no_of_clients'] else None
    # Calculation of Market cap type code
    mcap_type_code = fund_info['market_cap_type_code']
    if mcap_type_code:
        market_cap_type_code = fund_info['market_cap_type_code']
    else:
        market_cap_type_code = get_market_cap_type_code(market_cap_values, iq_database)
    # Calculation of Fund allocations
    portfolio_equity_allocation = round(float(allocation_values['Equity']), 4) if allocation_values['Equity'] else None
    portfolio_cash_allocation = round(float(allocation_values['Cash & Equivalent']), 4) if \
        allocation_values['Cash & Equivalent'] else None
    portfolio_asset_allocation = round(float(allocation_values['Asset']), 4) if allocation_values['Asset'] else None
    portfolio_other_allocations = round(float(allocation_values['Others']), 4) if allocation_values['Others'] else None
    # Calculation of Fund NAV
    prev_1m_end_date = get_1m_date(fund_info)
    prev_3m_end_date = get_3m_date(fund_info)
    prev_6m_end_date = get_6m_date(fund_info)
    prev_1y_end_date = get_1y_date(fund_info)
    prev_2y_end_date = get_2y_date(fund_info)
    prev_3y_end_date = get_3y_date(fund_info)
    prev_5y_end_date = get_5y_date(fund_info)
    perf_1m = None
    perf_3m = None
    perf_6m = None
    perf_1y = None
    perf_2y = None
    perf_3y = None
    perf_5y = None
    fund_1m_nav = get_fund_nav(fund_info, prev_1m_end_date, iq_database)
    # Calculation of Fund nav
    fund_nav = round((fund_1m_nav[0][0] * (1 + fund_info["performance_1m"])), 4)
    # Calculation of 1 month Fund performance
    if fund_1m_nav:
        perf_1m = round(((fund_nav / fund_1m_nav[0][0]) - 1), 4)
    # Calculation of 3 months Fund performance
    fund_3m_nav = get_fund_nav(fund_info, prev_3m_end_date, iq_database)
    if fund_3m_nav:
        perf_3m = round(((fund_nav / fund_3m_nav[0][0]) - 1), 4)
    # Calculation of 6 months Fund performance
    fund_6m_nav = get_fund_nav(fund_info, prev_6m_end_date, iq_database)
    if fund_6m_nav:
        perf_6m = round(((fund_nav / fund_6m_nav[0][0]) - 1), 4)
    # Calculation of 1 year Fund performance
    fund_1y_nav = get_fund_nav(fund_info, prev_1y_end_date, iq_database)
    if fund_1y_nav:
        date_power_1y = effective_end_date - prev_1y_end_date
        perf_1y = round((((fund_nav / fund_1y_nav[0][0]) ** (365 / date_power_1y.days)) - 1), 4)
    # Calculation of 2 years Fund performance
    fund_2y_nav = get_fund_nav(fund_info, prev_2y_end_date, iq_database)
    if fund_2y_nav:
        date_power_2y = effective_end_date - prev_2y_end_date
        perf_2y = round((((fund_nav / fund_2y_nav[0][0]) ** (365 / date_power_2y.days)) - 1), 4)
    # Calculation of 3 years Fund performance
    fund_3y_nav = get_fund_nav(fund_info, prev_3y_end_date, iq_database)
    if fund_3y_nav:
        date_power_3y = effective_end_date - prev_3y_end_date
        perf_3y = round((((fund_nav / fund_3y_nav[0][0]) ** (365 / date_power_3y.days)) - 1), 4)
    # Calculation of 5 years Fund performance
    fund_5y_nav = get_fund_nav(fund_info, prev_5y_end_date, iq_database)
    if fund_5y_nav:
        date_power_5y = effective_end_date - prev_5y_end_date
        perf_5y = round((((fund_nav / fund_5y_nav[0][0]) ** (365 / date_power_5y.days)) - 1), 4)
    # Calculation of Fund performance inception
    nav_start_date = get_nav_start_date(fund_info, app_database)
    date_power_inception = effective_end_date - nav_start_date
    perf_inception = round((((fund_nav / 1) ** (365 / date_power_inception.days)) - 1), 4)
    # Other fields
    isLatest = '1'
    created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = "ft-automation"
    fund_code = fund_info["fund_code"]
    fundperfData = {"fund_code": fund_code, "current_aum": current_aum, "no_of_clients": no_of_clients,
                    "market_cap_type_code": market_cap_type_code,
                    "portfolio_equity_allocation": portfolio_equity_allocation,
                    "portfolio_cash_allocation": portfolio_cash_allocation,
                    "portfolio_asset_allocation": portfolio_asset_allocation,
                    "portfolio_other_allocations": portfolio_other_allocations, "perf_1m": perf_1m, "perf_3m": perf_3m,
                    "perf_6m": perf_6m, "perf_1y": perf_1y, "perf_2y": perf_2y, "perf_3y": perf_3y, "perf_5y": perf_5y,
                    "perf_inception": perf_inception, "isLatest": isLatest,
                    "effective_start_date": effective_start_date, "effective_end_date": effective_end_date,
                    "created_ts": created_ts, "created_by": created_by}
    return fundperfData, fund_nav


def get_benchmark_performance(fund_info, iq_database, app_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    benchmark_index_code = get_benchmark_index(fund_info, iq_database)
    nav_start_date = get_nav_start_date(fund_info, app_database)
    start_index_price = get_start_price(nav_start_date, benchmark_index_code, iq_database)
    curr_price = get_index_price_as_on_date(effective_end_date, benchmark_index_code, iq_database)
    benchmark_1m_date = get_1m_date(fund_info)
    benchmark_3m_date = get_3m_date(fund_info)
    benchmark_6m_date = get_6m_date(fund_info)
    benchmark_1y_date = get_1y_date(fund_info)
    benchmark_2y_date = get_2y_date(fund_info)
    benchmark_3y_date = get_3y_date(fund_info)
    benchmark_5y_date = get_5y_date(fund_info)
    benchmark_perf_1m = None
    benchmark_perf_3m = None
    benchmark_perf_6m = None
    benchmark_perf_1y = None
    benchmark_perf_2y = None
    benchmark_perf_3y = None
    benchmark_perf_5y = None
    # Calculation of 1 month Benchmark performance
    if nav_start_date <= benchmark_1m_date:
        benchmark_1m_price = get_index_price_as_on_date(benchmark_1m_date, benchmark_index_code, iq_database)
        benchmark_perf_1m = round(((curr_price[0][0] / benchmark_1m_price[0][0]) - 1), 4)
    # Calculation of 3 months Benchmark performance
    if nav_start_date <= benchmark_3m_date:
        benchmark_3m_price = get_index_price_as_on_date(benchmark_3m_date, benchmark_index_code, iq_database)
        benchmark_perf_3m = round(((curr_price[0][0] / benchmark_3m_price[0][0]) - 1), 4)
    # Calculation of 6 months Benchmark performance
    if nav_start_date <= benchmark_6m_date:
        benchmark_6m_price = get_index_price_as_on_date(benchmark_6m_date, benchmark_index_code, iq_database)
        benchmark_perf_6m = round(((curr_price[0][0] / benchmark_6m_price[0][0]) - 1), 4)
    # Calculation of 1 year Benchmark performance
    if nav_start_date <= benchmark_1y_date:
        benchmark_1y_price = get_index_price_as_on_date(benchmark_1y_date, benchmark_index_code, iq_database)
        bm_date_power_1y = effective_end_date - benchmark_1y_date
        benchmark_perf_1y = round((((curr_price[0][0] / benchmark_1y_price[0][0]) **
                                    (365 / bm_date_power_1y.days)) - 1), 4)
    # Calculation of 2 years Benchmark performance
    if nav_start_date <= benchmark_2y_date:
        benchmark_2y_price = get_index_price_as_on_date(benchmark_2y_date, benchmark_index_code, iq_database)
        bm_date_power_2y = effective_end_date - benchmark_2y_date
        benchmark_perf_2y = round((((curr_price[0][0] / benchmark_2y_price[0][0]) **
                                    (365 / bm_date_power_2y.days)) - 1), 4)
    # Calculation of 3 years Benchmark performance
    if nav_start_date <= benchmark_3y_date:
        benchmark_3y_price = get_index_price_as_on_date(benchmark_3y_date, benchmark_index_code, iq_database)
        bm_date_power_3y = effective_end_date - benchmark_3y_date
        benchmark_perf_3y = round((((curr_price[0][0] / benchmark_3y_price[0][0]) **
                                    (365 / bm_date_power_3y.days)) - 1), 4)
    # Calculation of 5 years Benchmark performance
    if nav_start_date <= benchmark_5y_date:
        benchmark_5y_price = get_index_price_as_on_date(benchmark_5y_date, benchmark_index_code, iq_database)
        bm_date_power_5y = effective_end_date - benchmark_5y_date
        benchmark_perf_5y = round((((curr_price[0][0] / benchmark_5y_price[0][0]) **
                                    (365 / bm_date_power_5y.days)) - 1), 4)
    # Calculation of Benchmark performance inception
    benchmark_power_inception = effective_end_date - nav_start_date
    benchmark_perf_inception = round((((curr_price[0][0] / start_index_price) **
                                       (365 / benchmark_power_inception.days)) - 1), 4)
    benchmark_perf_data = {"index_code": benchmark_index_code, "benchmark_perf_1m": benchmark_perf_1m,
                           "benchmark_perf_3m": benchmark_perf_3m, "benchmark_perf_6m": benchmark_perf_6m,
                           "benchmark_perf_1y": benchmark_perf_1y, "benchmark_perf_2y": benchmark_perf_2y,
                           "benchmark_perf_3y": benchmark_perf_3y, "benchmark_perf_5y": benchmark_perf_5y,
                           "benchmark_perf_inception": benchmark_perf_inception}
    return benchmark_perf_data


def get_alt_benchmark_performance(fund_info, iq_database, app_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    alt_benchmark_index_code = get_alt_benchmark_index(fund_info, iq_database)
    nav_start_date = get_nav_start_date(fund_info, app_database)
    start_index_price = get_start_price(nav_start_date, alt_benchmark_index_code, iq_database)
    curr_price = get_index_price_as_on_date(effective_end_date, alt_benchmark_index_code, iq_database)
    alt_benchmark_1m_date = get_1m_date(fund_info)
    alt_benchmark_3m_date = get_3m_date(fund_info)
    alt_benchmark_6m_date = get_6m_date(fund_info)
    alt_benchmark_1y_date = get_1y_date(fund_info)
    alt_benchmark_2y_date = get_2y_date(fund_info)
    alt_benchmark_3y_date = get_3y_date(fund_info)
    alt_benchmark_5y_date = get_5y_date(fund_info)
    alt_benchmark_perf_1m = None
    alt_benchmark_perf_3m = None
    alt_benchmark_perf_6m = None
    alt_benchmark_perf_1y = None
    alt_benchmark_perf_2y = None
    alt_benchmark_perf_3y = None
    alt_benchmark_perf_5y = None
    # Calculation of 1 month alt_benchmark performance
    if nav_start_date <= alt_benchmark_1m_date:
        alt_benchmark_1m_price = get_index_price_as_on_date(alt_benchmark_1m_date, alt_benchmark_index_code,
                                                            iq_database)
        alt_benchmark_perf_1m = round(((curr_price[0][0] / alt_benchmark_1m_price[0][0]) - 1), 4)
    # Calculation of 3 months alt_benchmark performance
    if nav_start_date <= alt_benchmark_3m_date:
        alt_benchmark_3m_price = get_index_price_as_on_date(alt_benchmark_3m_date, alt_benchmark_index_code,
                                                            iq_database)
        alt_benchmark_perf_3m = round(((curr_price[0][0] / alt_benchmark_3m_price[0][0]) - 1), 4)
    # Calculation of 6 months alt_benchmark performance
    if nav_start_date <= alt_benchmark_6m_date:
        alt_benchmark_6m_price = get_index_price_as_on_date(alt_benchmark_6m_date, alt_benchmark_index_code,
                                                            iq_database)
        alt_benchmark_perf_6m = round(((curr_price[0][0] / alt_benchmark_6m_price[0][0]) - 1), 4)
    # Calculation of 1 year alt_benchmark performance
    if nav_start_date <= alt_benchmark_1y_date:
        alt_benchmark_1y_price = get_index_price_as_on_date(alt_benchmark_1y_date, alt_benchmark_index_code,
                                                            iq_database)
        alt_bm_date_power_1y = effective_end_date - alt_benchmark_1y_date
        alt_benchmark_perf_1y = round((((curr_price[0][0] / alt_benchmark_1y_price[0][0]) **
                                        (365 / alt_bm_date_power_1y.days)) - 1), 4)
    # Calculation of 2 years alt_benchmark performance
    if nav_start_date <= alt_benchmark_2y_date:
        alt_benchmark_2y_price = get_index_price_as_on_date(alt_benchmark_2y_date, alt_benchmark_index_code,
                                                            iq_database)
        alt_bm_date_power_2y = effective_end_date - alt_benchmark_2y_date
        alt_benchmark_perf_2y = round((((curr_price[0][0] / alt_benchmark_2y_price[0][0]) **
                                        (365 / alt_bm_date_power_2y.days)) - 1), 4)
    # Calculation of 3 years alt_benchmark performance
    if nav_start_date <= alt_benchmark_3y_date:
        alt_benchmark_3y_price = get_index_price_as_on_date(alt_benchmark_3y_date, alt_benchmark_index_code,
                                                            iq_database)
        alt_bm_date_power_3y = effective_end_date - alt_benchmark_3y_date
        alt_benchmark_perf_3y = round((((curr_price[0][0] / alt_benchmark_3y_price[0][0]) **
                                        (365 / alt_bm_date_power_3y.days)) - 1), 4)
    # Calculation of 5 years alt_benchmark performance
    if nav_start_date <= alt_benchmark_5y_date:
        alt_benchmark_5y_price = get_index_price_as_on_date(alt_benchmark_5y_date, alt_benchmark_index_code,
                                                            iq_database)
        alt_bm_date_power_5y = effective_end_date - alt_benchmark_5y_date
        alt_benchmark_perf_5y = round((((curr_price[0][0] / alt_benchmark_5y_price[0][0]) **
                                        (365 / alt_bm_date_power_5y.days)) - 1), 4)
    # Calculation of alt_benchmark performance inception
    alt_benchmark_power_inception = effective_end_date - nav_start_date
    alt_benchmark_perf_inception = round((((curr_price[0][0] / start_index_price) **
                                           (365 / alt_benchmark_power_inception.days)) - 1), 4)
    alt_benchmark_perf_data = {"index_code": alt_benchmark_index_code, "alt_benchmark_perf_1m": alt_benchmark_perf_1m,
                               "alt_benchmark_perf_3m": alt_benchmark_perf_3m,
                               "alt_benchmark_perf_6m": alt_benchmark_perf_6m,
                               "alt_benchmark_perf_1y": alt_benchmark_perf_1y,
                               "alt_benchmark_perf_2y": alt_benchmark_perf_2y,
                               "alt_benchmark_perf_3y": alt_benchmark_perf_3y,
                               "alt_benchmark_perf_5y": alt_benchmark_perf_5y,
                               "alt_benchmark_perf_inception": alt_benchmark_perf_inception}
    return alt_benchmark_perf_data


def get_market_cap(fund_info, market_cap_values):
    created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = "ft-automation"
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    capData = []
    for type_market_cap, exposure in market_cap_values.items():
        cap_body = {}
        cap_body.update({"fund_code": fund_info["fund_code"]})
        cap_body.update({"type_market_cap": type_market_cap})
        exposure_calc = round(float(exposure), 4)
        if exposure_calc != 0:
            cap_body.update({"exposure": exposure_calc})
        else:
            cap_body.update({"exposure": None})
        cap_body.update({"start_date": effective_start_date})
        cap_body.update({"end_date": effective_end_date})
        cap_body.update({"created_ts": created_ts})
        cap_body.update({"action_by": created_by})
        capData.append(cap_body)
    return capData


def get_isin(security_name, iq_database):
    global security_isin, sec_name
    if portfolio_dict.__contains__(security_name):
        sec_name = portfolio_dict[security_name]
    else:
        sec_name = security_name
    isin_details = get_isin_sector(sec_name.replace("'", " "), iq_database)
    if len(isin_details) == 0:
        sec_name = sec_name.replace(".", " ").replace("'", " ")
        cleaned_sec_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', sec_name).lower()
        security_details = get_all_isin(iq_database)
        max_ratio = 0
        max_index = 0
        for value in range(len(security_details)):
            name = security_details[value][1].replace(".", " ").replace("'", " ")
            cleaned_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', name).lower()
            ratio = distance.get_jaro_distance(cleaned_sec_name, cleaned_name, winkler=True, scaling=0.1)
            if ratio > 0 and max_ratio < ratio:
                max_ratio = ratio
                max_index = value
        security_isin = security_details[max_index][0]
    else:
        security_isin = isin_details[0][0]
    print(security_isin)
    return security_isin


def get_fund_portfolio(fund_info, portfolio_values, iq_database):
    created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = "ft-automation"
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    portfolio_data = []
    for value in portfolio_values:
        portfolio_body = {}
        portfolio_body.update({"fund_code": fund_info["fund_code"]})
        portfolio_body.update({"security_isin": get_isin(value['security_name'], iq_database)})
        exp = round(float(value['exposure']), 4)
        if exp == 0:
            exposure = None
        else:
            exposure = exp
        portfolio_body.update({"exposure": exposure})
        portfolio_body.update({"start_date": effective_start_date})
        portfolio_body.update({"end_date": effective_end_date})
        portfolio_body.update({"created_ts": created_ts})
        portfolio_body.update({"action_by": created_by})
        portfolio_data.append(portfolio_body)
    return portfolio_data


def get_security_list(portfolio_values, iq_database):
    security_isin_list = []
    for value in portfolio_values:
        security_name = value['security_name']
        security_isin = get_isin(security_name, iq_database)
        exposure = float(value['exposure'])
        security_isin_list.append(
            {"security_name": security_name, "security_isin": security_isin, "exposure": exposure})
    return security_isin_list


def get_fund_sector_from_portfolio(portfolio_values, iq_database):
    global sec_isin, sector_response
    sector_breakdown = []
    securityList = get_security_list(portfolio_values, iq_database)
    for securityData in securityList:
        sector_body = {"security": securityData["security_name"], "isin": securityData["security_isin"],
                       "sector": None, "exposure": securityData["exposure"]}
        if securityData["security_isin"] != "CASH":
            sec_isin = securityData["security_isin"]
            sector_response = get_sector_from_portfolio(sec_isin, iq_database)
        elif securityData["security_isin"] == 'CASH':
            sec_isin = securityData["security_isin"]
            sector_response = get_sectorcash_from_portfolio(sec_isin, iq_database)
        sector_body["sector"] = sector_response[0][0]
        sector_breakdown.append(sector_body)
    sector_breakdown_result = {}
    sector_sum = 0
    for i in sector_breakdown:
        sector_sum += i['exposure']
        if sector_breakdown_result.__contains__(i["sector"]):
            sector_breakdown_result[i["sector"]] += i["exposure"]
        else:
            sector_breakdown_result.update({i["sector"]: i["exposure"]})
    for sec, exp in sector_breakdown_result.items():
        if exp == 0:
            sector_breakdown_result[sec] = None
        else:
            sector_breakdown_result[sec] = round(exp, 4)
    return sector_breakdown_result


def get_fund_sector(sector_values, iq_database):
    sector_dict = {}
    for sector_data in sector_values:
        sector_data = dict(sector_data)
        sector_details = get_sector_from_industry(sector_data['sector_name'], iq_database)
        if len(sector_details) > 0:
            sector_name = sector_details[0][0]
            if sector_details[0][0] in sector_dict:
                if sector_name in sector_dict.keys():
                    sector_data['exposure'] += sector_dict[sector_name]
                    sector_dict.update({sector_details[0][0]: round(sector_data['exposure'], 4)})
                else:
                    sector_dict.update({sector_details[0][0]: round(sector_data['exposure'], 4)})
            else:
                sector_dict.update({sector_details[0][0]: round(sector_data['exposure'], 4)})
        else:
            industry = sector_data['sector_name']
            if sector_dictionary.__contains__(industry):
                sector_name = sector_dictionary[industry]
                if sector_name in sector_dict.keys():
                    sector_data['exposure'] += sector_dict[sector_name]
                    sector_dict.update({sector_dictionary[industry]: round(sector_data['exposure'], 4)})
                else:
                    sector_dict.update({sector_dictionary[industry]: round(sector_data['exposure'], 4)})
    return sector_dict


def get_collateral(fund_info, fs_database, app_database):
    eff_start_date, eff_end_date = get_effective_start_end_date(fund_info)
    collateral_code = get_collateral_code(fs_database)
    view_code = get_collateral_view_code(fs_database)
    collateral_type_code = "FACTSHEET"
    entity_type = "FUND"
    entity_code = fund_info['fund_code']
    fund_short_code = get_fund_short_code(fund_info, app_database)
    collateral_title = fund_short_code + " Fintuple Factsheet"
    visibility_code = "PUBLIC"
    template_code = get_collateral_template_code(fund_info, fs_database)
    collateral_date = eff_end_date + datetime.timedelta(days=1)
    collateral_status = "PUBLISHED"
    reporting_date = eff_end_date
    effective_start_date = collateral_date
    is_premium = 1
    is_published = 1
    is_data_changed = 1
    published_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = "ft-automation"
    collateral_data = {"collateral_code": collateral_code, "view_code": view_code,
                       "collateral_type_code": collateral_type_code, "entity_type": entity_type,
                       "entity_code": entity_code, "collateral_title": collateral_title,
                       "visibility_code": visibility_code, "template_code": template_code,
                       "collateral_date": collateral_date, "collateral_status": collateral_status,
                       "reporting_date": reporting_date, "effective_start_date": effective_start_date,
                       "is_premium": is_premium, "is_published": is_published, "is_data_changed": is_data_changed,
                       "published_ts": published_ts, "created_ts": created_ts, "created_by": created_by}
    return collateral_data


def calc_top5_pe_ratio(top5_holdings, iq_database):
    security_isin_list = get_security_list(top5_holdings, iq_database)
    pe_ratio_list = get_pe_ratio(security_isin_list, iq_database)
    pe_ratio_values = []
    exposure_values = []
    for security in security_isin_list:
        for pe_ratio in pe_ratio_list:
            if security['security_isin'] == pe_ratio['security_isin']:
                pe_ratio_values.append(pe_ratio['pe_ratio'])
    for exposure in security_isin_list:
        exposure_values.append(exposure['exposure'])
    calc_pe_ratio = []
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        if ratio == 0:
            pe_ratio_values.remove(ratio)
            exposure_values.remove(exp)
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        calc_pe_ratio.append(exp * ratio)
    top5_pe_ratio = round((sum(calc_pe_ratio) / sum(exposure_values)), 4)
    return top5_pe_ratio


def calc_top10_pe_ratio(top10_holdings, iq_database):
    security_isin_list = get_security_list(top10_holdings, iq_database)
    pe_ratio_list = get_pe_ratio(security_isin_list, iq_database)
    pe_ratio_values = []
    exposure_values = []
    for security in security_isin_list:
        for pe_ratio in pe_ratio_list:
            if security['security_isin'] == pe_ratio['security_isin']:
                pe_ratio_values.append(pe_ratio['pe_ratio'])
    for exposure in security_isin_list:
        exposure_values.append(exposure['exposure'])
    calc_pe_ratio = []
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        if ratio == 0:
            pe_ratio_values.remove(ratio)
            exposure_values.remove(exp)
    for exp, ratio in zip(exposure_values, pe_ratio_values):
        calc_pe_ratio.append(exp * ratio)
    top10_pe_ratio = round((sum(calc_pe_ratio) / sum(exposure_values)), 4)
    return top10_pe_ratio


def calc_top5_market_cap(top5_holdings, iq_database):
    security_isin_list = get_security_list(top5_holdings, iq_database)
    mcap_list = get_fund_ratio_mcap(security_isin_list, iq_database)
    mcap_values = []
    exposure_values = []
    for security in security_isin_list:
        for market_cap in mcap_list:
            if security['security_isin'] == market_cap['security_isin']:
                mcap_values.append(market_cap['market_cap'])
    for exposure in security_isin_list:
        exposure_values.append(exposure['exposure'])
    calc_mcap = []
    for exp, mcap in zip(exposure_values, mcap_values):
        if mcap == 0:
            mcap_values.remove(mcap)
            exposure_values.remove(exp)
    for exp, mcap in zip(exposure_values, mcap_values):
        calc_mcap.append(exp * mcap)
    top5_market_cap = int(round(sum(calc_mcap) / sum(exposure_values)))
    return top5_market_cap


def calc_top10_market_cap(top10_holdings, iq_database):
    security_isin_list = get_security_list(top10_holdings, iq_database)
    mcap_list = get_fund_ratio_mcap(security_isin_list, iq_database)
    mcap_values = []
    exposure_values = []
    for security in security_isin_list:
        for market_cap in mcap_list:
            if security['security_isin'] == market_cap['security_isin']:
                mcap_values.append(market_cap['market_cap'])
    for exposure in security_isin_list:
        exposure_values.append(exposure['exposure'])
    calc_mcap = []
    for exp, mcap in zip(exposure_values, mcap_values):
        if mcap == 0:
            mcap_values.remove(mcap)
            exposure_values.remove(exp)
    for exp, mcap in zip(exposure_values, mcap_values):
        calc_mcap.append(exp * mcap)
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


def get_annualized_return(fund_info, effective_end_date, fund_nav, app_database):
    nav_start_date = get_nav_start_date(fund_info, app_database)
    start_date_nav = -1
    start_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(str(effective_end_date), "%Y-%m-%d").date()
    annualized_values = [(datetime.date(start_date.year, start_date.month, start_date.day), start_date_nav),
                         (datetime.date(end_date.year, end_date.month, end_date.day), fund_nav)]
    annualized_return = optimize.newton(lambda r: xnpv(r, annualized_values), 0.1)
    return annualized_return


def get_fund_ratios(fund_info, portfolio_values, fund_nav, benchmark_perf_1m, iq_database, app_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    fund_code = fund_info['fund_code']
    reporting_date = effective_end_date
    sorted_exposure = sorted(portfolio_values, key=lambda i: i['exposure'], reverse=True)
    sorted_pf_values = [i for i in sorted_exposure if not (i['security_name'] == 'Cash & Equivalents')]
    top5_holdings = sorted_pf_values[0:5]
    top10_holdings = sorted_pf_values[0:10]
    pe5_ratio = calc_top5_pe_ratio(top5_holdings, iq_database)
    top5_pe_ratio = None if (pe5_ratio == 0) else pe5_ratio
    pe10_ratio = calc_top10_pe_ratio(top10_holdings, iq_database)
    top10_pe_ratio = None if (pe10_ratio == 0) else pe10_ratio
    market5_cap = calc_top5_market_cap(top5_holdings, iq_database)
    top5_market_cap = None if (market5_cap == 0) else market5_cap
    market10_cap = calc_top10_market_cap(top10_holdings, iq_database)
    top10_market_cap = None if (market10_cap == 0) else market10_cap
    fund_return_list = get_all_fund_return(fund_info, iq_database)
    fund_return_list.append(fund_info['performance_1m'])
    standard_deviation = round(statistics.stdev(fund_return_list), 4)
    median = round(statistics.median(fund_return_list), 4)
    risk_free = get_risk_free_rate(iq_database)
    negative_excess_returns_risk_free = get_negative_excess_return(fund_return_list, risk_free)
    sigma = round(math.sqrt(negative_excess_returns_risk_free / 12), 4)
    annualized_return = get_annualized_return(fund_info, effective_end_date, fund_nav, app_database)
    sortino_ratio = round(((annualized_return - risk_free) / sigma), 4)
    fund_alpha = round(((fund_info['performance_1m'] - benchmark_perf_1m) * 100), 4)
    updated_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_by = "ft-automation"
    fund_ratio_data = {"fund_code": fund_code, "reporting_date": reporting_date, "top5_pe_ratio": top5_pe_ratio,
                       "top10_pe_ratio": top10_pe_ratio, "top5_market_cap": top5_market_cap,
                       "top10_market_cap": top10_market_cap, "standard_deviation": standard_deviation,
                       "median": median, "sigma": sigma, "sortino_ratio": sortino_ratio,
                       "negative_excess_returns_risk_free": negative_excess_returns_risk_free,
                       "fund_alpha": fund_alpha, "updated_ts": updated_ts, "updated_by": updated_by}
    return fund_ratio_data


def table_records(excel_values, iq_database, fs_database, app_database):
    fund_info = excel_values['fund_info']
    allocation_values = excel_values['allocation_values']
    market_cap_values = excel_values['market_cap_values']
    portfolio_values = excel_values['portfolio_values']
    sector_values = excel_values['sector_values']

    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    previous_1m_end_date = get_1m_date(fund_info)

    # Calculation of Benchmark NAV
    benchmark_nav = calc_benchmark_nav(fund_info, iq_database)
    alt_benchmark_nav = calc_alt_benchmark_nav(fund_info, iq_database)

    # Update isLatest for the previous month
    update_islatest(fund_info, previous_1m_end_date, iq_database)

    market_cap_data = get_market_cap(fund_info, market_cap_values)
    if market_cap_data is not None:
        put_market_cap_data(market_cap_data, iq_database)

    fund_perf_data, fund_nav = get_fund_performance(fund_info, allocation_values, market_cap_values, iq_database,
                                                    app_database)
    benchmark_perf_data = get_benchmark_performance(fund_info, iq_database, app_database)
    alt_benchmark_perf_data = get_alt_benchmark_performance(fund_info, iq_database, app_database)

    # Collateral details
    collateral_data = get_collateral(fund_info, fs_database, app_database)
    collateral_details = collaterals_check(fund_info, fs_database)
    print(collateral_details)
    if len(collateral_details) == 0:
        put_collateral_data(collateral_data, fs_database)

    benchmark_index_code = get_benchmark_index(fund_info, iq_database)
    alt_benchmark_index_code = get_alt_benchmark_index(fund_info, iq_database)
    nav_data = {"fund_code": fund_info['fund_code'], "benchmark_index_code": benchmark_index_code,
                "alt_benchmark_index_code": alt_benchmark_index_code, "fund_nav": fund_nav,
                "benchmark_nav": benchmark_nav, "alt_benchmark_nav": alt_benchmark_nav,
                "effective_end_date": effective_end_date}

    if portfolio_values is not None:
        portfolio_data = get_fund_portfolio(fund_info, portfolio_values, iq_database)
        put_fund_portfolio(portfolio_data, iq_database)

    portfolio_sum = 0
    for value in portfolio_values:
        if 'exposure' in value:
            portfolio_sum += value['exposure']
    portfolio_sum = round(portfolio_sum * 100)

    if portfolio_sum == 100:
        sector_data = get_fund_sector_from_portfolio(portfolio_values, iq_database)
    elif portfolio_sum > 0 and portfolio_sum != 100:
        sector_data = get_fund_sector(sector_values, iq_database)
    elif portfolio_sum == 0:
        sector_data = get_fund_sector_from_portfolio(portfolio_values, iq_database)
    else:
        sector_data = None

    sector_data_list = []
    if sector_data is not None:
        for sector_name, exposure in sector_data.items():
            sectorBody = {"fund_code": fund_info['fund_code'], "sector_type_name": sector_name,
                          "exposure": exposure, "start_date": effective_start_date,
                          "end_date": effective_end_date, "created_ts": fund_perf_data['created_ts'],
                          "action_by": fund_perf_data['created_by']}
            sector_data_list.append(sectorBody)
        put_fund_sector(sector_data_list, iq_database)

    if portfolio_sum > 0:
        fund_ratio_data = get_fund_ratios(fund_info, portfolio_values, fund_nav,
                                          benchmark_perf_data['benchmark_perf_1m'], iq_database, app_database)
        put_fund_ratio_data(fund_ratio_data, iq_database)

    final_data = {"fund_perf_data": fund_perf_data, "benchmark_perf_data": benchmark_perf_data,
                  "alt_benchmark_perf_data": alt_benchmark_perf_data, "nav_data": nav_data}
    return final_data
