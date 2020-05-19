import MySQLdb
from envparse import env

from Spiders.db_actions import get_start_price, get_index_price_as_on_date, put_into_fund_bm_nav, get_benchmark_info, \
    get_nav_dates


def update_benchmark_nav(fund_code, nav_start_date, bm_index, current_date, iq_database):
    start_index_price = get_start_price(nav_start_date, bm_index, iq_database)
    curr_index_price = get_index_price_as_on_date(current_date, bm_index, iq_database)
    benchmark_nav = round((curr_index_price[0][0] / start_index_price), 6)
    put_into_fund_bm_nav(fund_code, benchmark_nav, current_date, iq_database)
    print("benchmark_nav", fund_code, benchmark_nav, current_date)


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
    fund_code_list = []
    for fund_code in fund_code_list:
        bm_info = get_benchmark_info(fund_code, app_database)
        nav_dates_list = get_nav_dates(fund_code, iq_database)
        nav_dates_list.pop(0)
        for date in nav_dates_list:
            update_benchmark_nav(fund_code, bm_info['nav_start_date'], bm_info['bm_index'], date, iq_database)
    iq_database.commit()
    print("Commit success")
    iq_database.close()
    fs_database.close()
    app_database.close()

except Exception as error:
    print("Exception raised :", error)
