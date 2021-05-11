import database.db_queries as query


def calc_benchmark_nav(fund_code, nav_start_date, bm_index, current_date):
    start_index_price = query.get_start_price(nav_start_date, bm_index)
    curr_index_price = float(query.get_index_price_as_on_date(current_date, bm_index)[-1])
    benchmark_nav = round((curr_index_price / start_index_price), 6)
    try:
        query.put_fund_bm_nav(fund_code, benchmark_nav, current_date)
        query.iq_session.commit()
    except Exception as error:
        query.iq_session.rollback()
        print('Exception raised:', error)
    finally:
        query.iq_session.close()


def get_benchmark_nav(fund_code_list):
    for fund_code in fund_code_list:
        bm_info = query.get_benchmark_info(fund_code)
        nav_dates_list = query.get_nav_dates(fund_code)
        nav_dates_list.pop(0)
        for date in nav_dates_list:
            calc_benchmark_nav(fund_code, bm_info[0], bm_info[1], date)
