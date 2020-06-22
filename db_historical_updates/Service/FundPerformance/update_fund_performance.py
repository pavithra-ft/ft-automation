import datetime

from model.FundTablesModel import FundPerformance, BenchmarkPerformance, AlternateBenchmarkPerformance
from Service.date_calculation import get_effective_start_end_date, get_1m_date, get_3m_date, get_6m_date, get_1y_date, \
    get_2y_date, get_3y_date, get_5y_date
from database.db_queries import get_benchmark_index, get_index_price_as_on_date, get_alt_benchmark_index, \
    get_fund_nav, get_nav_start_date, get_start_price, put_fund_performance, update_islatest, get_nav_dates, \
    get_investment_style


def get_fund_performance(fund_code, reporting_date):
    perf_1m = perf_3m = perf_6m = perf_1y = perf_2y = perf_3y = perf_5y = None
    effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)

    prev_1m_end_date = get_1m_date(reporting_date)
    prev_3m_end_date = get_3m_date(reporting_date)
    prev_6m_end_date = get_6m_date(reporting_date)
    prev_1y_end_date = get_1y_date(reporting_date)
    prev_2y_end_date = get_2y_date(reporting_date)
    prev_3y_end_date = get_3y_date(reporting_date)
    prev_5y_end_date = get_5y_date(reporting_date)
    nav_start_date = get_nav_start_date(fund_code)

    fund_1m_nav = get_fund_nav(fund_code, prev_1m_end_date)
    fund_3m_nav = get_fund_nav(fund_code, prev_3m_end_date)
    fund_6m_nav = get_fund_nav(fund_code, prev_6m_end_date)
    fund_1y_nav = get_fund_nav(fund_code, prev_1y_end_date)
    fund_2y_nav = get_fund_nav(fund_code, prev_2y_end_date)
    fund_3y_nav = get_fund_nav(fund_code, prev_3y_end_date)
    fund_5y_nav = get_fund_nav(fund_code, prev_5y_end_date)
    fund_nav = get_fund_nav(fund_code, reporting_date)

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
    fund_perf_data.set_investment_style_type_code(get_investment_style(fund_code))
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


def get_benchmark_performance(fund_code, reporting_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)
    benchmark_index_code = get_benchmark_index(fund_code)

    bm_1m_date = get_1m_date(reporting_date)
    bm_3m_date = get_3m_date(reporting_date)
    bm_6m_date = get_6m_date(reporting_date)
    bm_1y_date = get_1y_date(reporting_date)
    bm_2y_date = get_2y_date(reporting_date)
    bm_3y_date = get_3y_date(reporting_date)
    bm_5y_date = get_5y_date(reporting_date)
    nav_start_date = get_nav_start_date(fund_code)

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


def get_alt_benchmark_performance(fund_code, reporting_date):
    effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)
    alt_bm_index_code = get_alt_benchmark_index(fund_code)

    alt_bm_1m_date = get_1m_date(reporting_date)
    alt_bm_3m_date = get_3m_date(reporting_date)
    alt_bm_6m_date = get_6m_date(reporting_date)
    alt_bm_1y_date = get_1y_date(reporting_date)
    alt_bm_2y_date = get_2y_date(reporting_date)
    alt_bm_3y_date = get_3y_date(reporting_date)
    alt_bm_5y_date = get_5y_date(reporting_date)
    nav_start_date = get_nav_start_date(fund_code)

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


def table_records(fund_code, reporting_date):
    previous_1m_end_date = get_1m_date(reporting_date)
    update_islatest(fund_code, previous_1m_end_date)
    fund_perf_data = get_fund_performance(fund_code, reporting_date)
    benchmark_perf_data = get_benchmark_performance(fund_code, reporting_date)
    alt_benchmark_perf_data = get_alt_benchmark_performance(fund_code, reporting_date)
    final_data = {"fund_perf_data": fund_perf_data, "benchmark_perf_data": benchmark_perf_data,
                  "alt_benchmark_perf_data": alt_benchmark_perf_data}
    return final_data


try:
    fund_code_list = []
    for fund_code in fund_code_list:
        nav_dates_list = get_nav_dates(fund_code)
        first_date = nav_dates_list.pop(0)
        for reporting_date in nav_dates_list:
            final_data = table_records(fund_code, reporting_date)
            put_fund_performance(final_data['fund_perf_data'], final_data['benchmark_perf_data'],
                                 final_data['alt_benchmark_perf_data'])
            print(final_data)

except Exception as error:
    print("Exception raised :", error)
