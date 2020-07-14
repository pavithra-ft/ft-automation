import database.db_queries as query


def get_alt_benchmark_nav(fund_code, nav_start_date, alt_bm_index, current_date):
    start_index_price = query.get_start_price(nav_start_date, alt_bm_index)
    curr_index_price = float(query.get_index_price_as_on_date(current_date, alt_bm_index)[-1][0])
    alt_benchmark_nav = round((curr_index_price / start_index_price), 6)
    query.put_fund_alt_bm_nav(fund_code, alt_benchmark_nav, current_date)


try:
    fund_code_list = []
    for fund_code in fund_code_list:
        alt_bm_info = query.get_alt_benchmark_info(fund_code)
        nav_dates_list = query.get_nav_dates(fund_code)
        nav_dates_list.pop(0)
        for date in nav_dates_list:
            get_alt_benchmark_nav(fund_code, alt_bm_info[0][0], alt_bm_info[0][1], date)

except Exception as error:
    print("Exception raised :", error)
