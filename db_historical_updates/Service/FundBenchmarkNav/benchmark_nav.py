import database.db_queries as query


def get_benchmark_nav(fund_code, nav_start_date, bm_index, current_date):
    start_index_price = query.get_start_price(nav_start_date, bm_index)
    curr_index_price = float(query.get_index_price_as_on_date(current_date, bm_index)[-1][0])
    benchmark_nav = round((curr_index_price / start_index_price), 6)
    query.put_fund_bm_nav(fund_code, benchmark_nav, current_date)


try:
    fund_code_list = ['29476384']
    for fund_code in fund_code_list:
        bm_info = query.get_benchmark_info(fund_code)
        nav_dates_list = query.get_nav_dates(fund_code)
        nav_dates_list.pop(0)
        for date in nav_dates_list:
            get_benchmark_nav(fund_code, bm_info[0][0], bm_info[0][1], date)

except Exception as error:
    print("Exception raised :", error)
