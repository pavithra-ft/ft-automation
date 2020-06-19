from database.db_queries import get_start_price, get_index_price_as_on_date, put_fund_bm_nav, get_benchmark_info, \
    get_nav_dates


def get_benchmark_nav(fund_code, nav_start_date, bm_index, current_date):
    start_index_price = get_start_price(nav_start_date, bm_index)
    curr_index_price = get_index_price_as_on_date(current_date, bm_index)
    benchmark_nav = round((curr_index_price / start_index_price), 6)
    put_fund_bm_nav(fund_code, benchmark_nav, current_date)
    print("benchmark_nav", fund_code, benchmark_nav, current_date)


try:
    fund_code_list = []
    for fund_code in fund_code_list:
        bm_info = get_benchmark_info(fund_code)
        nav_dates_list = get_nav_dates(fund_code)
        nav_dates_list.pop(0)
        for date in nav_dates_list:
            get_benchmark_nav(fund_code, bm_info[0][0], bm_info[0][1], date)

except Exception as error:
    print("Exception raised :", error)
