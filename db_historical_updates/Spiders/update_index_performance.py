import MySQLdb
from envparse import env
import calendar
from pandas.tseries.offsets import BMonthEnd
from dateutil.relativedelta import relativedelta
from datetime import datetime


def get_effective_start_end_date(start_date):
    # Calculation of effective start date and end date
    start_date = datetime.strptime(str(start_date), '%Y-%m-%d').date()
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


def get_index_code(database):
    index_cursor = database.cursor()
    index_query = "SELECT distinct index_code FROM iq.index_prices"
    index_cursor.execute(index_query)
    index_details = index_cursor.fetchall()
    index_code_list = []
    for code in index_details:
        index_code_list.append(code[0])
    return index_code_list


def get_start_date(index_code, database):
    start_date_cursor = database.cursor()
    start_date_query = "SELECT index_price_as_on_date FROM iq.index_prices where index_code ='" + index_code \
                       + "' order    by index_price_as_on_date asc limit 1"
    start_date_cursor.execute(start_date_query)
    start_date_details = start_date_cursor.fetchall()
    start_date = start_date_details[0][0]
    return start_date


def get_start_price(start_date, index_code, database):
    start_nav_cursor = database.cursor()
    start_index_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                              + "' and index_price_as_on_date = '" + str(start_date) + "'"
    start_nav_cursor.execute(start_index_price_query)
    start_index_price_details = start_nav_cursor.fetchall()
    start_index_price = start_index_price_details[0][0]
    return start_index_price


def get_monthly_dates(index_code, database):
    start_date = get_start_date(index_code, database)
    current_date = datetime.today().date()
    monthly_dates = []
    while start_date < current_date:
        monthly_dates.append(start_date)
        start_date += relativedelta(months=1)
    return monthly_dates


def get_curr_price(month, index_code, database):
    curr_price_cursor = database.cursor()
    curr_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                       + "' and year(ip.index_price_as_on_date) = year('" + str(month) \
                       + "') and month(ip.index_price_as_on_date) = month('" + str(month) \
                       + "') order by ip.index_price_as_on_date desc limit 1"
    curr_price_cursor.execute(curr_price_query)
    curr_price_details = curr_price_cursor.fetchall()
    curr_price = curr_price_details[0][0]
    return curr_price


def get_prev_1m_price(prev_1m_date, index_code, database):
    prev_1m_price_cursor = database.cursor()
    prev_1m_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                          + "' and year(ip.index_price_as_on_date) = year('" + str(prev_1m_date) \
                          + "') and month(ip.index_price_as_on_date) = month('" + str(prev_1m_date) \
                          + "') order by ip.index_price_as_on_date desc limit 1"
    prev_1m_price_cursor.execute(prev_1m_price_query)
    prev_1m_price = prev_1m_price_cursor.fetchall()
    return prev_1m_price


def get_prev_3m_price(prev_3m_date, index_code, database):
    prev_3m_price_cursor = database.cursor()
    prev_3m_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                          + "' and year(ip.index_price_as_on_date) = year('" + str(prev_3m_date) \
                          + "') and month(ip.index_price_as_on_date) = month('" + str(prev_3m_date) \
                          + "') order by ip.index_price_as_on_date desc limit 1"
    prev_3m_price_cursor.execute(prev_3m_price_query)
    prev_3m_price = prev_3m_price_cursor.fetchall()
    return prev_3m_price


def get_prev_6m_price(prev_6m_date, index_code, database):
    prev_6m_price_cursor = database.cursor()
    prev_6m_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                          + "' and year(ip.index_price_as_on_date) = year('" + str(prev_6m_date) \
                          + "') and month(ip.index_price_as_on_date) = month('" + str(prev_6m_date) \
                          + "') order by ip.index_price_as_on_date desc limit 1"
    prev_6m_price_cursor.execute(prev_6m_price_query)
    prev_6m_price = prev_6m_price_cursor.fetchall()
    return prev_6m_price


def get_prev_1y_price(prev_1y_date, index_code, database):
    prev_1y_price_cursor = database.cursor()
    prev_1y_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                          + "' and year(ip.index_price_as_on_date) = year('" + str(prev_1y_date) \
                          + "') and month(ip.index_price_as_on_date) = month('" + str(prev_1y_date) \
                          + "') order by ip.index_price_as_on_date desc limit 1"
    prev_1y_price_cursor.execute(prev_1y_price_query)
    prev_1y_price = prev_1y_price_cursor.fetchall()
    return prev_1y_price


def get_prev_2y_price(prev_2y_date, index_code, database):
    prev_2y_price_cursor = database.cursor()
    prev_2y_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                          + "' and year(ip.index_price_as_on_date) = year('" + str(prev_2y_date) \
                          + "') and month(ip.index_price_as_on_date) = month('" + str(prev_2y_date) \
                          + "') order by ip.index_price_as_on_date desc limit 1"
    prev_2y_price_cursor.execute(prev_2y_price_query)
    prev_2y_price = prev_2y_price_cursor.fetchall()
    return prev_2y_price


def get_prev_3y_price(prev_3y_date, index_code, database):
    prev_3y_price_cursor = database.cursor()
    prev_3y_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                          + "' and year(ip.index_price_as_on_date) = year('" + str(prev_3y_date) \
                          + "') and month(ip.index_price_as_on_date) = month('" + str(prev_3y_date) \
                          + "') order by ip.index_price_as_on_date desc limit 1"
    prev_3y_price_cursor.execute(prev_3y_price_query)
    prev_3y_price = prev_3y_price_cursor.fetchall()
    return prev_3y_price


def get_prev_5y_price(prev_5y_date, index_code, database):
    prev_5y_price_cursor = database.cursor()
    prev_5y_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                          + "' and year(ip.index_price_as_on_date) = year('" + str(prev_5y_date) \
                          + "') and month(ip.index_price_as_on_date) = month('" + str(prev_5y_date) \
                          + "') order by ip.index_price_as_on_date desc limit 1"
    prev_5y_price_cursor.execute(prev_5y_price_query)
    prev_5y_price = prev_5y_price_cursor.fetchall()
    return prev_5y_price


def get_performance(index_code, month, database):
    effective_start_date, effective_end_date = get_effective_start_end_date(month)
    curr_price = get_curr_price(effective_end_date, index_code, database)
    # Calculation of 1 month performance
    prev_1m_date = get_1m_date(month)
    prev_1m = get_prev_1m_price(prev_1m_date, index_code, database)
    if len(prev_1m) == 0:
        perf_1m = None
    else:
        prev_1m_price = prev_1m[0][0]
        perf_1m = round(((curr_price / prev_1m_price) - 1), 4)
    # Calculation of 3 months performance
    prev_3m_date = get_3m_date(month)
    prev_3m = get_prev_3m_price(prev_3m_date, index_code, database)
    if len(prev_3m) == 0:
        perf_3m = None
    else:
        prev_3m_price = prev_3m[0][0]
        perf_3m = round(((curr_price / prev_3m_price) - 1), 4)
    # Calculation of 6 months performance
    prev_6m_date = get_6m_date(month)
    prev_6m = get_prev_6m_price(prev_6m_date, index_code, database)
    if len(prev_6m) == 0:
        perf_6m = None
    else:
        prev_6m_price = prev_6m[0][0]
        perf_6m = round(((curr_price / prev_6m_price) - 1), 4)
    # Calculation of 1 year performance
    prev_1y_date = get_1y_date(month)
    prev_1y = get_prev_1y_price(prev_1y_date, index_code, database)
    if len(prev_1y) == 0:
        perf_1y = None
    else:
        prev_1y_price = prev_1y[0][0]
        date_power_1y = effective_end_date - prev_1y_date
        perf_1y = round((((curr_price / prev_1y_price) ** (365 / date_power_1y.days)) - 1), 4)
    # Calculation of 2 years performance
    prev_2y_date = get_2y_date(month)
    prev_2y = get_prev_2y_price(prev_2y_date, index_code, database)
    if len(prev_2y) == 0:
        perf_2y = None
    else:
        prev_2y_price = prev_2y[0][0]
        date_power_2y = effective_end_date - prev_2y_date
        perf_2y = round((((curr_price / prev_2y_price) ** (365 / date_power_2y.days)) - 1), 4)
    # Calculation of 3 years performance
    prev_3y_date = get_3y_date(month)
    prev_3y = get_prev_3y_price(prev_3y_date, index_code, database)
    if len(prev_3y) == 0:
        perf_3y = None
    else:
        prev_3y_price = prev_3y[0][0]
        date_power_3y = effective_end_date - prev_3y_date
        perf_3y = round((((curr_price / prev_3y_price) ** (365 / date_power_3y.days)) - 1), 4)
    # Calculation of 5 years performance
    prev_5y_date = get_5y_date(month)
    prev_5y = get_prev_5y_price(prev_5y_date, index_code, database)
    if len(prev_5y) == 0:
        perf_5y = None
    else:
        prev_5y_price = prev_5y[0][0]
        date_power_5y = effective_end_date - prev_5y_date
        perf_5y = round((((curr_price / prev_5y_price) ** (365 / date_power_5y.days)) - 1), 4)
    # Calculation of Benchmark performance inception
    inception_date = get_start_date(index_code, database)
    start_date = start_date = get_start_date(index_code, database)
    start_index_price = get_start_price(start_date, index_code, database)
    power_inception = effective_end_date - inception_date
    perf_inception = round((((curr_price / start_index_price) ** (365 / power_inception.days)) - 1), 4)
    final_data = {"index_code": index_code, "perf_1m": perf_1m, "perf_3m": perf_3m, "perf_6m": perf_6m,
                  "perf_1y": perf_1y, "perf_2y": perf_2y, "perf_3y": perf_3y, "perf_5y": perf_5y,
                  "perf_inception": perf_inception, "reporting_date": effective_end_date}
    print(final_data)
    return final_data


def put_index_perf(final_data, database):
    ip_cursor = database.cursor()
    ip_query = "INSERT INTO iq.index_performance (index_code, perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, perf_3y," \
               "perf_5y, perf_inception, reporting_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    ip_values = (final_data['index_code'], final_data['perf_1m'], final_data['perf_3m'], final_data['perf_6m'],
                 final_data['perf_1y'], final_data['perf_2y'], final_data['perf_3y'], final_data['perf_5y'],
                 final_data['perf_inception'], final_data['reporting_date'])
    ip_cursor.execute(ip_query, ip_values)
    ip_cursor.close()


def get_first_record(index_code, month, database):
    effective_start_date, effective_end_date = get_effective_start_end_date(month)
    start_date = get_start_date(index_code, database)
    end_price = get_start_price(start_date, index_code, database)
    curr_price = get_curr_price(effective_end_date, index_code, database)
    # Calculation of Benchmark performance inception
    inception_date = get_start_date(index_code, database)
    start_date = get_start_date(index_code, database)
    start_index_price = get_start_price(start_date, index_code, database)
    power_inception = effective_end_date - inception_date
    perf_inception = round((((curr_price / start_index_price) ** (365 / power_inception.days)) - 1), 4)
    final_data = {"index_code": index_code, "perf_1m": None, "perf_3m": None, "perf_6m": None,
                  "perf_1y": None, "perf_2y": None, "perf_3y": None, "perf_5y": None,
                  "perf_inception": perf_inception, "reporting_date": effective_end_date}
    print(final_data)
    return final_data


try:
    db_host, db_user, db_pass, db_name = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                         'd0m#l1dZwhz!*9Iq0y1h', 'iq'
    # db_host, db_user, db_pass, db_name = env('DB_HOST'), env('DB_USER'), env('DB_PASS'), env('DB_NAME')
    database = MySQLdb.connect(db_host, db_user, db_pass, db_name, use_unicode=True, charset="utf8")
    # index_code_list = get_index_code(database)
    index_code_list = ['BSE100']
    for index_code in index_code_list:
        print(index_code)
        monthly_dates = get_monthly_dates(index_code, database)
        monthly_dates.pop(-1)
        for month in monthly_dates:
            if month is monthly_dates[0]:
                final_data = get_first_record(index_code, month, database)
                put_index_perf(final_data, database)
            else:
                final_data = get_performance(index_code, month, database)
                put_index_perf(final_data, database)
    database.commit()
    database.close()

except Exception as error:
    print("Exception raised :", error)
