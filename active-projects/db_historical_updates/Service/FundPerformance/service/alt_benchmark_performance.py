import Service.date_calculation as date
from database.db_queries import get_reporting_dates, get_nav_start_date, get_start_price, \
    get_index_price_as_on_date, get_alt_benchmark_index, put_alt_benchmark_performance, iq_session
from model.FundTablesModel import AlternateBenchmarkPerformance


def get_benchmark_perf_month(index_code, nav_start_date, curr_price, date):
    perf_mon = None
    price_mon = get_index_price_as_on_date(date, index_code)
    if price_mon:
        if nav_start_date <= date:
            perf_mon = round(((curr_price / float(price_mon[-1][0])) - 1), 4)
    return perf_mon


def get_benchmark_perf_year(effective_end_date, index_code, nav_start_date, curr_price, date):
    perf_yr = None
    price_yr = get_index_price_as_on_date(date, index_code)
    date_power_yr = effective_end_date - date
    if price_yr:
        if nav_start_date <= date:
            perf_yr = round((((curr_price / float(price_yr[-1][0])) ** (365 / date_power_yr.days)) - 1), 4)
    return perf_yr


def get_benchmark_perf_inception(effective_end_date, index_code, nav_start_date, curr_price):
    start_index_price = get_start_price(nav_start_date, index_code)
    bm_power_inception = effective_end_date - nav_start_date
    if bm_power_inception.days > 365:
        bm_perf_inception = round((((curr_price / start_index_price) ** (365 / bm_power_inception.days)) - 1), 4)
    else:
        bm_perf_inception = round(((curr_price / start_index_price) - 1), 4)
    return bm_perf_inception


def calc_alt_benchmark_performance(fund_code, reporting_date):
    effective_start_date, effective_end_date = date.get_effective_start_end_date(reporting_date)
    index_code = get_alt_benchmark_index(fund_code)
    curr_price = float(get_index_price_as_on_date(effective_end_date, index_code)[-1][0])

    alt_1m_date = date.get_1m_date(reporting_date)
    alt_3m_date = date.get_3m_date(reporting_date)
    alt_6m_date = date.get_6m_date(reporting_date)
    alt_1y_date = date.get_1y_date(reporting_date)
    alt_2y_date = date.get_2y_date(reporting_date)
    alt_3y_date = date.get_3y_date(reporting_date)
    alt_5y_date = date.get_5y_date(reporting_date)
    nav_start_date = get_nav_start_date(fund_code)

    alt_bm_data = AlternateBenchmarkPerformance()
    alt_bm_data.set_alt_benchmark_index_code(index_code)
    alt_bm_data.set_alt_benchmark_perf_1m(get_benchmark_perf_month(index_code, nav_start_date, curr_price, alt_1m_date))
    alt_bm_data.set_alt_benchmark_perf_3m(get_benchmark_perf_month(index_code, nav_start_date, curr_price, alt_3m_date))
    alt_bm_data.set_alt_benchmark_perf_6m(get_benchmark_perf_month(index_code, nav_start_date, curr_price, alt_6m_date))
    alt_bm_data.set_alt_benchmark_perf_1y(get_benchmark_perf_year(effective_end_date, index_code, nav_start_date,
                                                                  curr_price, alt_1y_date))
    alt_bm_data.set_alt_benchmark_perf_2y(get_benchmark_perf_year(effective_end_date, index_code, nav_start_date,
                                                                  curr_price, alt_2y_date))
    alt_bm_data.set_alt_benchmark_perf_3y(get_benchmark_perf_year(effective_end_date, index_code, nav_start_date,
                                                                  curr_price, alt_3y_date))
    alt_bm_data.set_alt_benchmark_perf_5y(get_benchmark_perf_year(effective_end_date, index_code, nav_start_date,
                                                                  curr_price, alt_5y_date))
    alt_bm_data.set_alt_benchmark_perf_inception(get_benchmark_perf_inception(effective_end_date, index_code,
                                                                              nav_start_date, curr_price))
    return alt_bm_data


def get_alt_benchmark_performance(fund_code_list):
    for fund_code in fund_code_list:
        reporting_dates_list = get_reporting_dates(fund_code)
        reporting_dates_list.pop(0)
        for reporting_date in reporting_dates_list:
            alt_benchmark_perf_data = calc_alt_benchmark_performance(fund_code, reporting_date)
            try:
                put_alt_benchmark_performance(fund_code, reporting_date, alt_benchmark_perf_data)
                iq_session.commit()
            except Exception as error:
                iq_session.rollback()
                print("Exception raised :", error)
            finally:
                iq_session.close()
