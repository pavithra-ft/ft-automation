import MySQLdb
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from envparse import env
import datetime
import calendar


def get_alt_benchmark_info(fund_code):
    benchmark_index_cursor = database.cursor()
    benchmark_index_query = "SELECT fund_code, nav_start_date, benchmark_index_code FROM " \
                                "app.per_all_funds where fund_code = '" + fund_code + "'"
    benchmark_index_cursor.execute(benchmark_index_query)
    bm_details = benchmark_index_cursor.fetchall()
    benchmark_index_cursor.close()
    benchmark = {}
    for details in bm_details:
        benchmark = {"fund_code": details[0], "nav_start_date": str(details[1]), "alt_bm_index": details[2]}
    return benchmark


def get_nav_dates(fund_code):
    fund_bm_nav_cursor = database.cursor()
    fund_bm_nav_query = "SELECT effective_end_date from fund_benchmark_nav where fund_code = '" \
                        + fund_code + "' order by effective_end_date"
    fund_bm_nav_cursor.execute(fund_bm_nav_query)
    nav_dates = fund_bm_nav_cursor.fetchall()
    nav_dates_list = list(nav_dates)
    return nav_dates_list


def get_1m_date(current_date):
    current_date = datetime.datetime.strptime(str(current_date), '%Y-%m-%d').replace(day=1).date()
    previous_1m_date = current_date - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1])
    return previous_1m_end_date


def get_curr_price(current_date, bm_info, database):
    curr_price_cursor = database.cursor()
    curr_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + \
                       bm_info['alt_bm_index'] + "' and year(ip.index_price_as_on_date) = year('" + str(
        current_date) \
                       + "') and month(ip.index_price_as_on_date) = month('" + str(current_date) \
                       + "') order by ip.index_price_as_on_date desc limit 1"
    curr_price_cursor.execute(curr_price_query)
    curr_index_details = curr_price_cursor.fetchall()
    print("curr_index_details", curr_index_details)
    curr_index_price = curr_index_details[0][0]
    return curr_index_price


def get_prev_price(current_date, bm_info, database):
    prev_1m_date = get_1m_date(current_date)
    prev_price_cursor = database.cursor()
    prev_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + \
                       bm_info['alt_bm_index'] + "' and year(ip.index_price_as_on_date) = year('" + \
                       str(prev_1m_date) + "') and month(ip.index_price_as_on_date) = month('" + str(prev_1m_date) \
                       + "') order by ip.index_price_as_on_date desc limit 1"
    prev_price_cursor.execute(prev_price_query)
    prev_index_details = prev_price_cursor.fetchall()
    print("prev_index_details", prev_index_details)
    prev_index_price = prev_index_details[0][0]
    return prev_index_price


def get_prev_bm_nav(fund_code, current_date):
    # prev_1m_date = get_1m_date(current_date)
    prev_nav_cursor = database.cursor()
    prev_nav_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where fund_code = '" + fund_code \
                     + "' and effective_end_date = '" + str(current_date) + "'"
    prev_nav_cursor.execute(prev_nav_query)
    previous_nav_details = prev_nav_cursor.fetchall()
    print("previous_nav_details", previous_nav_details)
    return previous_nav_details[0][0]


def get_start_price(bm_info, start_date_nav):
    nav_indexprice_cursor = database.cursor()
    nav_indexprice_query = "SELECT index_price_close from index_prices where index_code = '" + bm_info[
        'alt_bm_index'] + "' and index_price_as_on_date = '" + str(start_date_nav) + "'"
    nav_indexprice_cursor.execute(nav_indexprice_query)
    nav_index_price_details = nav_indexprice_cursor.fetchall()
    if len(nav_index_price_details) != 0:
        print("nav_index_price_details", nav_index_price_details)
        start_index_price = nav_index_price_details[0][0]
    else:
        shift = datetime.timedelta(max(1, (start_date_nav.weekday() + 6) % 7 - 3))
        start_date = start_date_nav - shift
        nav_indexprice_query = "SELECT index_price_close from index_prices where index_code = '" + bm_info[
            'alt_bm_index'] + "' and index_price_as_on_date = '" + str(start_date) + "'"
        nav_indexprice_cursor.execute(nav_indexprice_query)
        nav_index_price_details = nav_indexprice_cursor.fetchall()
        print("nav_index_price_details", nav_index_price_details)
        start_index_price = nav_index_price_details[0][0]
    return start_index_price


def update_first_benchmark_nav(start_date_nav, bm_info, fund_code, database):
    start_date_nav = datetime.datetime.strptime(str(start_date_nav), '%Y-%m-%d').date()
    start_date = start_date_nav - datetime.timedelta(days=1)
    start_end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
    prev_index_price = get_start_price(bm_info, start_date)
    curr_index_price = get_curr_price(start_end_date, bm_info, database)
    prev_month_benchmark_nav = get_prev_bm_nav(fund_code, start_end_date)
    benchmark_return = (curr_index_price / prev_index_price) - 1
    benchmark_nav = round(prev_month_benchmark_nav * (1 + benchmark_return), 6)
    print(fund_code, benchmark_nav, start_end_date)
    put_into_fund_bm_nav(fund_code, benchmark_nav, start_end_date, database)


def update_benchmark_nav(current_date, bm_info, fund_code, database):
    prev_index_price = get_prev_price(current_date, bm_info, database)
    curr_index_price = get_curr_price(current_date, bm_info, database)
    prev_month_benchmark_nav = get_prev_bm_nav(fund_code, current_date)
    benchmark_return = (curr_index_price / prev_index_price) - 1
    benchmark_nav = round(prev_month_benchmark_nav * (1 + benchmark_return), 6)
    put_into_fund_bm_nav(fund_code, benchmark_nav, current_date, database)
    print(fund_code, benchmark_nav, current_date)


def put_into_fund_bm_nav(fund_code, benchmark_nav, date, database):
    insert_cursor = database.cursor()
    insert_query = "UPDATE iq.fund_benchmark_nav SET benchmark_nav = '" + str(benchmark_nav) + \
                   "' where fund_code = '" + fund_code + "' and effective_end_date = '" + str(date) + "'"
    insert_cursor.execute(insert_query)
    insert_cursor.close()


try:
    db_host, db_user, db_pass, db_name = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                         'd0m#l1dZwhz!*9Iq0y1h', 'iq'
    # db_host, db_user, db_pass, db_name = env('DB_HOST'), env('DB_USER'), env('DB_PASS'), env('DB_NAME')
    database = MySQLdb.connect(db_host, db_user, db_pass, db_name, use_unicode=True, charset="utf8")
    fund_code_list = ["45873878"]
    for fund_code in fund_code_list:
        bm_info = get_alt_benchmark_info(fund_code)
        print(bm_info)
        nav_dates_list = get_nav_dates(fund_code)
        start_date_nav = bm_info['nav_start_date']
        for date in nav_dates_list:
            if date is nav_dates_list[0]:
                update_first_benchmark_nav(start_date_nav, bm_info, fund_code, database)
                nav_dates_list.pop(0)
            else:
                current_date = date[0]
                update_benchmark_nav(current_date, bm_info, fund_code, database)
    database.commit()
    print("Commit success")
    database.close()

except Exception as error:
    print("Exception raised :", error)
