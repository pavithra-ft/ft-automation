import database.db_queries as query
import Service.date_calculation as date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from model.FundTablesModel import IndexPerformance


def get_monthly_dates(index_code):
    start_date = query.get_index_start_date(index_code)
    current_date = datetime.today().date()
    monthly_dates = []
    while start_date < current_date:
        monthly_dates.append(start_date)
        start_date += relativedelta(months=1)
    return monthly_dates


def get_index_performance(index_code, month):
    start_date = query.get_index_start_date(index_code)
    start_index_price = query.get_index_start_price(index_code, start_date)
    effective_start_date, effective_end_date = date.get_effective_start_end_date(month)
    curr_price = float(query.get_index_price_as_on_date(effective_end_date, index_code)[-1][0])
    perf_1m_date = date.get_1m_date(month)
    perf_3m_date = date.get_3m_date(month)
    perf_6m_date = date.get_6m_date(month)
    perf_1y_date = date.get_1y_date(month)
    perf_2y_date = date.get_2y_date(month)
    perf_3y_date = date.get_3y_date(month)
    perf_5y_date = date.get_5y_date(month)
    perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, perf_3y, perf_5y = None, None, None, None, None, None, None
    # Calculation of 1 month index performance
    if start_date <= perf_1m_date:
        index_1m_price = query.get_index_price_as_on_date(perf_1m_date, index_code)
        perf_1m = round(((curr_price / float(index_1m_price[-1][0])) - 1), 4)
    # Calculation of 3 months index performance
    if start_date <= perf_3m_date:
        index_3m_price = query.get_index_price_as_on_date(perf_3m_date, index_code)
        perf_3m = round(((curr_price / float(index_3m_price[-1][0])) - 1), 4)
    # Calculation of 6 months index performance
    if start_date <= perf_6m_date:
        index_6m_price = query.get_index_price_as_on_date(perf_6m_date, index_code)
        perf_6m = round(((curr_price / float(index_6m_price[-1][0])) - 1), 4)
    # Calculation of 1 year index performance
    if start_date <= perf_1y_date:
        index_1y_price = query.get_index_price_as_on_date(perf_1y_date, index_code)
        date_power_1y = month - perf_1y_date
        perf_1y = round((((curr_price / float(index_1y_price[-1][0])) ** (365 / date_power_1y.days)) - 1), 4)
    # Calculation of 2 years index performance
    if start_date <= perf_2y_date:
        index_2y_price = query.get_index_price_as_on_date(perf_2y_date, index_code)
        date_power_2y = month - perf_2y_date
        perf_2y = round((((curr_price / float(index_2y_price[-1][0])) ** (365 / date_power_2y.days)) - 1), 4)
    # Calculation of 3 years index performance
    if start_date <= perf_3y_date:
        index_3y_price = query.get_index_price_as_on_date(perf_3y_date, index_code)
        date_power_3y = month - perf_3y_date
        perf_3y = round((((curr_price / float(index_3y_price[-1][0])) ** (365 / date_power_3y.days)) - 1), 4)
    # Calculation of 5 years index performance
    if start_date <= perf_5y_date:
        index_5y_price = query.get_index_price_as_on_date(perf_5y_date, index_code)
        date_power_5y = month - perf_5y_date
        perf_5y = round((((curr_price / float(index_5y_price[-1][0])) ** (365 / date_power_5y.days)) - 1), 4)
    # Calculation of index performance inception
    power_inception = month - start_date
    if power_inception.days >= 365:
        perf_inception = round((((curr_price / start_index_price) ** (365 / power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((curr_price / start_index_price) - 1), 4)
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
    effective_start_date, effective_end_date = date.get_effective_start_end_date(month)
    inception_date = query.get_index_start_date(index_code)
    start_index_price = query.get_start_price(inception_date, index_code)
    curr_price = float(query.get_index_price_as_on_date(effective_end_date, index_code)[-1][0])
    # Calculation of Benchmark performance inception
    power_inception = effective_end_date - inception_date
    if power_inception.days >= 365:
        perf_inception = round((((curr_price / start_index_price) ** (365 / power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((curr_price / start_index_price) - 1), 4)
    index_data = IndexPerformance()
    index_data.set_index_code(index_code)
    index_data.set_perf_inception(perf_inception)
    index_data.set_reporting_date(effective_end_date)
    return index_data


try:
    index_code_list = []
    for index_code in index_code_list:
        monthly_dates = get_monthly_dates(index_code)
        monthly_dates.pop(-1)
        for month in monthly_dates:
            if month is monthly_dates[0]:
                index_data = get_first_record(index_code, month)
                query.put_index_performance(index_data)
            else:
                index_data = get_index_performance(index_code, month)
                query.put_index_performance(index_data)
        print('Commit success :', index_code)

except Exception as error:
    print("Exception raised :", error)
