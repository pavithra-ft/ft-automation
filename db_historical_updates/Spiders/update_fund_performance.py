import MySQLdb
import datetime

from envparse import env

from Spiders.date_calculation import get_effective_start_end_date, get_1m_date, get_3m_date, get_6m_date, get_1y_date, \
    get_2y_date, get_3y_date, get_5y_date
from Spiders.db_actions import get_benchmark_index, get_index_price_as_on_date, get_alt_benchmark_index, get_fund_nav, \
    get_nav_start_date, get_start_price, put_fund_performance, update_islatest, get_nav_dates, get_current_fund_nav, \
    get_investment_style


def get_fund_performance(fund_code, reporting_date, iq_database, app_database):
    perf_1m = perf_3m = perf_6m = perf_1y = perf_2y = perf_3y = perf_5y = None
    effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)
    # Calculation of Fund NAV
    nav_start_date = get_nav_start_date(fund_code, app_database)
    prev_1m_end_date = get_1m_date(reporting_date)
    prev_3m_end_date = get_3m_date(reporting_date)
    prev_6m_end_date = get_6m_date(reporting_date)
    prev_1y_end_date = get_1y_date(reporting_date)
    prev_2y_end_date = get_2y_date(reporting_date)
    prev_3y_end_date = get_3y_date(reporting_date)
    prev_5y_end_date = get_5y_date(reporting_date)

    fund_1m_nav = get_fund_nav(fund_code, prev_1m_end_date, iq_database)
    fund_3m_nav = get_fund_nav(fund_code, prev_3m_end_date, iq_database)
    fund_6m_nav = get_fund_nav(fund_code, prev_6m_end_date, iq_database)
    fund_1y_nav = get_fund_nav(fund_code, prev_1y_end_date, iq_database)
    fund_2y_nav = get_fund_nav(fund_code, prev_2y_end_date, iq_database)
    fund_3y_nav = get_fund_nav(fund_code, prev_3y_end_date, iq_database)
    fund_5y_nav = get_fund_nav(fund_code, prev_5y_end_date, iq_database)
    fund_nav = get_current_fund_nav(fund_code, reporting_date, iq_database)

    date_power_1y = effective_end_date - prev_1y_end_date
    date_power_2y = effective_end_date - prev_2y_end_date
    date_power_3y = effective_end_date - prev_3y_end_date
    date_power_5y = effective_end_date - prev_5y_end_date
    date_power_inception = effective_end_date - nav_start_date

    # Calculation of 1 month Fund performance
    if nav_start_date <= prev_1m_end_date:
        perf_1m = round(((fund_nav[0][0] / fund_1m_nav[0][0]) - 1), 4) if fund_1m_nav else None
    # Calculation of 3 months Fund performance
    if nav_start_date <= prev_3m_end_date:
        perf_3m = round(((fund_nav[0][0] / fund_3m_nav[0][0]) - 1), 4) if fund_3m_nav else None
    # Calculation of 6 months Fund performance
    if nav_start_date <= prev_6m_end_date:
        perf_6m = round(((fund_nav[0][0] / fund_6m_nav[0][0]) - 1), 4) if fund_6m_nav else None
    # Calculation of 1 year Fund performance
    if nav_start_date <= prev_1y_end_date:
        perf_1y = round((((fund_nav[0][0] / fund_1y_nav[0][0]) ** (365 / date_power_1y.days)) - 1), 4) if fund_1y_nav \
            else None
    # Calculation of 2 years Fund performance
    if nav_start_date <= prev_2y_end_date:
        perf_2y = round((((fund_nav[0][0] / fund_2y_nav[0][0]) ** (365 / date_power_2y.days)) - 1), 4) if fund_2y_nav \
            else None
    # Calculation of 3 years Fund performance
    if nav_start_date <= prev_3y_end_date:
        perf_3y = round((((fund_nav[0][0] / fund_3y_nav[0][0]) ** (365 / date_power_3y.days)) - 1), 4) if fund_3y_nav \
            else None
    # Calculation of 5 years Fund performance
    if nav_start_date <= prev_5y_end_date:
        perf_5y = round((((fund_nav[0][0] / fund_5y_nav[0][0]) ** (365 / date_power_5y.days)) - 1), 4) if fund_5y_nav \
            else None
    # Calculation of Fund performance inception
    if date_power_inception.days >= 365:
        perf_inception = round((((fund_nav[0][0] / 1) ** (365 / date_power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((fund_nav[0][0] / 1) - 1), 4)
    fundperfData = {"fund_code": fund_code, "current_aum": None, "no_of_clients": None, "market_cap_type_code": None,
                    "investment_style_type_code": get_investment_style(fund_code, app_database),
                    "portfolio_equity_allocation": None, "portfolio_cash_allocation": None,
                    "portfolio_asset_allocation": None, "portfolio_other_allocations": None, "perf_1m": perf_1m,
                    "perf_3m": perf_3m, "perf_6m": perf_6m, "perf_1y": perf_1y, "perf_2y": perf_2y, "perf_3y": perf_3y,
                    "perf_5y": perf_5y, "perf_inception": perf_inception, "isLatest": '1',
                    "effective_start_date": effective_start_date, "effective_end_date": effective_end_date,
                    "created_ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "created_by": "ft-automation"}
    return fundperfData


def get_benchmark_performance(fund_code, reporting_date, iq_database, app_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)
    benchmark_index_code = get_benchmark_index(fund_code, iq_database)
    nav_start_date = get_nav_start_date(fund_code, app_database)
    start_index_price = get_start_price(nav_start_date, benchmark_index_code, iq_database)
    curr_price = get_index_price_as_on_date(effective_end_date, benchmark_index_code, iq_database)

    benchmark_1m_date = get_1m_date(reporting_date)
    benchmark_3m_date = get_3m_date(reporting_date)
    benchmark_6m_date = get_6m_date(reporting_date)
    benchmark_1y_date = get_1y_date(reporting_date)
    benchmark_2y_date = get_2y_date(reporting_date)
    benchmark_3y_date = get_3y_date(reporting_date)
    benchmark_5y_date = get_5y_date(reporting_date)

    benchmark_1m_price = get_index_price_as_on_date(benchmark_1m_date, benchmark_index_code, iq_database)
    benchmark_3m_price = get_index_price_as_on_date(benchmark_3m_date, benchmark_index_code, iq_database)
    benchmark_6m_price = get_index_price_as_on_date(benchmark_6m_date, benchmark_index_code, iq_database)
    benchmark_1y_price = get_index_price_as_on_date(benchmark_1y_date, benchmark_index_code, iq_database)
    benchmark_2y_price = get_index_price_as_on_date(benchmark_2y_date, benchmark_index_code, iq_database)
    benchmark_3y_price = get_index_price_as_on_date(benchmark_3y_date, benchmark_index_code, iq_database)
    benchmark_5y_price = get_index_price_as_on_date(benchmark_5y_date, benchmark_index_code, iq_database)

    bm_date_power_1y = effective_end_date - benchmark_1y_date
    bm_date_power_2y = effective_end_date - benchmark_2y_date
    bm_date_power_3y = effective_end_date - benchmark_3y_date
    bm_date_power_5y = effective_end_date - benchmark_5y_date
    benchmark_power_inception = effective_end_date - nav_start_date

    benchmark_perf_1m = round(((curr_price[0][0] / benchmark_1m_price[0][0]) - 1), 4) if \
        nav_start_date <= benchmark_1m_date else None
    benchmark_perf_3m = round(((curr_price[0][0] / benchmark_3m_price[0][0]) - 1), 4) if \
        nav_start_date <= benchmark_3m_date else None
    benchmark_perf_6m = round(((curr_price[0][0] / benchmark_6m_price[0][0]) - 1), 4) if \
        nav_start_date <= benchmark_6m_date else None
    benchmark_perf_1y = round((((curr_price[0][0] / benchmark_1y_price[0][0]) ** (365 / bm_date_power_1y.days)) - 1),
                              4) if nav_start_date <= benchmark_1y_date else None
    benchmark_perf_2y = round((((curr_price[0][0] / benchmark_2y_price[0][0]) ** (365 / bm_date_power_2y.days)) - 1),
                              4) if nav_start_date <= benchmark_2y_date else None
    benchmark_perf_3y = round((((curr_price[0][0] / benchmark_3y_price[0][0]) ** (365 / bm_date_power_3y.days)) - 1),
                              4) if nav_start_date <= benchmark_3y_date else None
    benchmark_perf_5y = round((((curr_price[0][0] / benchmark_5y_price[0][0]) ** (365 / bm_date_power_5y.days)) - 1),
                              4) if nav_start_date <= benchmark_5y_date else None
    # Calculation of Benchmark performance inception
    if benchmark_power_inception.days >= 365:
        benchmark_perf_inception = round((((curr_price[0][0] / start_index_price) **
                                           (365 / benchmark_power_inception.days)) - 1), 4)
    else:
        benchmark_perf_inception = round(((curr_price[0][0] / start_index_price) - 1), 4)
    benchmark_perf_data = {"index_code": benchmark_index_code, "benchmark_perf_1m": benchmark_perf_1m,
                           "benchmark_perf_3m": benchmark_perf_3m, "benchmark_perf_6m": benchmark_perf_6m,
                           "benchmark_perf_1y": benchmark_perf_1y, "benchmark_perf_2y": benchmark_perf_2y,
                           "benchmark_perf_3y": benchmark_perf_3y, "benchmark_perf_5y": benchmark_perf_5y,
                           "benchmark_perf_inception": benchmark_perf_inception}
    return benchmark_perf_data


def get_alt_benchmark_performance(fund_code, reporting_date, iq_database, app_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)
    alt_benchmark_index_code = get_alt_benchmark_index(fund_code, iq_database)
    nav_start_date = get_nav_start_date(fund_code, app_database)
    start_index_price = get_start_price(nav_start_date, alt_benchmark_index_code, iq_database)
    curr_price = get_index_price_as_on_date(effective_end_date, alt_benchmark_index_code, iq_database)

    alt_benchmark_1m_date = get_1m_date(reporting_date)
    alt_benchmark_3m_date = get_3m_date(reporting_date)
    alt_benchmark_6m_date = get_6m_date(reporting_date)
    alt_benchmark_1y_date = get_1y_date(reporting_date)
    alt_benchmark_2y_date = get_2y_date(reporting_date)
    alt_benchmark_3y_date = get_3y_date(reporting_date)
    alt_benchmark_5y_date = get_5y_date(reporting_date)

    alt_benchmark_1m_price = get_index_price_as_on_date(alt_benchmark_1m_date, alt_benchmark_index_code, iq_database)
    alt_benchmark_3m_price = get_index_price_as_on_date(alt_benchmark_3m_date, alt_benchmark_index_code, iq_database)
    alt_benchmark_6m_price = get_index_price_as_on_date(alt_benchmark_6m_date, alt_benchmark_index_code, iq_database)
    alt_benchmark_1y_price = get_index_price_as_on_date(alt_benchmark_1y_date, alt_benchmark_index_code, iq_database)
    alt_benchmark_2y_price = get_index_price_as_on_date(alt_benchmark_2y_date, alt_benchmark_index_code, iq_database)
    alt_benchmark_3y_price = get_index_price_as_on_date(alt_benchmark_3y_date, alt_benchmark_index_code, iq_database)
    alt_benchmark_5y_price = get_index_price_as_on_date(alt_benchmark_5y_date, alt_benchmark_index_code, iq_database)

    alt_bm_date_power_1y = effective_end_date - alt_benchmark_1y_date
    alt_bm_date_power_2y = effective_end_date - alt_benchmark_2y_date
    alt_bm_date_power_3y = effective_end_date - alt_benchmark_3y_date
    alt_bm_date_power_5y = effective_end_date - alt_benchmark_5y_date

    alt_benchmark_perf_1m = round(((curr_price[0][0] / alt_benchmark_1m_price[0][0]) - 1), 4) if \
        nav_start_date <= alt_benchmark_1m_date else None
    alt_benchmark_perf_3m = round(((curr_price[0][0] / alt_benchmark_3m_price[0][0]) - 1), 4) if \
        nav_start_date <= alt_benchmark_3m_date else None
    alt_benchmark_perf_6m = round(((curr_price[0][0] / alt_benchmark_6m_price[0][0]) - 1), 4) if \
        nav_start_date <= alt_benchmark_6m_date else None
    alt_benchmark_perf_1y = round((((curr_price[0][0] / alt_benchmark_1y_price[0][0]) **
                                    (365 / alt_bm_date_power_1y.days)) - 1), 4) if nav_start_date <= \
                                                                                   alt_benchmark_1y_date else None
    alt_benchmark_perf_2y = round((((curr_price[0][0] / alt_benchmark_2y_price[0][0]) **
                                    (365 / alt_bm_date_power_2y.days)) - 1), 4) if nav_start_date <= \
                                                                                   alt_benchmark_2y_date else None
    alt_benchmark_perf_3y = round((((curr_price[0][0] / alt_benchmark_3y_price[0][0]) **
                                    (365 / alt_bm_date_power_3y.days)) - 1), 4) if nav_start_date <= \
                                                                                   alt_benchmark_3y_date else None
    alt_benchmark_perf_5y = round((((curr_price[0][0] / alt_benchmark_5y_price[0][0]) **
                                    (365 / alt_bm_date_power_5y.days)) - 1), 4) if nav_start_date <= \
                                                                                   alt_benchmark_5y_date else None
    # Calculation of alt_benchmark performance inception
    alt_benchmark_power_inception = effective_end_date - nav_start_date
    if alt_benchmark_power_inception.days > 365:
        alt_benchmark_perf_inception = round((((curr_price[0][0] / start_index_price) **
                                               (365 / alt_benchmark_power_inception.days)) - 1), 4)
    else:
        alt_benchmark_perf_inception = round(((curr_price[0][0] / start_index_price) - 1), 4)
    alt_benchmark_perf_data = {"index_code": alt_benchmark_index_code, "alt_benchmark_perf_1m": alt_benchmark_perf_1m,
                               "alt_benchmark_perf_3m": alt_benchmark_perf_3m,
                               "alt_benchmark_perf_6m": alt_benchmark_perf_6m,
                               "alt_benchmark_perf_1y": alt_benchmark_perf_1y,
                               "alt_benchmark_perf_2y": alt_benchmark_perf_2y,
                               "alt_benchmark_perf_3y": alt_benchmark_perf_3y,
                               "alt_benchmark_perf_5y": alt_benchmark_perf_5y,
                               "alt_benchmark_perf_inception": alt_benchmark_perf_inception}
    return alt_benchmark_perf_data


def table_records(fund_code, reporting_date, iq_database, app_database):
    previous_1m_end_date = get_1m_date(reporting_date)
    # Update isLatest for the previous month
    if previous_1m_end_date != '2018-10-31':
        update_islatest(fund_code, previous_1m_end_date, iq_database)
    fund_perf_data = get_fund_performance(fund_code, reporting_date, iq_database, app_database)
    benchmark_perf_data = get_benchmark_performance(fund_code, reporting_date, iq_database, app_database)
    alt_benchmark_perf_data = get_alt_benchmark_performance(fund_code, reporting_date, iq_database, app_database)
    final_data = {"fund_perf_data": fund_perf_data, "benchmark_perf_data": benchmark_perf_data,
                  "alt_benchmark_perf_data": alt_benchmark_perf_data}
    return final_data


try:
    db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    # db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', 'd0m#l1dZwhz!*9Iq0y1h'
    iq_db = 'iq'
    app_db = 'app'
    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db)
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db)
    fund_code_list = ['20840832']
    for fund_code in fund_code_list:
        nav_dates_list = get_nav_dates(fund_code, iq_database)
        first_date = nav_dates_list.pop(0)
        # nav_dates_list.pop(0)
        for reporting_date in nav_dates_list:
            final_data = table_records(fund_code, reporting_date, iq_database, app_database)
            put_fund_performance(final_data['fund_perf_data'], final_data['benchmark_perf_data'],
                                 final_data['alt_benchmark_perf_data'], iq_database)
            print(final_data)
    iq_database.commit()
    print("Commit success")
    iq_database.close()
    app_database.close()

except Exception as error:
    print("Exception raised :", error)
