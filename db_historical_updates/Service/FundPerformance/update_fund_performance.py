import datetime
import database.db_queries as query
import Service.date_calculation as date
from model.FundTablesModel import FundPerformance, BenchmarkPerformance, AlternateBenchmarkPerformance


def get_fund_performance(fund_code, reporting_date):
    perf_1m = perf_3m = perf_6m = perf_1y = perf_2y = perf_3y = perf_5y = None
    effective_start_date, effective_end_date = date.get_effective_start_end_date(reporting_date)

    prev_1m_end_date = date.get_1m_date(reporting_date)
    prev_3m_end_date = date.get_3m_date(reporting_date)
    prev_6m_end_date = date.get_6m_date(reporting_date)
    prev_1y_end_date = date.get_1y_date(reporting_date)
    prev_2y_end_date = date.get_2y_date(reporting_date)
    prev_3y_end_date = date.get_3y_date(reporting_date)
    prev_5y_end_date = date.get_5y_date(reporting_date)
    nav_start_date = query.get_nav_start_date(fund_code)

    fund_1m_nav = query.get_fund_nav(fund_code, prev_1m_end_date)
    fund_3m_nav = query.get_fund_nav(fund_code, prev_3m_end_date)
    fund_6m_nav = query.get_fund_nav(fund_code, prev_6m_end_date)
    fund_1y_nav = query.get_fund_nav(fund_code, prev_1y_end_date)
    fund_2y_nav = query.get_fund_nav(fund_code, prev_2y_end_date)
    fund_3y_nav = query.get_fund_nav(fund_code, prev_3y_end_date)
    fund_5y_nav = query.get_fund_nav(fund_code, prev_5y_end_date)
    fund_nav = query.get_fund_nav(fund_code, reporting_date)

    date_power_1y = effective_end_date - prev_1y_end_date
    date_power_2y = effective_end_date - prev_2y_end_date
    date_power_3y = effective_end_date - prev_3y_end_date
    date_power_5y = effective_end_date - prev_5y_end_date
    date_power_inception = effective_end_date - nav_start_date

    if fund_1m_nav:
        if nav_start_date <= prev_1m_end_date:
            perf_1m = round(((float(fund_nav[0][0]) / float(fund_1m_nav[0][0])) - 1), 4)
    if fund_3m_nav:
        if nav_start_date <= prev_3m_end_date:
            perf_3m = round(((float(fund_nav[0][0]) / float(fund_3m_nav[0][0])) - 1), 4)
    if fund_6m_nav:
        if nav_start_date <= prev_6m_end_date:
            perf_6m = round(((float(fund_nav[0][0]) / float(fund_6m_nav[0][0])) - 1), 4)
    if fund_1y_nav:
        if nav_start_date <= prev_1y_end_date:
            perf_1y = round((((float(fund_nav[0][0]) / float(fund_1y_nav[0][0])) ** (365 / date_power_1y.days)) - 1), 4)
    if fund_2y_nav:
        if nav_start_date <= prev_2y_end_date:
            perf_2y = round((((float(fund_nav[0][0]) / float(fund_2y_nav[0][0])) ** (365 / date_power_2y.days)) - 1), 4)
    if fund_3y_nav:
        if nav_start_date <= prev_3y_end_date:
            perf_3y = round((((float(fund_nav[0][0]) / float(fund_3y_nav[0][0])) ** (365 / date_power_3y.days)) - 1), 4)
    if fund_5y_nav:
        if nav_start_date <= prev_5y_end_date:
            perf_5y = round((((float(fund_nav[0][0]) / float(fund_5y_nav[0][0])) ** (365 / date_power_5y.days)) - 1), 4)

    if date_power_inception.days > 365:
        perf_inception = round((((float(fund_nav[0][0]) / 1) ** (365 / date_power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((float(fund_nav[0][0]) / 1) - 1), 4)
    fund_perf_data = FundPerformance()
    fund_perf_data.set_fund_code(fund_code)
    fund_perf_data.set_investment_style_type_code(query.get_investment_style(fund_code))
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
    return fund_perf_data


def get_benchmark_perf_month(index_code, nav_start_date, curr_price, date):
    perf_mon = None
    price_mon = query.get_index_price_as_on_date(date, index_code)
    if price_mon:
        if nav_start_date <= date:
            perf_mon = round(((curr_price / float(price_mon[-1][0])) - 1), 4)
    return perf_mon


def get_benchmark_perf_year(effective_end_date, index_code, nav_start_date, curr_price, date):
    perf_yr = None
    price_yr = query.get_index_price_as_on_date(date, index_code)
    date_power_yr = effective_end_date - date
    if price_yr:
        if nav_start_date <= date:
            perf_yr = round((((curr_price / float(price_yr[-1][0])) ** (365 / date_power_yr.days)) - 1), 4)
    return perf_yr


def get_benchmark_perf_inception(effective_end_date, index_code, nav_start_date, curr_price):
    start_index_price = query.get_start_price(nav_start_date, index_code)
    bm_power_inception = effective_end_date - nav_start_date
    if bm_power_inception.days > 365:
        bm_perf_inception = round((((curr_price / start_index_price) ** (365 / bm_power_inception.days)) - 1), 4)
    else:
        bm_perf_inception = round(((curr_price / start_index_price) - 1), 4)
    return bm_perf_inception


def get_benchmark_performance(fund_code, reporting_date):
    effective_start_date, effective_end_date = date.get_effective_start_end_date(reporting_date)
    index_code = query.get_benchmark_index(fund_code)
    curr_price = float(query.get_index_price_as_on_date(effective_end_date, index_code)[-1][0])

    bm_date_1m = date.get_1m_date(reporting_date)
    bm_date_3m = date.get_3m_date(reporting_date)
    bm_date_6m = date.get_6m_date(reporting_date)
    bm_date_1y = date.get_1y_date(reporting_date)
    bm_date_2y = date.get_2y_date(reporting_date)
    bm_date_3y = date.get_3y_date(reporting_date)
    bm_date_5y = date.get_5y_date(reporting_date)
    nav_start_date = query.get_nav_start_date(fund_code)

    bm_perf_data = BenchmarkPerformance()
    bm_perf_data.set_benchmark_index_code(index_code)
    bm_perf_data.set_benchmark_perf_1m(get_benchmark_perf_month(index_code, nav_start_date, curr_price, bm_date_1m))
    bm_perf_data.set_benchmark_perf_3m(get_benchmark_perf_month(index_code, nav_start_date, curr_price, bm_date_3m))
    bm_perf_data.set_benchmark_perf_6m(get_benchmark_perf_month(index_code, nav_start_date, curr_price, bm_date_6m))
    bm_perf_data.set_benchmark_perf_1y(get_benchmark_perf_year(effective_end_date, index_code, nav_start_date,
                                                               curr_price, bm_date_1y))
    bm_perf_data.set_benchmark_perf_2y(get_benchmark_perf_year(effective_end_date, index_code, nav_start_date,
                                                               curr_price, bm_date_2y))
    bm_perf_data.set_benchmark_perf_3y(get_benchmark_perf_year(effective_end_date, index_code, nav_start_date,
                                                               curr_price, bm_date_3y))
    bm_perf_data.set_benchmark_perf_5y(get_benchmark_perf_year(effective_end_date, index_code, nav_start_date,
                                                               curr_price, bm_date_5y))
    bm_perf_data.set_benchmark_perf_inception(get_benchmark_perf_inception(effective_end_date, index_code,
                                                                           nav_start_date, curr_price))
    return bm_perf_data


def get_alt_benchmark_performance(fund_code, reporting_date):
    effective_start_date, effective_end_date = date.get_effective_start_end_date(reporting_date)
    index_code = query.get_alt_benchmark_index(fund_code)
    curr_price = float(query.get_index_price_as_on_date(effective_end_date, index_code)[-1][0])

    alt_1m_date = date.get_1m_date(reporting_date)
    alt_3m_date = date.get_3m_date(reporting_date)
    alt_6m_date = date.get_6m_date(reporting_date)
    alt_1y_date = date.get_1y_date(reporting_date)
    alt_2y_date = date.get_2y_date(reporting_date)
    alt_3y_date = date.get_3y_date(reporting_date)
    alt_5y_date = date.get_5y_date(reporting_date)
    nav_start_date = query.get_nav_start_date(fund_code)

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


def table_records(fund_code, reporting_date):
    previous_1m_end_date = date.get_1m_date(reporting_date)
    query.update_islatest(fund_code, previous_1m_end_date)
    fund_perf_data = get_fund_performance(fund_code, reporting_date)
    benchmark_perf_data = get_benchmark_performance(fund_code, reporting_date)
    alt_benchmark_perf_data = get_alt_benchmark_performance(fund_code, reporting_date)
    final_data = {"fund_perf_data": fund_perf_data, "benchmark_perf_data": benchmark_perf_data,
                  "alt_benchmark_perf_data": alt_benchmark_perf_data}
    return final_data


try:
    fund_code_list = []
    for fund_code in fund_code_list:
        nav_dates_list = query.get_nav_dates(fund_code)
        first_date = nav_dates_list.pop(0)
        for reporting_date in nav_dates_list:
            final_data = table_records(fund_code, reporting_date)
            query.put_fund_performance(final_data['fund_perf_data'], final_data['benchmark_perf_data'],
                                       final_data['alt_benchmark_perf_data'])

except Exception as error:
    print("Exception raised :", error)
