from dateutil.relativedelta import relativedelta
import calendar
import datetime
import re
from pyjarowinkler import distance
from pandas.tseries.offsets import BMonthEnd

from Spiders.db_actions import get_benchmark_index, get_previous_index_price, get_index_price, get_benchmark_nav, \
    get_alt_benchmark_index, get_alt_index_price, get_alt_previous_index_price, get_alt_benchmark_nav, \
    get_previous_1m_nav, get_previous_3m_nav, get_previous_6m_nav, get_previous_1y_nav, get_previous_2y_nav, \
    get_previous_3y_nav, get_previous_5y_nav, get_inception_date, get_benchmark_3m_nav, get_benchmark_6m_nav, \
    get_benchmark_1y_nav, get_benchmark_2y_nav, get_benchmark_3y_nav, get_benchmark_5y_nav, get_alt_benchmark_3m_nav, \
    get_alt_benchmark_6m_nav, get_alt_benchmark_1y_nav, get_alt_benchmark_2y_nav, get_alt_benchmark_3y_nav, \
    get_alt_benchmark_5y_nav, get_isin_sector, get_all_isin, get_sector_type, get_sector_cash_type, update_islatest


def get_effective_start_end_date(file_date):
    start_date = datetime.datetime.strptime(file_date, '%b %Y').date()
    effective_start_date = start_date.replace(day=1)
    effective_end_date = start_date.replace(
        day=calendar.monthrange(effective_start_date.year, effective_start_date.month)[1])
    return effective_start_date, effective_end_date


def get_last_working_date(file_date):
    start_date = datetime.datetime.strptime(file_date, '%b %Y').date()
    end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
    offset = BMonthEnd()
    last_date = offset.rollforward(start_date)
    effective_last_date = last_date.date()
    return start_date, end_date, effective_last_date


def get_previous_last_working_date(file_date):
    start_date, end_date, effective_last_date = get_last_working_date(file_date)
    previous_month_date = start_date - relativedelta(months=1)
    previous_month_end_date = previous_month_date.replace(day=calendar.monthrange(previous_month_date.year,
                                                                                  previous_month_date.month)[1])
    off = BMonthEnd()
    previous_month_end_date = off.rollback(previous_month_end_date)
    return previous_month_end_date


def get_1m_date(file_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    previous_1m_date = effective_end_date - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1])
    return previous_1m_end_date


def get_3m_date(file_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    previous_3m_date = effective_end_date - relativedelta(months=3)
    previous_3m_end_date = previous_3m_date.replace(day=calendar.monthrange(previous_3m_date.year,
                                                                            previous_3m_date.month)[1])
    return previous_3m_end_date


def get_6m_date(file_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    previous_6m_date = effective_end_date - relativedelta(months=6)
    previous_6m_end_date = previous_6m_date.replace(day=calendar.monthrange(previous_6m_date.year,
                                                                            previous_6m_date.month)[1])
    return previous_6m_end_date


def get_1y_date(file_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    previous_1y_date = effective_end_date - relativedelta(years=1)
    previous_1y_end_date = (previous_1y_date.replace(day=calendar.monthrange(previous_1y_date.year,
                                                                             previous_1y_date.month)[1]))
    return previous_1y_end_date


def get_2y_date(file_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    previous_2y_date = effective_end_date - relativedelta(years=2)
    previous_2y_end_date = previous_2y_date.replace(day=calendar.monthrange(previous_2y_date.year,
                                                                            previous_2y_date.month)[1])
    return previous_2y_end_date


def get_3y_date(file_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    previous_3y_date = effective_end_date - relativedelta(years=3)
    previous_3y_end_date = previous_3y_date.replace(day=calendar.monthrange(previous_3y_date.year,
                                                                            previous_3y_date.month)[1])
    return previous_3y_end_date


def get_5y_date(file_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    previous_5y_date = effective_end_date - relativedelta(years=5)
    previous_5y_end_date = previous_5y_date.replace(day=calendar.monthrange(previous_5y_date.year,
                                                                            previous_5y_date.month)[1])
    return previous_5y_end_date


def calc_benchmark_nav(fund_code, database, file_date):
    start_date, end_date, effective_last_date = get_last_working_date(file_date)
    previous_month_end_date = get_1m_date(file_date)
    prev_month_end_date = get_previous_last_working_date(file_date)
    benchmark_index = get_benchmark_index(fund_code, database, end_date)
    index_price = get_index_price(benchmark_index, database, effective_last_date)
    previous_index_price = get_previous_index_price(benchmark_index, database, prev_month_end_date)
    previous_benchmark_nav = get_benchmark_nav(fund_code, database, previous_month_end_date)
    benchmark_return = (index_price / previous_index_price) - 1
    benchmark_nav = round((previous_benchmark_nav * (1 + benchmark_return)), 4)
    return benchmark_nav


def calc_alt_benchmark_nav(fund_code, database, file_date):
    start_date, end_date, effective_last_date = get_last_working_date(file_date)
    alt_previous_month_end_date = get_1m_date(file_date)
    alt_prev_month_end_date = get_previous_last_working_date(file_date)
    alt_benchmark_index = get_alt_benchmark_index(fund_code, database, end_date)
    alt_index_price = get_alt_index_price(alt_benchmark_index, database, effective_last_date)
    alt_previous_index_price = get_alt_previous_index_price(alt_benchmark_index, database, alt_prev_month_end_date)
    alt_benchmark_previous_nav = get_alt_benchmark_nav(fund_code, database, alt_previous_month_end_date)
    alt_benchmark_return = (alt_index_price / alt_previous_index_price) - 1
    alt_benchmark_nav = round((alt_benchmark_previous_nav * (1 + alt_benchmark_return)), 4)
    return alt_benchmark_nav


def get_market_cap_type_code(cap_type):
    global market_cap_type_code
    for market_cap, exposure in cap_type.items():
        if len(cap_type) == 1:
            if cap_type['Cash']:
                cap_type = None
                break
    mega_value = cap_type['Mega'] if 'Mega' in cap_type.keys() else 0
    large_value = cap_type['Large'] if 'Large' in cap_type.keys() else 0
    small_value = cap_type['Small'] if 'Small' in cap_type.keys() else 0
    micro_value = cap_type['Micro'] if 'Micro' in cap_type.keys() else 0
    cap_type.update({"Large": mega_value + large_value})
    cap_type.update({"Small": small_value + micro_value})
    keys_to_remove = ["Cash", "Micro", "Mega"]
    for key in keys_to_remove:
        if key in cap_type.keys():
            del cap_type[key]
    large_exposure = cap_type['Large'] if 'Large' in cap_type.keys() else 0
    small_exposure = cap_type['Small'] if 'Small' in cap_type.keys() else 0
    mid_exposure = cap_type['Mid'] if 'Mid' in cap_type.keys() else 0
    if large_exposure >= 20 and mid_exposure >= 20 and small_exposure >= 20:
        market_cap_type_code = "MULTI"
    elif ((65 > large_exposure >= 35 and 65 > mid_exposure >= 35) or
          (65 > mid_exposure >= 35 and 65 > small_exposure >= 35) or
          (65 > small_exposure >= 35 and 65 > large_exposure >= 35)):
        if large_exposure < mid_exposure and large_exposure < small_exposure:
            market_cap_type_code = "MIDSMALL"
        elif mid_exposure < large_exposure and mid_exposure < small_exposure:
            market_cap_type_code = "LARGESMALL"
        elif small_exposure < large_exposure and small_exposure < mid_exposure:
            market_cap_type_code = "LARGEMID"
    else:
        if large_exposure > mid_exposure and large_exposure > small_exposure:
            market_cap_type_code = "LARGE"
        elif mid_exposure > large_exposure and mid_exposure > small_exposure:
            market_cap_type_code = "MID"
        else:
            market_cap_type_code = "SMALL"
    return market_cap_type_code


def get_fund_performance(fund_code, fund_info, market_cap_values, database, file_date):
    if fund_info['aum'] is not None:
        aum = float(fund_info['aum'].replace("Rs ", "").replace(" cr", ""))
        current_aum = float(aum) * 10000000
    else:
        current_aum = None
    clients = fund_info['clients']
    no_of_clients = None if clients == "nan" else clients
    # getting fund allocations
    equity_allocation = float(fund_info['equity_allocation'])
    portfolio_equity_allocation = round((equity_allocation / 100), 4)
    cash_allocation = float(fund_info['cash_allocation'])
    portfolio_cash_allocation = round((cash_allocation / 100), 4)
    asset_allocation = float(fund_info['asset_allocation'])
    if asset_allocation == "-" or asset_allocation is None:
        portfolio_asset_allocation = None
    elif asset_allocation == float(fund_info['asset_allocation']):
        portfolio_asset_allocation = round((asset_allocation / 100), 4)
    else:
        portfolio_asset_allocation = None
    performance_1m = round(float(fund_info['performance_1m']), 4)
    created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = "fintuple-data"
    isLatest = '1'
    market_cap_type_code = get_market_cap_type_code(market_cap_values)
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    previous_1m_end_date = get_1m_date(file_date)
    previous_1m_nav = get_previous_1m_nav(fund_code, previous_1m_end_date, database)
    # current month fund NAV
    previous_1m_nav_final = previous_1m_nav[0][0]
    fund_nav = round((previous_1m_nav_final * (1 + performance_1m)), 4)
    # performance of 1 month
    perf_1m = round(((fund_nav / previous_1m_nav_final) - 1), 4)
    # performance of 3 months
    previous_3m_end_date = get_3m_date(file_date)
    previous_3m = get_previous_3m_nav(fund_code, previous_3m_end_date, database)
    if len(previous_3m) == 0:
        perf_3m = None
    else:
        previous_3m_final = previous_3m[0][0]
        perf_3m = round(((fund_nav / previous_3m_final) - 1), 4)
    # performance of 6 months
    previous_6m_end_date = get_6m_date(file_date)
    previous_6m = get_previous_6m_nav(fund_code, previous_6m_end_date, database)
    if len(previous_6m) == 0:
        perf_6m = None
    else:
        previous_6m_final = previous_6m[0][0]
        perf_6m = round(((fund_nav / previous_6m_final) - 1), 4)
    # performance of 1 year
    previous_1y_end_date = get_1y_date(file_date)
    previous_1y = get_previous_1y_nav(fund_code, previous_1y_end_date, database)
    if len(previous_1y) == 0:
        perf_1y = None
    else:
        previous_1y_final = previous_1y[0][0]
        date_power_1y = effective_end_date - previous_1y_end_date
        perf_1y = round((((fund_nav / previous_1y_final) ** (365 / date_power_1y.days)) - 1), 4)
    # performance of 2 years
    previous_2y_end_date = get_2y_date(file_date)
    previous_2y = get_previous_2y_nav(fund_code, previous_2y_end_date, database)
    if len(previous_2y) == 0:
        perf_2y = None
    else:
        previous_2y_final = previous_2y[0][0]
        date_power_2y = effective_end_date - previous_2y_end_date
        perf_2y = round((((fund_nav / previous_2y_final) ** (365 / date_power_2y.days)) - 1), 4)
    # performance of 3 years
    previous_3y_end_date = get_3y_date(file_date)
    previous_3y = get_previous_3y_nav(fund_code, previous_3y_end_date, database)
    if len(previous_3y) == 0:
        perf_3y = None
    else:
        previous_3y_final = previous_3y[0][0]
        date_power_3y = effective_end_date - previous_3y_end_date
        perf_3y = round((((fund_nav / previous_3y_final) ** (365 / date_power_3y.days)) - 1), 4)
    # performance of 5 years
    previous_5y_end_date = get_5y_date(file_date)
    previous_5y = get_previous_5y_nav(fund_code, previous_5y_end_date, database)
    if len(previous_5y) == 0:
        perf_5y = None
    else:
        previous_5y_final = previous_5y[0][0]
        date_power_5y = effective_end_date - previous_5y_end_date
        perf_5y = round((((fund_nav / previous_5y_final) ** (365 / date_power_5y.days)) - 1), 4)
    # performance inception
    inception_date = get_inception_date(fund_code, database)
    date_power_inception = effective_end_date - inception_date
    perf_inception = round((((fund_nav / 1) ** (365 / date_power_inception.days)) - 1), 4)
    return fund_code, current_aum, no_of_clients, market_cap_type_code, portfolio_equity_allocation, \
           portfolio_cash_allocation, portfolio_asset_allocation, perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, \
           perf_3y, perf_5y, perf_inception, isLatest, effective_start_date, effective_end_date, created_ts, \
           created_by, fund_nav


def get_benchmark_performance(fund_code, database, file_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    start_date, end_date, effective_lwd_date = get_last_working_date(file_date)
    previous_month_end_date = get_1m_date(file_date)
    benchmark_index_code = get_benchmark_index(fund_code, database, end_date)
    previous_benchmark_nav = get_benchmark_nav(fund_code, database, previous_month_end_date)
    benchmark_nav = calc_benchmark_nav(fund_code, database, file_date)
    # benchmark performance of 1 month
    benchmark_perf_1m = round(((benchmark_nav / previous_benchmark_nav) - 1), 4)
    # benchmark performance of 3 months
    benchmark_3m_end_date = get_3m_date(file_date)
    benchmark_3m = get_benchmark_3m_nav(fund_code, benchmark_index_code, benchmark_3m_end_date, database)
    if len(benchmark_3m) == 0:
        benchmark_perf_3m = None
    else:
        benchmark_3m_final = benchmark_3m[0][0]
        benchmark_perf_3m = round(((benchmark_nav / benchmark_3m_final) - 1), 4)
    # benchmark performance of 6 months
    benchmark_6m_end_date = get_6m_date(file_date)
    benchmark_6m = get_benchmark_6m_nav(fund_code, benchmark_index_code, benchmark_6m_end_date, database)
    if len(benchmark_6m) == 0:
        benchmark_perf_6m = None
    else:
        benchmark_6m_final = benchmark_6m[0][0]
        benchmark_perf_6m = round(((benchmark_nav / benchmark_6m_final) - 1), 4)
    # benchmark performance of 1 year
    benchmark_1y_end_date = get_1y_date(file_date)
    benchmark_1y = get_benchmark_1y_nav(fund_code, benchmark_index_code, benchmark_1y_end_date, database)
    if len(benchmark_1y) == 0:
        benchmark_perf_1y = None
    else:
        benchmark_1y_final = benchmark_1y[0][0]
        benchmark_date_power_1y = effective_end_date - benchmark_1y_end_date
        benchmark_perf_1y = round((((benchmark_nav / benchmark_1y_final) ** (365 / benchmark_date_power_1y.days)) - 1),
                                  4)
    # benchmark performance of 2 years
    benchmark_2y_end_date = get_2y_date(file_date)
    benchmark_2y = get_benchmark_2y_nav(fund_code, benchmark_index_code, benchmark_2y_end_date, database)
    if len(benchmark_2y) == 0:
        benchmark_perf_2y = None
    else:
        benchmark_2y_final = benchmark_2y[0][0]
        benchmark_date_power_2y = effective_end_date - benchmark_2y_end_date
        benchmark_perf_2y = round((((benchmark_nav / benchmark_2y_final) ** (365 / benchmark_date_power_2y.days)) - 1),
                                  4)
    # benchmark performance of 3 years
    benchmark_3y_end_date = get_3y_date(file_date)
    benchmark_3y = get_benchmark_3y_nav(fund_code, benchmark_index_code, benchmark_3y_end_date, database)
    if len(benchmark_3y) == 0:
        benchmark_perf_3y = None
    else:
        benchmark_3y_final = benchmark_3y[0][0]
        benchmark_date_power_3y = effective_end_date - benchmark_3y_end_date
        benchmark_perf_3y = round((((benchmark_nav / benchmark_3y_final) ** (365 / benchmark_date_power_3y.days)) - 1),
                                  4)
    # benchmark performance of 5 years
    benchmark_5y_end_date = get_5y_date(file_date)
    benchmark_5y = get_benchmark_5y_nav(fund_code, benchmark_index_code, benchmark_5y_end_date, database)
    if len(benchmark_5y) == 0:
        benchmark_perf_5y = None
    else:
        benchmark_5y_final = benchmark_5y[0][0]
        benchmark_date_power_5y = effective_end_date - benchmark_5y_end_date
        benchmark_perf_5y = round((((benchmark_nav / benchmark_5y_final) ** (365 / benchmark_date_power_5y.days)) - 1),
                                  4)
    # benchmark performance inception
    inception_date = get_inception_date(fund_code, database)
    benchmark_power_inception = effective_end_date - inception_date
    benchmark_perf_inception = round((((benchmark_nav / 1) ** (365 / benchmark_power_inception.days)) - 1), 4)
    return benchmark_perf_1m, benchmark_perf_3m, benchmark_perf_6m, benchmark_perf_1y, benchmark_perf_2y, \
           benchmark_perf_3y, benchmark_perf_5y, benchmark_perf_inception


def get_alt_benchmark_performance(fund_code, database, file_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    start_date, end_date, effective_last_date = get_last_working_date(file_date)
    alt_previous_month_end_date = get_1m_date(file_date)
    alt_benchmark_nav = calc_alt_benchmark_nav(fund_code, database, file_date)
    alt_benchmark_index_code = get_alt_benchmark_index(fund_code, database, end_date)
    alt_benchmark_previous_nav = get_alt_benchmark_nav(fund_code, database, alt_previous_month_end_date)
    # alternate benchmark performance of 1 month
    alt_benchmark_perf_1m = round(((alt_benchmark_nav / alt_benchmark_previous_nav) - 1), 4)
    # alternate benchmark performance of 3 months
    alt_benchmark_3m_end_date = get_3m_date(file_date)
    alt_benchmark_3m = get_alt_benchmark_3m_nav(fund_code, alt_benchmark_index_code, alt_benchmark_3m_end_date,
                                                database)
    if len(alt_benchmark_3m) == 0:
        alt_benchmark_perf_3m = None
    else:
        alt_benchmark_3m_final = alt_benchmark_3m[0][0]
        alt_benchmark_perf_3m = round(((alt_benchmark_nav / alt_benchmark_3m_final) - 1), 4)
    # alternate benchmark performance of 6 months
    alt_benchmark_6m_end_date = get_6m_date(file_date)
    alt_benchmark_6m = get_alt_benchmark_6m_nav(fund_code, alt_benchmark_index_code, alt_benchmark_6m_end_date,
                                                database)
    if len(alt_benchmark_6m) == 0:
        alt_benchmark_perf_6m = None
    else:
        alt_benchmark_6m_final = alt_benchmark_6m[0][0]
        alt_benchmark_perf_6m = round(((alt_benchmark_nav / alt_benchmark_6m_final) - 1), 4)
    # alternate benchmark performance of 1 year
    alt_benchmark_1y_end_date = get_1y_date(file_date)
    alt_benchmark_1y = get_alt_benchmark_1y_nav(fund_code, alt_benchmark_index_code, alt_benchmark_1y_end_date,
                                                database)
    if len(alt_benchmark_1y) == 0:
        alt_benchmark_perf_1y = None
    else:
        alt_benchmark_1y_final = alt_benchmark_1y[0][0]
        alt_benchmark_date_power_1y = effective_end_date - alt_benchmark_1y_end_date
        alt_benchmark_perf_1y = round((((alt_benchmark_nav / alt_benchmark_1y_final) **
                                        (365 / alt_benchmark_date_power_1y.days)) - 1), 4)
    # alternate benchmark performance of 2 years
    alt_benchmark_2y_end_date = get_2y_date(file_date)
    alt_benchmark_2y = get_alt_benchmark_2y_nav(fund_code, alt_benchmark_index_code, alt_benchmark_2y_end_date,
                                                database)
    if len(alt_benchmark_2y) == 0:
        alt_benchmark_perf_2y = None
    else:
        alt_benchmark_2y_final = alt_benchmark_2y[0][0]
        alt_benchmark_date_power_2y = effective_end_date - alt_benchmark_2y_end_date
        alt_benchmark_perf_2y = round((((alt_benchmark_nav / alt_benchmark_2y_final) **
                                        (365 / alt_benchmark_date_power_2y.days)) - 1), 4)
    # alternate benchmark performance of 3 years
    alt_benchmark_3y_end_date = get_3y_date(file_date)
    alt_benchmark_3y = get_alt_benchmark_3y_nav(fund_code, alt_benchmark_index_code, alt_benchmark_3y_end_date,
                                                database)
    if len(alt_benchmark_3y) == 0:
        alt_benchmark_perf_3y = None
    else:
        alt_benchmark_3y_final = alt_benchmark_3y[0][0]
        alt_benchmark_date_power_3y = effective_end_date - alt_benchmark_3y_end_date
        alt_benchmark_perf_3y = round((((alt_benchmark_nav / alt_benchmark_3y_final) **
                                        (365 / alt_benchmark_date_power_3y.days)) - 1), 4)
    # alternate benchmark performance of 5 years
    alt_benchmark_5y_end_date = get_5y_date(file_date)
    alt_benchmark_5y = get_alt_benchmark_5y_nav(fund_code, alt_benchmark_index_code, alt_benchmark_5y_end_date,
                                                database)
    if len(alt_benchmark_5y) == 0:
        alt_benchmark_perf_5y = None
    else:
        alt_benchmark_5y_final = alt_benchmark_5y[0][0]
        alt_benchmark_date_power_5y = effective_end_date - alt_benchmark_5y_end_date
        alt_benchmark_perf_5y = round((((alt_benchmark_nav / alt_benchmark_5y_final) **
                                        (365 / alt_benchmark_date_power_5y.days)) - 1), 4)
    # alternate benchmark inception
    inception_date = get_inception_date(fund_code, database)
    alt_benchmark_power_inception = effective_end_date - inception_date
    alt_benchmark_perf_inception = round((((alt_benchmark_nav / 1) ** (365 / alt_benchmark_power_inception.days)) - 1),
                                         4)
    return alt_benchmark_perf_1m, alt_benchmark_perf_3m, alt_benchmark_perf_6m, alt_benchmark_perf_1y, \
           alt_benchmark_perf_2y, alt_benchmark_perf_3y, alt_benchmark_perf_5y, alt_benchmark_perf_inception


def get_market_cap(market_cap_values, fund_code, file_date):
    created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = "fintuple-data"
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    capData = []
    for type_market_cap, exposure in market_cap_values.items():
        cap_body = {}
        cap_body.update({"fund_code": fund_code})
        cap_body.update({"type_market_cap": type_market_cap})
        exposure_calc = round((float(exposure) / 100), 4)
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


def get_isin(security_name, database):
    global security_isin
    abbreviation_dict = {"ONGC": "Oil and Natural Gas Corporation Limited",
                         "MCX": "Multi Commodity Exchange of India Limited"}
    if security_name == "Cash & Equivalents" or security_name == "Cash":
        security_isin = "CASH"
    else:
        if "ONGC" in security_name:
            sec_name = abbreviation_dict['ONGC']
        elif "MCX" in security_name:
            sec_name = abbreviation_dict['MCX']
        else:
            sec_name = security_name
        isin_details = get_isin_sector(sec_name, database)
        if len(isin_details) == 0:
            sec_name = sec_name.replace(".", " ")
            cleaned_sec_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', sec_name).lower()
            security_details = get_all_isin(database)
            max_ratio = 0
            max_index = 0
            for value in range(len(security_details)):
                name = security_details[value][1].replace(".", " ")
                cleaned_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', name).lower()
                ratio = distance.get_jaro_distance(cleaned_sec_name, cleaned_name, winkler=True, scaling=0.1)
                if ratio > 0 and max_ratio < ratio:
                    max_ratio = ratio
                    max_index = value
            security_isin = security_details[max_index][0]
        else:
            security_isin = isin_details[0][0]
    return security_isin


def get_fund_portfolio(portfolio_values, fund_code, database, file_date):
    created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = "fintuple-data"
    effective_start_date, effective_end_date = get_effective_start_end_date(file_date)
    portfoliodata = []
    for value in portfolio_values:
        portfolio_body = {}
        portfolio_body.update({"fund_code": fund_code})
        portfolio_body.update({"security_isin": get_isin(value['security_name'], database)})
        portfolio_body.update({"exposure": round(float(value['exposure']), 4)})
        portfolio_body.update({"start_date": effective_start_date})
        portfolio_body.update({"end_date": effective_end_date})
        portfolio_body.update({"created_ts": created_ts})
        portfolio_body.update({"action_by": created_by})
        portfoliodata.append(portfolio_body)
    return portfoliodata


def get_security_list(portfolio_values, database):
    security_isin_list = []
    for value in portfolio_values:
        security_name = value['security_name']
        security_isin = get_isin(security_name, database)
        exposure = float(value['exposure'])
        security_isin_list.append(
            {"security_name": security_name, "security_isin": security_isin, "exposure": exposure})
    return security_isin_list


def get_fund_sector(portfolio_values, database):
    global sec_isin, sector_response
    sector_breakdown = []
    securityList = get_security_list(portfolio_values, database)
    for securityData in securityList:
        sector_body = {"security": securityData["security_name"], "isin": securityData["security_isin"],
                       "sector": None, "exposure": securityData["exposure"]}
        if securityData["security_isin"] != "CASH":
            sec_isin = securityData["security_isin"]
            sector_response = get_sector_type(sec_isin, database)
        elif securityData["security_isin"] == 'CASH':
            sec_isin = securityData["security_isin"]
            sector_response = get_sector_cash_type(sec_isin, database)
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
    return sector_breakdown_result


def put_into_iq_db(fund_code, fund_info, portfolio_values, market_cap_values, database, file_date):
    marketcapData = get_market_cap(market_cap_values, fund_code, file_date)
    start_date, end_date, effective_last_date = get_last_working_date(file_date)
    previous_1m_end_date = get_1m_date(file_date)
    # update isLatest
    update_islatest(database, previous_1m_end_date)
    # get fund performance
    fund_code, current_aum, no_of_clients, market_cap_type_code, portfolio_equity_allocation, \
    portfolio_cash_allocation, portfolio_asset_allocation, perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, perf_3y, \
    perf_5y, perf_inception, isLatest, effective_start_date, effective_end_date, created_ts, created_by, \
    fund_nav = get_fund_performance(fund_code, fund_info, market_cap_values, database, file_date)
    # get benchmark performance
    benchmark_perf_1m, benchmark_perf_3m, benchmark_perf_6m, benchmark_perf_1y, benchmark_perf_2y, benchmark_perf_3y, \
    benchmark_perf_5y, benchmark_perf_inception = get_benchmark_performance(fund_code, database, file_date)
    # get alternate benchmark performance
    alt_benchmark_perf_1m, alt_benchmark_perf_3m, alt_benchmark_perf_6m, alt_benchmark_perf_1y, alt_benchmark_perf_2y, \
    alt_benchmark_perf_3y, alt_benchmark_perf_5y, alt_benchmark_perf_inception = get_alt_benchmark_performance(
        fund_code, database, file_date)
    benchmark_index_code = get_benchmark_index(fund_code, database, end_date)
    alt_benchmark_index_code = get_alt_benchmark_index(fund_code, database, end_date)
    benchmark_nav = calc_benchmark_nav(fund_code, database, file_date)
    alt_benchmark_nav = calc_alt_benchmark_nav(fund_code, database, file_date)
    portfolioData = get_fund_portfolio(portfolio_values, fund_code, database, file_date)
    sectorData = get_fund_sector(portfolio_values, database)
    sectorDataList = []
    fundData = {}
    navData = {}
    fundData.update({"fund_code": fund_code, "current_aum": current_aum, "no_of_clients": no_of_clients,
                     "market_cap_type_code": market_cap_type_code,
                     "portfolio_equity_allocation": portfolio_equity_allocation,
                     "portfolio_cash_allocation": portfolio_cash_allocation,
                     "portfolio_asset_allocation": portfolio_asset_allocation, "perf_1m": perf_1m,
                     "perf_3m": perf_3m, "perf_6m": perf_6m, "perf_1y": perf_1y, "perf_2y": perf_2y,
                     "perf_3y": perf_3y, "perf_5y": perf_5y, "perf_inception": perf_inception, "isLatest": isLatest,
                     "effective_start_date": effective_start_date, "effective_end_date": effective_end_date,
                     "created_ts": created_ts, "created_by": created_by, "benchmark_perf_1m": benchmark_perf_1m,
                     "benchmark_perf_3m": benchmark_perf_3m, "benchmark_perf_6m": benchmark_perf_6m,
                     "benchmark_perf_1y": benchmark_perf_1y, "benchmark_perf_2y": benchmark_perf_2y,
                     "benchmark_perf_3y": benchmark_perf_3y, "benchmark_perf_5y": benchmark_perf_5y,
                     "benchmark_perf_inception": benchmark_perf_inception,
                     "alt_benchmark_perf_1m": alt_benchmark_perf_1m, "alt_benchmark_perf_3m": alt_benchmark_perf_3m,
                     "alt_benchmark_perf_6m": alt_benchmark_perf_6m, "alt_benchmark_perf_1y": alt_benchmark_perf_1y,
                     "alt_benchmark_perf_2y": alt_benchmark_perf_2y, "alt_benchmark_perf_3y": alt_benchmark_perf_3y,
                     "alt_benchmark_perf_5y": alt_benchmark_perf_5y,
                     "alt_benchmark_perf_inception": alt_benchmark_perf_inception})
    navData.update({"fund_code": fund_code, "benchmark_index_code": benchmark_index_code,
                    "alt_benchmark_index_code": alt_benchmark_index_code, "fund_nav": fund_nav,
                    "benchmark_nav": benchmark_nav, "alt_benchmark_nav": alt_benchmark_nav,
                    "effective_end_date": effective_end_date})
    for sector_name, exposure in sectorData.items():
        sectorBody = {"fund_code": fund_code, "sector_type_name": sector_name, "exposure": round(exposure, 4),
                      "start_date": effective_start_date, "end_date": effective_end_date, "created_ts": created_ts,
                      "action_by": created_by}
        sectorDataList.append(sectorBody)
    return fundData, navData, marketcapData, portfolioData, sectorDataList
