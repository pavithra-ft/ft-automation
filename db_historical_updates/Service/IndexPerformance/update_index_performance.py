from datetime import datetime
from dateutil.relativedelta import relativedelta

from model.FundTablesModel import IndexPerformance
from Service.date_calculation import get_effective_start_end_date, get_1m_date, get_3m_date, get_6m_date, get_1y_date, \
    get_2y_date, get_3y_date, get_5y_date
from database.db_queries import get_index_price_as_on_date, get_index_start_date, get_start_price, get_mas_indices, \
    put_index_performance, get_index_start_price


def get_monthly_dates(index_code):
    start_date = get_index_start_date(index_code)
    current_date = datetime.today().date()
    monthly_dates = []
    while start_date < current_date:
        monthly_dates.append(start_date)
        start_date += relativedelta(months=1)
    return monthly_dates


def get_index_performance(index_code, month):
    start_date = get_index_start_date(index_code)
    start_index_price = get_index_start_price(start_date, index_code)
    effective_start_date, effective_end_date = get_effective_start_end_date(month)
    curr_price = get_index_price_as_on_date(effective_end_date, index_code)
    perf_1m_date = get_1m_date(month)
    perf_3m_date = get_3m_date(month)
    perf_6m_date = get_6m_date(month)
    perf_1y_date = get_1y_date(month)
    perf_2y_date = get_2y_date(month)
    perf_3y_date = get_3y_date(month)
    perf_5y_date = get_5y_date(month)
    perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, perf_3y, perf_5y = None, None, None, None, None, None, None
    # Calculation of 1 month index performance
    if start_date <= perf_1m_date:
        index_1m_price = get_index_price_as_on_date(perf_1m_date, index_code)
        perf_1m = round(((curr_price[0][0] / index_1m_price[0][0]) - 1), 4)
    # Calculation of 3 months index performance
    if start_date <= perf_3m_date:
        index_3m_price = get_index_price_as_on_date(perf_3m_date, index_code)
        perf_3m = round(((curr_price[0][0] / index_3m_price[0][0]) - 1), 4)
    # Calculation of 6 months index performance
    if start_date <= perf_6m_date:
        index_6m_price = get_index_price_as_on_date(perf_6m_date, index_code)
        perf_6m = round(((curr_price[0][0] / index_6m_price[0][0]) - 1), 4)
    # Calculation of 1 year index performance
    if start_date <= perf_1y_date:
        index_1y_price = get_index_price_as_on_date(perf_1y_date, index_code)
        date_power_1y = month - perf_1y_date
        perf_1y = round((((curr_price[0][0] / index_1y_price[0][0]) ** (365 / date_power_1y.days)) - 1), 4)
    # Calculation of 2 years index performance
    if start_date <= perf_2y_date:
        index_2y_price = get_index_price_as_on_date(perf_2y_date, index_code)
        date_power_2y = month - perf_2y_date
        perf_2y = round((((curr_price[0][0] / index_2y_price[0][0]) ** (365 / date_power_2y.days)) - 1), 4)
    # Calculation of 3 years index performance
    if start_date <= perf_3y_date:
        index_3y_price = get_index_price_as_on_date(perf_3y_date, index_code)
        date_power_3y = month - perf_3y_date
        perf_3y = round((((curr_price[0][0] / index_3y_price[0][0]) ** (365 / date_power_3y.days)) - 1), 4)
    # Calculation of 5 years index performance
    if start_date <= perf_5y_date:
        index_5y_price = get_index_price_as_on_date(perf_5y_date, index_code)
        date_power_5y = month - perf_5y_date
        perf_5y = round((((curr_price[0][0] / index_5y_price[0][0]) ** (365 / date_power_5y.days)) - 1), 4)
    # Calculation of index performance inception
    power_inception = month - start_date
    if power_inception.days >= 365:
        perf_inception = round((((curr_price[0][0] / start_index_price) ** (365 / power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((curr_price[0][0] / start_index_price) - 1), 4)
    index_data = IndexPerformance()
    index_data.set_index_code(index_code)
    index_data.set_perf_1m(perf_1m)
    index_data.set_perf_3m(perf_3m)
    index_data.set_perf_6m(perf_6m)
    index_data.set_perf_1y(perf_1y)
    index_data.set_perf_2y(perf_2y)
    index_data.set_perf_3y(perf_3y)
    index_data.set_perf_5y(perf_5y)
    index_data.set_perf_inception(perf_inception)
    index_data.set_reporting_date(effective_end_date)
    return index_data


def get_first_record(index_code, month):
    effective_start_date, effective_end_date = get_effective_start_end_date(month)
    inception_date = get_index_start_date(index_code)
    start_index_price = get_start_price(inception_date, index_code)
    curr_price = get_index_price_as_on_date(effective_end_date, index_code)
    # Calculation of Benchmark performance inception
    power_inception = effective_end_date - inception_date
    if power_inception.days >= 365:
        perf_inception = round((((curr_price[0][0] / start_index_price) ** (365 / power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((curr_price[0][0] / start_index_price) - 1), 4)
    index_data = IndexPerformance()
    index_data.set_index_code(index_code)
    index_data.set_perf_inception(perf_inception)
    index_data.set_reporting_date(effective_end_date)
    return index_data


try:
    index_code_list = get_mas_indices()
    for index_code in index_code_list:
        monthly_dates = get_monthly_dates(index_code)
        monthly_dates.pop(-1)
        for month in monthly_dates:
            if month is monthly_dates[0]:
                index_data = get_first_record(index_code, month)
                put_index_performance(index_data)
            else:
                index_data = get_index_performance(index_code, month)
                put_index_performance(index_data)
        print('Commit success :', index_code)

except Exception as error:
    print("Exception raised :", error)
