import datetime
import re
import math
import statistics


def calc_benchmark_nav(fund_info, iq_database):
    effective_start_date, effective_end_date = get_effective_start_end_date(fund_info)
    previous_1m_date = get_1m_date(fund_info)
    benchmark_index = get_benchmark_index(fund_info, iq_database)
    index_price = get_index_price_as_on_date(effective_end_date, benchmark_index, iq_database)
    prev_index_price = get_index_price_as_on_date(previous_1m_date, benchmark_index, iq_database)
    if len(prev_index_price) == 0:
        previous_index_price = None
    else:
        previous_index_price = prev_index_price[0][0]
    previous_benchmark_nav = get_benchmark_nav(fund_info, previous_1m_date, iq_database)
    benchmark_return = (index_price[0][0] / previous_index_price) - 1
    benchmark_nav = round((previous_benchmark_nav * (1 + benchmark_return)), 6)
    return benchmark_nav
