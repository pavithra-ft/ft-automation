import MySQLdb
from dateutil.relativedelta import relativedelta
from envparse import env
import datetime
import calendar

from Spiders.db_actions import get_benchmark_index, get_index_price_as_on_date, get_alt_benchmark_index, get_fund_nav, \
    get_nav_start_date, get_start_price, put_fund_performance, update_islatest


def get_nav_dates(fund_code):
    fund_bm_nav_cursor = iq_database.cursor()
    fund_bm_nav_query = "SELECT effective_end_date from iq.fund_benchmark_nav where fund_code = '" \
                        + fund_code + "' order by effective_end_date"
    fund_bm_nav_cursor.execute(fund_bm_nav_query)
    nav_dates = fund_bm_nav_cursor.fetchall()
    nav_dates_list = []
    for date in nav_dates:
        nav_dates_list.append(date[0])
    return nav_dates_list


def get_effective_start_end_date(reporting_date):
    effective_start_date = reporting_date.replace(day=1)
    effective_end_date = reporting_date.replace(
        day=calendar.monthrange(effective_start_date.year, effective_start_date.month)[1])
    return effective_start_date, effective_end_date


def get_1m_date(reporting_date):
    previous_1m_date = reporting_date - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1])
    return previous_1m_end_date


def get_3m_date(reporting_date):
    previous_3m_date = reporting_date - relativedelta(months=3)
    previous_3m_end_date = previous_3m_date.replace(day=calendar.monthrange(previous_3m_date.year,
                                                                            previous_3m_date.month)[1])
    return previous_3m_end_date


def get_6m_date(reporting_date):
    previous_6m_date = reporting_date - relativedelta(months=6)
    previous_6m_end_date = previous_6m_date.replace(day=calendar.monthrange(previous_6m_date.year,
                                                                            previous_6m_date.month)[1])
    return previous_6m_end_date


def get_1y_date(reporting_date):
    previous_1y_date = reporting_date - relativedelta(years=1)
    previous_1y_end_date = (previous_1y_date.replace(day=calendar.monthrange(previous_1y_date.year,
                                                                             previous_1y_date.month)[1]))
    return previous_1y_end_date


def get_2y_date(reporting_date):
    previous_2y_date = reporting_date - relativedelta(years=2)
    previous_2y_end_date = previous_2y_date.replace(day=calendar.monthrange(previous_2y_date.year,
                                                                            previous_2y_date.month)[1])
    return previous_2y_end_date


def get_3y_date(reporting_date):
    previous_3y_date = reporting_date - relativedelta(years=3)
    previous_3y_end_date = previous_3y_date.replace(day=calendar.monthrange(previous_3y_date.year,
                                                                            previous_3y_date.month)[1])
    return previous_3y_end_date


def get_5y_date(reporting_date):
    previous_5y_date = reporting_date - relativedelta(years=5)
    previous_5y_end_date = previous_5y_date.replace(day=calendar.monthrange(previous_5y_date.year,
                                                                            previous_5y_date.month)[1])
    return previous_5y_end_date


def get_fund_performance(fund_code, reporting_date, iq_database, app_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)
    current_aum = None
    no_of_clients = None
    market_cap_type_code = None
    portfolio_equity_allocation = None
    portfolio_cash_allocation = None
    portfolio_asset_allocation = None
    portfolio_other_allocations = None
    # Calculation of Fund NAV
    prev_1m_end_date = get_1m_date(reporting_date)
    prev_3m_end_date = get_3m_date(reporting_date)
    prev_6m_end_date = get_6m_date(reporting_date)
    prev_1y_end_date = get_1y_date(reporting_date)
    prev_2y_end_date = get_2y_date(reporting_date)
    prev_3y_end_date = get_3y_date(reporting_date)
    prev_5y_end_date = get_5y_date(reporting_date)
    perf_1m = None
    perf_3m = None
    perf_6m = None
    perf_1y = None
    perf_2y = None
    perf_3y = None
    perf_5y = None
    fund_1m_nav = get_fund_nav(fund_code, prev_1m_end_date, iq_database)
    # Calculation of Fund nav
    fund_nav = get_fund_nav(fund_code, effective_end_date, iq_database)
    # Calculation of 1 month Fund performance
    if fund_1m_nav:
        perf_1m = round(((fund_nav[0][0] / fund_1m_nav[0][0]) - 1), 4)
    # Calculation of 3 months Fund performance
    fund_3m_nav = get_fund_nav(fund_code, prev_3m_end_date, iq_database)
    if fund_3m_nav:
        perf_3m = round(((fund_nav[0][0] / fund_3m_nav[0][0]) - 1), 4)
    # Calculation of 6 months Fund performance
    fund_6m_nav = get_fund_nav(fund_code, prev_6m_end_date, iq_database)
    if fund_6m_nav:
        perf_6m = round(((fund_nav[0][0] / fund_6m_nav[0][0]) - 1), 4)
    # Calculation of 1 year Fund performance
    fund_1y_nav = get_fund_nav(fund_code, prev_1y_end_date, iq_database)
    if fund_1y_nav:
        date_power_1y = effective_end_date - prev_1y_end_date
        perf_1y = round((((fund_nav[0][0] / fund_1y_nav[0][0]) ** (365 / date_power_1y.days)) - 1), 4)
    # Calculation of 2 years Fund performance
    fund_2y_nav = get_fund_nav(fund_code, prev_2y_end_date, iq_database)
    if fund_2y_nav:
        date_power_2y = effective_end_date - prev_2y_end_date
        perf_2y = round((((fund_nav[0][0] / fund_2y_nav[0][0]) ** (365 / date_power_2y.days)) - 1), 4)
    # Calculation of 3 years Fund performance
    fund_3y_nav = get_fund_nav(fund_code, prev_3y_end_date, iq_database)
    if fund_3y_nav:
        date_power_3y = effective_end_date - prev_3y_end_date
        perf_3y = round((((fund_nav[0][0] / fund_3y_nav[0][0]) ** (365 / date_power_3y.days)) - 1), 4)
    # Calculation of 5 years Fund performance
    fund_5y_nav = get_fund_nav(fund_code, prev_5y_end_date, iq_database)
    if fund_5y_nav:
        date_power_5y = effective_end_date - prev_5y_end_date
        perf_5y = round((((fund_nav[0][0] / fund_5y_nav[0][0]) ** (365 / date_power_5y.days)) - 1), 4)
    # Calculation of Fund performance inception
    nav_start_date = get_nav_start_date(fund_code, app_database)
    date_power_inception = effective_end_date - nav_start_date
    if date_power_inception.days >= 365:
        perf_inception = round((((fund_nav[0][0] / 1) ** (365 / date_power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((fund_nav[0][0] / 1) - 1), 4)
    # Other fields
    isLatest = '1'
    created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = "ft-automation"
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
    update_islatest(fund_code, previous_1m_end_date, iq_database)

    fund_perf_data = get_fund_performance(fund_code, reporting_date, iq_database, app_database)
    benchmark_perf_data = get_benchmark_performance(fund_code, reporting_date, iq_database, app_database)
    alt_benchmark_perf_data = get_alt_benchmark_performance(fund_code, reporting_date, iq_database, app_database)
    final_data = {"fund_perf_data": fund_perf_data, "benchmark_perf_data": benchmark_perf_data,
                  "alt_benchmark_perf_data": alt_benchmark_perf_data}
    return final_data


try:
    # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                'd0m#l1dZwhz!*9Iq0y1h'
    iq_db = 'iq'
    app_db = 'app'

    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db)
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db)
    fund_code_list = ['72966297']
    for fund_code in fund_code_list:
        nav_dates_list = get_nav_dates(fund_code)
        first_date = nav_dates_list.pop(0)
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