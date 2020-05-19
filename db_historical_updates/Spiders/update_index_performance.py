import MySQLdb
from envparse import env
from dateutil.relativedelta import relativedelta
from datetime import datetime

from Spiders.date_calculation import get_effective_start_end_date, get_1m_date, get_3m_date, get_6m_date, get_1y_date, \
    get_2y_date, get_3y_date, get_5y_date
from Spiders.db_actions import get_index_price_as_on_date, get_index_start_date, get_start_price, get_mas_indices, \
    put_index_performance


def get_monthly_dates(index_code, iq_database):
    start_date = get_index_start_date(index_code, iq_database)
    current_date = datetime.today().date()
    monthly_dates = []
    while start_date < current_date:
        monthly_dates.append(start_date)
        start_date += relativedelta(months=1)
    return monthly_dates


def get_performance(index_code, month, iq_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(month)
    curr_price = get_index_price_as_on_date(effective_end_date, index_code, iq_database)
    prev_1m_date = get_1m_date(month)
    prev_3m_date = get_3m_date(month)
    prev_6m_date = get_6m_date(month)
    prev_1y_date = get_1y_date(month)
    prev_2y_date = get_2y_date(month)
    prev_3y_date = get_3y_date(month)
    prev_5y_date = get_5y_date(month)
    perf_1m = None
    perf_3m = None
    perf_6m = None
    perf_1y = None
    perf_2y = None
    perf_3y = None
    perf_5y = None
    # Calculation of 1 month performance
    prev_1m_price = get_index_price_as_on_date(prev_1m_date, index_code, iq_database)
    if prev_1m_price:
        perf_1m = round(((curr_price[0][0] / prev_1m_price[0][0]) - 1), 4)
    # Calculation of 3 months performance
    prev_3m_price = get_index_price_as_on_date(prev_3m_date, index_code, iq_database)
    if prev_3m_price:
        perf_3m = round(((curr_price[0][0] / prev_3m_price[0][0]) - 1), 4)
    # Calculation of 6 months performance
    prev_6m_price = get_index_price_as_on_date(prev_6m_date, index_code, iq_database)
    if prev_6m_price:
        perf_6m = round(((curr_price[0][0] / prev_6m_price[0][0]) - 1), 4)
    # Calculation of 1 year performance
    prev_1y_price = get_index_price_as_on_date(prev_1y_date, index_code, iq_database)
    if prev_1y_price:
        date_power_1y = effective_end_date - prev_1y_date
        perf_1y = round((((curr_price[0][0] / prev_1y_price[0][0]) ** (365 / date_power_1y.days)) - 1), 4)
    # Calculation of 2 years performance
    prev_2y_price = get_index_price_as_on_date(prev_2y_date, index_code, iq_database)
    if prev_2y_price:
        date_power_2y = effective_end_date - prev_2y_date
        perf_2y = round((((curr_price[0][0] / prev_2y_price[0][0]) ** (365 / date_power_2y.days)) - 1), 4)
    # Calculation of 3 years performance
    prev_3y_price = get_index_price_as_on_date(prev_3y_date, index_code, iq_database)
    if prev_3y_price:
        date_power_3y = effective_end_date - prev_3y_date
        perf_3y = round((((curr_price[0][0] / prev_3y_price[0][0]) ** (365 / date_power_3y.days)) - 1), 4)
    # Calculation of 5 years performance
    prev_5y_price = get_index_price_as_on_date(prev_5y_date, index_code, iq_database)
    if prev_5y_price:
        date_power_5y = effective_end_date - prev_5y_date
        perf_5y = round((((curr_price[0][0] / prev_5y_price[0][0]) ** (365 / date_power_5y.days)) - 1), 4)
    # Calculation of Benchmark performance inception
    inception_date = get_index_start_date(index_code, iq_database)
    start_index_price = get_start_price(inception_date, index_code, iq_database)
    power_inception = effective_end_date - inception_date
    if power_inception.days >= 365:
        perf_inception = round((((curr_price[0][0] / start_index_price) ** (365 / power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((curr_price[0][0] / start_index_price) - 1), 4)
    final_data = {"index_code": index_code, "perf_1m": perf_1m, "perf_3m": perf_3m, "perf_6m": perf_6m,
                  "perf_1y": perf_1y, "perf_2y": perf_2y, "perf_3y": perf_3y, "perf_5y": perf_5y,
                  "perf_inception": perf_inception, "reporting_date": effective_end_date}
    print(final_data)
    return final_data


def get_first_record(index_code, month, database):
    effective_start_date, effective_end_date = get_effective_start_end_date(month)
    inception_date = get_index_start_date(index_code, database)
    start_index_price = get_start_price(inception_date, index_code, database)
    curr_price = get_index_price_as_on_date(effective_end_date, index_code, database)
    # Calculation of Benchmark performance inception
    power_inception = effective_end_date - inception_date
    if power_inception.days >= 365:
        perf_inception = round((((curr_price[0][0] / start_index_price) ** (365 / power_inception.days)) - 1), 4)
    else:
        perf_inception = round(((curr_price[0][0] / start_index_price) - 1), 4)
    final_data = {"index_code": index_code, "perf_1m": None, "perf_3m": None, "perf_6m": None,
                  "perf_1y": None, "perf_2y": None, "perf_3y": None, "perf_5y": None,
                  "perf_inception": perf_inception, "reporting_date": effective_end_date}
    print(final_data)
    return final_data


try:
    db_host, db_user, db_pass, db_name = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                         'd0m#l1dZwhz!*9Iq0y1h', 'iq'
    # db_host, db_user, db_pass, db_name = env('DB_HOST'), env('DB_USER'), env('DB_PASS'), env('DB_NAME')
    iq_database = MySQLdb.connect(db_host, db_user, db_pass, db_name, use_unicode=True, charset="utf8")
    index_code_list = get_mas_indices(iq_database)
    for index_code in index_code_list:
        monthly_dates = get_monthly_dates(index_code, iq_database)
        monthly_dates.pop(-1)
        for month in monthly_dates:
            if month is monthly_dates[0]:
                index_perf_data = get_first_record(index_code, month, iq_database)
                put_index_performance(index_perf_data, iq_database)
            else:
                index_perf_data = get_performance(index_code, month, iq_database)
                put_index_performance(index_perf_data, iq_database)
        iq_database.commit()
        print('Commit success :', index_code)
    iq_database.close()

except Exception as error:
    print("Exception raised :", error)
