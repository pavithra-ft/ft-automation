import MySQLdb
from envparse import env

from Spiders.db_actions import get_start_price


def get_benchmark_info(fund_code):
    benchmark_index_cursor = app_database.cursor()
    benchmark_index_query = "SELECT fund_code, nav_start_date, benchmark_index_code FROM " \
                            "app.per_all_funds where fund_code = '" + fund_code + "'"
    benchmark_index_cursor.execute(benchmark_index_query)
    bm_details = benchmark_index_cursor.fetchall()
    benchmark_index_cursor.close()
    benchmark = {}
    for details in bm_details:
        benchmark = {"fund_code": details[0], "nav_start_date": str(details[1]), "bm_index": details[2]}
    return benchmark


def get_nav_dates(fund_code):
    fund_bm_nav_cursor = iq_database.cursor()
    fund_bm_nav_query = "SELECT effective_end_date from iq.fund_benchmark_nav where fund_code = '" \
                        + fund_code + "' order by effective_end_date"
    fund_bm_nav_cursor.execute(fund_bm_nav_query)
    nav_dates = fund_bm_nav_cursor.fetchall()
    nav_dates_list = list(nav_dates)
    return nav_dates_list


def get_curr_price(current_date, bm_info):
    curr_price_cursor = iq_database.cursor()
    curr_price_query = "SELECT ip.index_price_close from iq.index_prices ip where ip.index_code = '" + \
                       bm_info['bm_index'] + "' and year(ip.index_price_as_on_date) = year('" + str(current_date) \
                       + "') and month(ip.index_price_as_on_date) = month('" + str(current_date) \
                       + "') order by ip.index_price_as_on_date desc limit 1"
    curr_price_cursor.execute(curr_price_query)
    curr_index_details = curr_price_cursor.fetchall()
    return curr_index_details[0][0]


def update_benchmark_nav(current_date, bm_info, fund_code):
    start_index_price = get_start_price(bm_info['nav_start_date'], bm_info['bm_index'], iq_database)
    curr_index_price = get_curr_price(current_date, bm_info)
    benchmark_nav = round((curr_index_price / start_index_price), 6)
    put_into_fund_bm_nav(fund_code, benchmark_nav, current_date)
    print("benchmark_nav", fund_code, benchmark_nav, current_date)


def put_into_fund_bm_nav(fund_code, benchmark_nav, date):
    insert_cursor = iq_database.cursor()
    insert_query = "UPDATE iq.fund_benchmark_nav SET benchmark_nav = '" + str(benchmark_nav) + \
                   "' where fund_code = '" + fund_code + "' and effective_end_date = '" + str(date) + "'"
    insert_cursor.execute(insert_query)
    insert_cursor.close()


try:
    # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                'd0m#l1dZwhz!*9Iq0y1h'
    iq_db = 'iq'
    fs_db = 'fs'
    app_db = 'app'

    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db)
    fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db)
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db)
    fund_code_list = ['72966297']
    for fund_code in fund_code_list:
        bm_info = get_benchmark_info(fund_code)
        print(bm_info)
        nav_dates_list = get_nav_dates(fund_code)
        start_date_nav = bm_info['nav_start_date']
        nav_dates_list.pop(0)
        for date in nav_dates_list:
            update_benchmark_nav(date[0], bm_info, fund_code)
    iq_database.commit()
    print("Commit success")
    iq_database.close()
    fs_database.close()
    app_database.close()

except Exception as error:
    print("Exception raised :", error)
