# import pandas as pd
# import os
# import glob
# import MySQLdb
# from envparse import env
# import datetime
# import calendar
# import numpy as np
# import re
# from fuzzywuzzy import fuzz
# from dateutil.relativedelta import relativedelta
# from pandas.tseries.offsets import BMonthEnd
# from Spiders.db_actions import put_fund_performance, put_nav_data, put_market_cap_data, put_fund_portfolio, \
#     put_fund_sector
#
#
# def get_inst_details(keyterm):
#     inst_cursor = database.cursor()
#     inst_query = "SELECT inst_code FROM per_all_institutions where inst_display_name like '%" + keyterm + "%' "
#     inst_cursor.execute(inst_query)
#     inst_details = inst_cursor.fetchall()
#     inst_code = inst_details[0][0]
#     inst_cursor.close()
#     return inst_code
#
#
# def get_funds_list(inst_code):
#     fund_cursor = database.cursor()
#     fund_query = "SELECT paf.fund_code, paf.inst_code, paf.fund_name, paf.fund_type_code FROM per_all_funds paf, " \
#                  "per_all_institutions pai where pai.inst_code = paf.inst_code and pai.inst_code='" + inst_code + "' "
#     fund_cursor.execute(fund_query)
#     funds_list = fund_cursor.fetchall()
#     fund_cursor.close()
#     return funds_list
#
#
# def get_fund_code():
#     global fund_code
#     fund_name = str(df.iloc[2, 1])
#     if "Value" in fund_name:
#         for i in fund_list:
#             if "Value" in i[2]:
#                 fund_code = i[0]
#     elif "Flexicap" in fund_name:
#         for i in fund_list:
#             if "Flexicap" in i[2]:
#                 fund_code = i[0]
#     elif "Largecap" in fund_name:
#         for i in fund_list:
#             if "Largecap" in i[2]:
#                 fund_code = i[0]
#     elif "Contra" in fund_name:
#         for i in fund_list:
#             if "Contra" in i[2]:
#                 fund_code = i[0]
#     return fund_code
#
#
# def get_last_working_date():
#     start_date = datetime.datetime.strptime(file_date, '%b %Y').date()
#     end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
#     offset = BMonthEnd()
#     last_date = offset.rollforward(start_date)
#     effective_last_date = last_date.date()
#     return start_date, end_date, effective_last_date
#
#
# def get_previous_last_working_date():
#     start_date, end_date, effective_last_date = get_last_working_date()
#     previous_month_date = start_date - relativedelta(months=1)
#     previous_month_end_date = previous_month_date.replace(day=calendar.monthrange(previous_month_date.year,
#                                                                                   previous_month_date.month)[1])
#     off = BMonthEnd()
#     previous_month_end_date = off.rollback(previous_month_end_date)
#     return previous_month_end_date
#
#
# def get_benchmark_index():
#     benchmark_index_cursor = database.cursor()
#     start_date, end_date, effective_last_date = get_last_working_date()
#     benchmark_index_query = "SELECT benchmark_index_code FROM fund_benchmark_nav where fund_code = '" + \
#                             get_fund_code() + "' and effective_end_date = '" + str(end_date) + "'"
#     benchmark_index_cursor.execute(benchmark_index_query)
#     benchmark_index_details = benchmark_index_cursor.fetchall()
#     benchmark_index_code = benchmark_index_details[0][0]
#     benchmark_index_cursor.close()
#     return benchmark_index_code
#
#
# def get_index_price():
#     index_price_cursor = database.cursor()
#     start_date, end_date, effective_last_date = get_last_working_date()
#     index_price_query = "SELECT index_price_close FROM index_prices where index_code = '" + get_benchmark_index() + \
#                         "' and index_price_as_on_date = '" + str(effective_last_date) + "'"
#     index_price_cursor.execute(index_price_query)
#     index_price_details = index_price_cursor.fetchall()
#     index_price = index_price_details[0][0]
#     index_price_cursor.close()
#     return index_price
#
#
# def get_previous_index_price():
#     previous_index_price_cursor = database.cursor()
#     previous_month_end_date = get_previous_last_working_date()
#     benchmark_index_code = get_benchmark_index()
#     previous_index_price_query = "SELECT index_price_close FROM index_prices where index_code = '" + \
#                                  benchmark_index_code + "' and index_price_as_on_date = '" + \
#                                  str(previous_month_end_date) + "'"
#     previous_index_price_cursor.execute(previous_index_price_query)
#     previous_index_price_details = previous_index_price_cursor.fetchall()
#     previous_index_price = previous_index_price_details[0][0]
#     previous_index_price_cursor.close()
#     return previous_index_price
#
#
# def get_benchmark_nav():
#     benchmark_nav_cursor = database.cursor()
#     previous_month_end_date = get_1m_date()
#     benchmark_nav_query = "SELECT benchmark_nav FROM fund_benchmark_nav where fund_code = '" + \
#                           get_fund_code() + "' and effective_end_date = '" + \
#                           str(previous_month_end_date) + "'"
#     benchmark_nav_cursor.execute(benchmark_nav_query)
#     benchmark_nav_details = benchmark_nav_cursor.fetchall()
#     benchmark_previous_nav = benchmark_nav_details[0][0]
#     benchmark_nav_cursor.close()
#     effective_last_index_price = get_index_price()
#     effective_previous_index_price = get_previous_index_price()
#     benchmark_return = (effective_last_index_price / effective_previous_index_price) - 1
#     benchmark_nav = round((benchmark_previous_nav * (1 + benchmark_return)), 4)
#     return benchmark_nav, benchmark_previous_nav
#
#
# def get_alt_benchmark_index():
#     alt_benchmark_index_cursor = database.cursor()
#     start_date, end_date, effective_last_date = get_last_working_date()
#     alt_benchmark_index_query = "SELECT alt_benchmark_index_code FROM fund_benchmark_nav where fund_code = '" + \
#                                 get_fund_code() + "' and effective_end_date = '" + str(end_date) + "'"
#     alt_benchmark_index_cursor.execute(alt_benchmark_index_query)
#     alt_benchmark_index_details = alt_benchmark_index_cursor.fetchall()
#     alt_benchmark_index_code = alt_benchmark_index_details[0][0]
#     alt_benchmark_index_cursor.close()
#     return alt_benchmark_index_code
#
#
# def get_alt_index_price():
#     alt_index_price_cursor = database.cursor()
#     start_date, end_date, effective_last_date = get_last_working_date()
#     alt_index_price_query = "SELECT index_price_close FROM index_prices where index_code = '" + \
#                             get_alt_benchmark_index() + "' and index_price_as_on_date = '" + str(effective_last_date) \
#                             + "'"
#     alt_index_price_cursor.execute(alt_index_price_query)
#     alt_index_price_details = alt_index_price_cursor.fetchall()
#     alt_index_price = alt_index_price_details[0][0]
#     alt_index_price_cursor.close()
#     return alt_index_price
#
#
# def get_alt_previous_index_price():
#     alt_previous_index_price_cursor = database.cursor()
#     alt_previous_month_end_date = get_previous_last_working_date()
#     alt_previous_index_price_query = "SELECT index_price_close FROM index_prices where index_code = '" + \
#                                      get_alt_benchmark_index() + "' and index_price_as_on_date = '" + \
#                                      str(alt_previous_month_end_date) + "'"
#     alt_previous_index_price_cursor.execute(alt_previous_index_price_query)
#     alt_previous_index_price_details = alt_previous_index_price_cursor.fetchall()
#     alt_previous_index_price = alt_previous_index_price_details[0][0]
#     alt_previous_index_price_cursor.close()
#     return alt_previous_index_price
#
#
# def get_alt_benchmark_nav():
#     alt_benchmark_nav_cursor = database.cursor()
#     alt_previous_month_end_date = get_1m_date()
#     alt_benchmark_nav_query = "SELECT alt_benchmark_nav FROM fund_benchmark_nav where fund_code = '" + \
#                               get_fund_code() + "' and effective_end_date = '" + \
#                               str(alt_previous_month_end_date) + "'"
#     alt_benchmark_nav_cursor.execute(alt_benchmark_nav_query)
#     alt_benchmark_nav_details = alt_benchmark_nav_cursor.fetchall()
#     alt_benchmark_previous_nav = alt_benchmark_nav_details[0][0]
#     alt_benchmark_nav_cursor.close()
#     effective_alt_last_index_price = get_alt_index_price()
#     effective_alt_previous_index_price = get_alt_previous_index_price()
#     alt_benchmark_return = (effective_alt_last_index_price / effective_alt_previous_index_price) - 1
#     alt_benchmark_nav = round((alt_benchmark_previous_nav * (1 + alt_benchmark_return)), 4)
#     return alt_benchmark_nav, alt_benchmark_previous_nav
#
#
# def get_effective_start_end_date():
#     start_date = datetime.datetime.strptime(file_date, '%b %Y').date()
#     effective_start_date = start_date.replace(day=1)
#     effective_end_date = start_date.replace(
#         day=calendar.monthrange(effective_start_date.year, effective_start_date.month)[1])
#     return effective_start_date, effective_end_date
#
#
# def get_1m_date():
#     effective_start_date, effective_end_date = get_effective_start_end_date()
#     previous_1m_date = effective_end_date - relativedelta(months=1)
#     previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
#                                                                             previous_1m_date.month)[1])
#     return previous_1m_end_date
#
#
# def get_3m_date():
#     effective_start_date, effective_end_date = get_effective_start_end_date()
#     previous_3m_date = effective_end_date - relativedelta(months=3)
#     previous_3m_end_date = previous_3m_date.replace(day=calendar.monthrange(previous_3m_date.year,
#                                                                             previous_3m_date.month)[1])
#     return previous_3m_end_date
#
#
# def get_6m_date():
#     effective_start_date, effective_end_date = get_effective_start_end_date()
#     previous_6m_date = effective_end_date - relativedelta(months=6)
#     previous_6m_end_date = previous_6m_date.replace(day=calendar.monthrange(previous_6m_date.year,
#                                                                             previous_6m_date.month)[1])
#     return previous_6m_end_date
#
#
# def get_1y_date():
#     effective_start_date, effective_end_date = get_effective_start_end_date()
#     previous_1y_date = effective_end_date - relativedelta(years=1)
#     previous_1y_end_date = (previous_1y_date.replace(day=calendar.monthrange(previous_1y_date.year,
#                                                                              previous_1y_date.month)[1]))
#     return previous_1y_end_date
#
#
# def get_2y_date():
#     effective_start_date, effective_end_date = get_effective_start_end_date()
#     previous_2y_date = effective_end_date - relativedelta(years=2)
#     previous_2y_end_date = previous_2y_date.replace(day=calendar.monthrange(previous_2y_date.year,
#                                                                             previous_2y_date.month)[1])
#     return previous_2y_end_date
#
#
# def get_3y_date():
#     effective_start_date, effective_end_date = get_effective_start_end_date()
#     previous_3y_date = effective_end_date - relativedelta(years=3)
#     previous_3y_end_date = previous_3y_date.replace(day=calendar.monthrange(previous_3y_date.year,
#                                                                             previous_3y_date.month)[1])
#     return previous_3y_end_date
#
#
# def get_5y_date():
#     effective_start_date, effective_end_date = get_effective_start_end_date()
#     previous_5y_date = effective_end_date - relativedelta(years=5)
#     previous_5y_end_date = previous_5y_date.replace(day=calendar.monthrange(previous_5y_date.year,
#                                                                             previous_5y_date.month)[1])
#     return previous_5y_end_date
#
#
# def get_inception_date():
#     since_inception_cursor = database.cursor()
#     since_inception_query = "SELECT nav_start_date from per_all_funds where fund_code = '" + fund_code + "'"
#     since_inception_cursor.execute(since_inception_query)
#     inception_date = since_inception_cursor.fetchall()
#     since_inception_cursor.close()
#     temp = str(inception_date[0][0])
#     inception_date = datetime.datetime.strptime(temp, '%Y-%m-%d').date()
#     return inception_date
#
#
# def update_islatest():
#     update_cursor = database.cursor()
#     previous_1m_end_date = get_1m_date()
#     update_query = "UPDATE fund_performance SET isLatest = NULL where effective_end_date = '" + \
#                    str(previous_1m_end_date) + "'"
#     update_cursor.execute(update_query)
#
#
# def get_fund_performance():
#     global mega_value, large_value, small_value, micro_value, market_cap_type_code
#     fund_code = get_fund_code()
#     aum = float(df.iloc[6, 2].replace("Rs ", "").replace(" cr", ""))
#     current_aum = float(aum) * 10000000
#     clients = df.iloc[5, 2]
#     if clients == "nan":
#         no_of_clients = None
#     else:
#         no_of_clients = clients
#     # getting fund allocations
#     equity_allocation = float(df.iloc[13, 6])
#     portfolio_equity_allocation = round((equity_allocation / 100), 4)
#     cash_allocation = float(df.iloc[15, 6])
#     portfolio_cash_allocation = round((cash_allocation / 100), 4)
#     asset_allocation = float(df.iloc[14, 6])
#     if asset_allocation == "-" or asset_allocation is None:
#         portfolio_asset_allocation = None
#     elif asset_allocation == float(df.iloc[14, 6]):
#         portfolio_asset_allocation = round((asset_allocation / 100), 4)
#     else:
#         portfolio_asset_allocation = None
#     performance_1m = round(float(df.iloc[9, 2]), 4)
#     created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     created_by = "fintuple-data"
#     isLatest = '1'
#     effective_start_date, effective_end_date = get_effective_start_end_date()
#     previous_1m_end_date = get_1m_date()
#     previous_1m_cursor = database.cursor()
#     previous_1m_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
#                         str(previous_1m_end_date) + "' and fund_code = '" + fund_code + "'"
#     previous_1m_cursor.execute(previous_1m_query)
#     previous_1m_nav = previous_1m_cursor.fetchall()
#     previous_1m_cursor.close()
#     # current month fund NAV
#     previous_1m_nav_final = previous_1m_nav[0][0]
#     fund_nav = round((previous_1m_nav_final * (1 + performance_1m)), 4)
#     # performance of 1 month
#     perf_1m = round(((fund_nav / previous_1m_nav_final) - 1), 4)
#     # performance of 3 months
#     previous_3m_end_date = get_3m_date()
#     previous_3m_cursor = database.cursor()
#     previous_3m_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
#                         str(previous_3m_end_date) + "' and fund_code = '" + fund_code + "'"
#     previous_3m_cursor.execute(previous_3m_query)
#     previous_3m = previous_3m_cursor.fetchall()
#     previous_3m_cursor.close()
#     if len(previous_3m) == 0:
#         perf_3m = None
#     else:
#         previous_3m_final = previous_3m[0][0]
#         perf_3m = round(((fund_nav / previous_3m_final) - 1), 4)
#     # performance of 6 months
#     previous_6m_end_date = get_6m_date()
#     previous_6m_cursor = database.cursor()
#     previous_6m_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
#                         str(previous_6m_end_date) + "' and fund_code = '" + fund_code + "'"
#     previous_6m_cursor.execute(previous_6m_query)
#     previous_6m = previous_6m_cursor.fetchall()
#     previous_6m_cursor.close()
#     if len(previous_6m) == 0:
#         perf_6m = None
#     else:
#         previous_6m_final = previous_6m[0][0]
#         perf_6m = round(((fund_nav / previous_6m_final) - 1), 4)
#     # performance of 1 year
#     previous_1y_end_date = get_1y_date()
#     previous_1y_cursor = database.cursor()
#     previous_1y_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
#                         str(previous_1y_end_date) + "' and fund_code = '" + fund_code + "'"
#     previous_1y_cursor.execute(previous_1y_query)
#     previous_1y = previous_1y_cursor.fetchall()
#     previous_1y_cursor.close()
#     if len(previous_1y) == 0:
#         perf_1y = None
#     else:
#         previous_1y_final = previous_1y[0][0]
#         date_power_1y = effective_end_date - previous_1y_end_date
#         perf_1y = round((((fund_nav / previous_1y_final) ** (365 / date_power_1y.days)) - 1), 4)
#     # performance of 2 years
#     previous_2y_end_date = get_2y_date()
#     previous_2y_cursor = database.cursor()
#     previous_2y_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
#                         str(previous_2y_end_date) + "' and fund_code = '" + fund_code + "'"
#     previous_2y_cursor.execute(previous_2y_query)
#     previous_2y = previous_2y_cursor.fetchall()
#     previous_2y_cursor.close()
#     if len(previous_2y) == 0:
#         perf_2y = None
#     else:
#         previous_2y_final = previous_2y[0][0]
#         date_power_2y = effective_end_date - previous_2y_end_date
#         perf_2y = round((((fund_nav / previous_2y_final) ** (365 / date_power_2y.days)) - 1), 4)
#     # performance of 3 years
#     previous_3y_end_date = get_3y_date()
#     previous_3y_cursor = database.cursor()
#     previous_3y_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
#                         str(previous_3y_end_date) + "' and fund_code = '" + fund_code + "'"
#     previous_3y_cursor.execute(previous_3y_query)
#     previous_3y = previous_3y_cursor.fetchall()
#     previous_3y_cursor.close()
#     if len(previous_3y) == 0:
#         perf_3y = None
#     else:
#         previous_3y_final = previous_3y[0][0]
#         date_power_3y = effective_end_date - previous_3y_end_date
#         perf_3y = round((((fund_nav / previous_3y_final) ** (365 / date_power_3y.days)) - 1), 4)
#     # performance of 5 years
#     previous_5y_end_date = get_5y_date()
#     previous_5y_cursor = database.cursor()
#     previous_5y_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
#                         str(previous_5y_end_date) + "' and fund_code = '" + fund_code + "'"
#     previous_5y_cursor.execute(previous_5y_query)
#     previous_5y = previous_5y_cursor.fetchall()
#     previous_5y_cursor.close()
#     if len(previous_5y) == 0:
#         perf_5y = None
#     else:
#         previous_5y_final = previous_5y[0][0]
#         date_power_5y = effective_end_date - previous_5y_end_date
#         perf_5y = round((((fund_nav / previous_5y_final) ** (365 / date_power_5y.days)) - 1), 4)
#     # performance inception
#     inception_date = get_inception_date()
#     date_power_inception = effective_end_date - inception_date
#     perf_inception = round((((fund_nav / 1) ** (365 / date_power_inception.days)) - 1), 4)
#     # market_cap_type_code
#     index = 2
#     cap_type = {}
#     while df.iloc[index, 5] != "TOTAL":
#         type_market_cap = df.iloc[index, 5].replace(" Cap", "")
#         cap_type[type_market_cap] = float(df.iloc[index, 6])
#         index += 1
#     for k, v in cap_type.items():
#         if "Mega" in k:
#             mega_value = v
#         if "Large" in k:
#             large_value = v
#         if "Small" in k:
#             small_value = v
#         if "Micro" in k:
#             micro_value = v
#     cap_type.update({"Large": mega_value + large_value})
#     cap_type.update({"Small": small_value + micro_value})
#     del cap_type['Mega'], cap_type['Micro'], cap_type['Cash']
#     cap_type_cursor = database.cursor()
#     value_type = []
#     for k, v in cap_type.items():
#         if v >= 70:
#             cap_type_query = "SELECT market_cap_type_code from mas_market_cap_types where market_cap_type_desc like " \
#                              "'" + "Large Cap" + "%'"
#             cap_type_cursor.execute(cap_type_query)
#             type_code = cap_type_cursor.fetchall()
#             market_cap_type_code = type_code[0][0]
#         elif 70 > v >= 20:
#             value_type.append(k)
#     if value_type == ["Large", "Mid", "Small"]:
#         cap_type_query = "SELECT market_cap_type_code from mas_market_cap_types where market_cap_type_desc " \
#                          "like '" + "Multi Cap" + "%'"
#         cap_type_cursor.execute(cap_type_query)
#         type_code = cap_type_cursor.fetchall()
#         market_cap_type_code = type_code[0][0]
#     elif value_type == ["Large", "Small"]:
#         cap_type_query = "SELECT market_cap_type_code from mas_market_cap_types where market_cap_type_desc " \
#                          "like '" + "Large-Small Cap" + "%'"
#         cap_type_cursor.execute(cap_type_query)
#         type_code = cap_type_cursor.fetchall()
#         market_cap_type_code = type_code[0][0]
#     elif value_type == ["Large", "Mid"]:
#         cap_type_query = "SELECT market_cap_type_code from mas_market_cap_types where market_cap_type_desc " \
#                          "like '" + "Large-Mid Cap" + "%'"
#         cap_type_cursor.execute(cap_type_query)
#         type_code = cap_type_cursor.fetchall()
#         market_cap_type_code = type_code[0][0]
#     elif value_type == ["Mid", "Small"]:
#         cap_type_query = "SELECT market_cap_type_code from mas_market_cap_types where market_cap_type_desc " \
#                          "like '" + "Mid-Small Cap" + "%'"
#         cap_type_cursor.execute(cap_type_query)
#         type_code = cap_type_cursor.fetchall()
#         market_cap_type_code = type_code[0][0]
#     return fund_code, current_aum, no_of_clients, market_cap_type_code, portfolio_equity_allocation, \
#            portfolio_cash_allocation, portfolio_asset_allocation, perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, \
#            perf_3y, perf_5y, perf_inception, isLatest, effective_start_date, effective_end_date, created_ts, \
#            created_by, fund_nav
#
#
# def get_benchmark_performance():
#     effective_start_date, effective_end_date = get_effective_start_end_date()
#     benchmark_nav, benchmark_previous_nav = get_benchmark_nav()
#     # benchmark performance of 1 month
#     benchmark_perf_1m = round(((benchmark_nav / benchmark_previous_nav) - 1), 4)
#     benchmark_index_code = get_benchmark_index()
#     # benchmark performance of 3 months
#     benchmark_3m_end_date = get_3m_date()
#     benchmark_3m_cursor = database.cursor()
#     benchmark_3m_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                          str(benchmark_3m_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
#                          + "' and fund_code = '" + fund_code + "' "
#     benchmark_3m_cursor.execute(benchmark_3m_query)
#     benchmark_3m = benchmark_3m_cursor.fetchall()
#     benchmark_3m_cursor.close()
#     if len(benchmark_3m) == 0:
#         benchmark_perf_3m = None
#     else:
#         benchmark_3m_final = benchmark_3m[0][0]
#         benchmark_perf_3m = round(((benchmark_nav / benchmark_3m_final) - 1), 4)
#     # benchmark performance of 6 months
#     benchmark_6m_end_date = get_6m_date()
#     benchmark_6m_cursor = database.cursor()
#     benchmark_6m_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                          str(benchmark_6m_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
#                          + "' and fund_code = '" + fund_code + "' "
#     benchmark_6m_cursor.execute(benchmark_6m_query)
#     benchmark_6m = benchmark_6m_cursor.fetchall()
#     benchmark_6m_cursor.close()
#     if len(benchmark_6m) == 0:
#         benchmark_perf_6m = None
#     else:
#         benchmark_6m_final = benchmark_6m[0][0]
#         benchmark_perf_6m = round(((benchmark_nav / benchmark_6m_final) - 1), 4)
#     # benchmark performance of 1 year
#     benchmark_1y_end_date = get_1y_date()
#     benchmark_1y_cursor = database.cursor()
#     benchmark_1y_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                          str(benchmark_1y_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
#                          + "' and fund_code = '" + fund_code + "' "
#     benchmark_1y_cursor.execute(benchmark_1y_query)
#     benchmark_1y = benchmark_1y_cursor.fetchall()
#     benchmark_1y_cursor.close()
#     if len(benchmark_1y) == 0:
#         benchmark_perf_1y = None
#     else:
#         benchmark_1y_final = benchmark_1y[0][0]
#         benchmark_date_power_1y = effective_end_date - benchmark_1y_end_date
#         benchmark_perf_1y = round((((benchmark_nav / benchmark_1y_final) ** (365 / benchmark_date_power_1y.days)) - 1),
#                                   4)
#     # benchmark performance of 2 years
#     benchmark_2y_end_date = get_2y_date()
#     benchmark_2y_cursor = database.cursor()
#     benchmark_2y_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                          str(benchmark_2y_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
#                          + "' and fund_code = '" + fund_code + "' "
#     benchmark_2y_cursor.execute(benchmark_2y_query)
#     benchmark_2y = benchmark_2y_cursor.fetchall()
#     benchmark_2y_cursor.close()
#     if len(benchmark_2y) == 0:
#         benchmark_perf_2y = None
#     else:
#         benchmark_2y_final = benchmark_2y[0][0]
#         benchmark_date_power_2y = effective_end_date - benchmark_2y_end_date
#         benchmark_perf_2y = round((((benchmark_nav / benchmark_2y_final) ** (365 / benchmark_date_power_2y.days)) - 1),
#                                   4)
#     # benchmark performance of 3 years
#     benchmark_3y_end_date = get_3y_date()
#     benchmark_3y_cursor = database.cursor()
#     benchmark_3y_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                          str(benchmark_3y_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
#                          + "' and fund_code = '" + fund_code + "' "
#     benchmark_3y_cursor.execute(benchmark_3y_query)
#     benchmark_3y = benchmark_3y_cursor.fetchall()
#     benchmark_3y_cursor.close()
#     if len(benchmark_3y) == 0:
#         benchmark_perf_3y = None
#     else:
#         benchmark_3y_final = benchmark_3y[0][0]
#         benchmark_date_power_3y = effective_end_date - benchmark_3y_end_date
#         benchmark_perf_3y = round((((benchmark_nav / benchmark_3y_final) ** (365 / benchmark_date_power_3y.days)) - 1),
#                                   4)
#     # benchmark performance of 5 years
#     benchmark_5y_end_date = get_5y_date()
#     benchmark_5y_cursor = database.cursor()
#     benchmark_5y_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                          str(benchmark_5y_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
#                          + "' and fund_code = '" + fund_code + "' "
#     benchmark_5y_cursor.execute(benchmark_5y_query)
#     benchmark_5y = benchmark_5y_cursor.fetchall()
#     benchmark_5y_cursor.close()
#     if len(benchmark_5y) == 0:
#         benchmark_perf_5y = None
#     else:
#         benchmark_5y_final = benchmark_5y[0][0]
#         benchmark_date_power_5y = effective_end_date - benchmark_5y_end_date
#         benchmark_perf_5y = round((((benchmark_nav / benchmark_5y_final) ** (365 / benchmark_date_power_5y.days)) - 1),
#                                   4)
#     # benchmark performance inception
#     inception_date = get_inception_date()
#     benchmark_power_inception = effective_end_date - inception_date
#     benchmark_perf_inception = round((((benchmark_nav / 1) ** (365 / benchmark_power_inception.days)) - 1), 4)
#     return benchmark_perf_1m, benchmark_perf_3m, benchmark_perf_6m, benchmark_perf_1y, benchmark_perf_2y, \
#            benchmark_perf_3y, benchmark_perf_5y, benchmark_perf_inception
#
#
# def get_alt_benchmark_performance():
#     effective_start_date, effective_end_date = get_effective_start_end_date()
#     alt_benchmark_nav, alt_benchmark_previous_nav = get_alt_benchmark_nav()
#     # alternate benchmark performance of 1 month
#     alt_benchmark_perf_1m = round(((alt_benchmark_nav / alt_benchmark_previous_nav) - 1), 4)
#     alt_benchmark_index_code = get_alt_benchmark_index()
#     # alternate benchmark performance of 3 months
#     alt_benchmark_3m_end_date = get_3m_date()
#     alt_benchmark_3m_cursor = database.cursor()
#     alt_benchmark_3m_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                              str(alt_benchmark_3m_end_date) + "' and alt_benchmark_index_code = '" + \
#                              alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
#     alt_benchmark_3m_cursor.execute(alt_benchmark_3m_query)
#     alt_benchmark_3m = alt_benchmark_3m_cursor.fetchall()
#     alt_benchmark_3m_cursor.close()
#     if len(alt_benchmark_3m) == 0:
#         alt_benchmark_perf_3m = None
#     else:
#         alt_benchmark_3m_final = alt_benchmark_3m[0][0]
#         alt_benchmark_perf_3m = round(((alt_benchmark_nav / alt_benchmark_3m_final) - 1), 4)
#     # alternate benchmark performance of 6 months
#     alt_benchmark_6m_end_date = get_6m_date()
#     alt_benchmark_6m_cursor = database.cursor()
#     alt_benchmark_6m_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                              str(alt_benchmark_6m_end_date) + "' and alt_benchmark_index_code = '" + \
#                              alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
#     alt_benchmark_6m_cursor.execute(alt_benchmark_6m_query)
#     alt_benchmark_6m = alt_benchmark_6m_cursor.fetchall()
#     alt_benchmark_6m_cursor.close()
#     if len(alt_benchmark_6m) == 0:
#         alt_benchmark_perf_6m = None
#     else:
#         alt_benchmark_6m_final = alt_benchmark_6m[0][0]
#         alt_benchmark_perf_6m = round(((alt_benchmark_nav / alt_benchmark_6m_final) - 1), 4)
#     # alternate benchmark performance of 1 year
#     alt_benchmark_1y_end_date = get_1y_date()
#     alt_benchmark_1y_cursor = database.cursor()
#     alt_benchmark_1y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                              str(alt_benchmark_1y_end_date) + "' and alt_benchmark_index_code = '" + \
#                              alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
#     alt_benchmark_1y_cursor.execute(alt_benchmark_1y_query)
#     alt_benchmark_1y = alt_benchmark_1y_cursor.fetchall()
#     alt_benchmark_1y_cursor.close()
#     if len(alt_benchmark_1y) == 0:
#         alt_benchmark_perf_1y = None
#     else:
#         alt_benchmark_1y_final = alt_benchmark_1y[0][0]
#         alt_benchmark_date_power_1y = effective_end_date - alt_benchmark_1y_end_date
#         alt_benchmark_perf_1y = round((((alt_benchmark_nav / alt_benchmark_1y_final) **
#                                         (365 / alt_benchmark_date_power_1y.days)) - 1), 4)
#     # alternate benchmark performance of 2 years
#     alt_benchmark_2y_end_date = get_2y_date()
#     alt_benchmark_2y_cursor = database.cursor()
#     alt_benchmark_2y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                              str(alt_benchmark_2y_end_date) + "' and alt_benchmark_index_code = '" + \
#                              alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
#     alt_benchmark_2y_cursor.execute(alt_benchmark_2y_query)
#     alt_benchmark_2y = alt_benchmark_2y_cursor.fetchall()
#     alt_benchmark_2y_cursor.close()
#     if len(alt_benchmark_2y) == 0:
#         alt_benchmark_perf_2y = None
#     else:
#         alt_benchmark_2y_final = alt_benchmark_2y[0][0]
#         alt_benchmark_date_power_2y = effective_end_date - alt_benchmark_2y_end_date
#         alt_benchmark_perf_2y = round((((alt_benchmark_nav / alt_benchmark_2y_final) **
#                                         (365 / alt_benchmark_date_power_2y.days)) - 1), 4)
#     # alternate benchmark performance of 3 years
#     alt_benchmark_3y_end_date = get_3y_date()
#     alt_benchmark_3y_cursor = database.cursor()
#     alt_benchmark_3y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                              str(alt_benchmark_3y_end_date) + "' and alt_benchmark_index_code = '" + \
#                              alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
#     alt_benchmark_3y_cursor.execute(alt_benchmark_3y_query)
#     alt_benchmark_3y = alt_benchmark_3y_cursor.fetchall()
#     alt_benchmark_3y_cursor.close()
#     if len(alt_benchmark_3y) == 0:
#         alt_benchmark_perf_3y = None
#     else:
#         alt_benchmark_3y_final = alt_benchmark_3y[0][0]
#         alt_benchmark_date_power_3y = effective_end_date - alt_benchmark_3y_end_date
#         alt_benchmark_perf_3y = round((((alt_benchmark_nav / alt_benchmark_3y_final) **
#                                         (365 / alt_benchmark_date_power_3y.days)) - 1), 4)
#     # alternate benchmark performance of 5 years
#     alt_benchmark_5y_end_date = get_5y_date()
#     alt_benchmark_5y_cursor = database.cursor()
#     alt_benchmark_5y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
#                              str(alt_benchmark_5y_end_date) + "' and alt_benchmark_index_code = '" + \
#                              alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
#     alt_benchmark_5y_cursor.execute(alt_benchmark_5y_query)
#     alt_benchmark_5y = alt_benchmark_5y_cursor.fetchall()
#     alt_benchmark_5y_cursor.close()
#     if len(alt_benchmark_5y) == 0:
#         alt_benchmark_perf_5y = None
#     else:
#         alt_benchmark_5y_final = alt_benchmark_5y[0][0]
#         alt_benchmark_date_power_5y = effective_end_date - alt_benchmark_5y_end_date
#         alt_benchmark_perf_5y = round((((alt_benchmark_nav / alt_benchmark_5y_final) **
#                                         (365 / alt_benchmark_date_power_5y.days)) - 1), 4)
#     # alternate benchmark inception
#     inception_date = get_inception_date()
#     alt_benchmark_power_inception = effective_end_date - inception_date
#     alt_benchmark_perf_inception = round((((alt_benchmark_nav / 1) ** (365 / alt_benchmark_power_inception.days)) - 1),
#                                          4)
#     return alt_benchmark_perf_1m, alt_benchmark_perf_3m, alt_benchmark_perf_6m, alt_benchmark_perf_1y, \
#            alt_benchmark_perf_2y, alt_benchmark_perf_3y, alt_benchmark_perf_5y, alt_benchmark_perf_inception
#
#
# def get_market_cap():
#     fund_code, current_aum, no_of_clients, market_cap_type_code, portfolio_equity_allocation, \
#     portfolio_cash_allocation, portfolio_asset_allocation, perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, perf_3y, \
#     perf_5y, perf_inception, isLatest, effective_start_date, effective_end_date, created_ts, created_by, \
#     fund_nav = get_fund_performance()
#     index = 2
#     capData = []
#     while df.iloc[index, 5] != "TOTAL":
#         cap_body = {}
#         exposure = float(df.iloc[index, 6])
#         if exposure == 0.0:
#             index += 1
#             continue
#         cap_body.update({"fund_code": fund_code})
#         cap_body.update({"type_market_cap": df.iloc[index, 5].replace(" Cap", "")})
#         cap_body.update({"exposure": round((float(df.iloc[index, 6]) / 100), 4)})
#         cap_body.update({"start_date": effective_start_date})
#         cap_body.update({"end_date": effective_end_date})
#         cap_body.update({"created_ts": created_ts})
#         cap_body.update({"action_by": created_by})
#         capData.append(cap_body)
#         index += 1
#     return capData
#
#
# def get_isin(security_name):
#     global security_isin
#     security_cursor = database.cursor()
#     if security_name == "Cash & Equivalents" or security_name == "Cash":
#         security_isin = "CASH"
#     else:
#         security_query = "SELECT security_isin from mas_securities where security_name = '" + security_name + "'"
#         security_cursor.execute(security_query)
#         isin_details = security_cursor.fetchall()
#         if len(isin_details) == 0:
#             security_name = security_name.replace(".", " ")
#             security_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', security_name)
#             isin_cursor = database.cursor()
#             isin_query = "SELECT security_isin, security_name from mas_securities"
#             isin_cursor.execute(isin_query)
#             security_details = isin_cursor.fetchall()
#             max_ratio = 0
#             max_index = 0
#             for value in range(len(security_details)):
#                 name = security_details[value][1].replace(".", " ")
#                 name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', name)
#                 ratio = fuzz.token_sort_ratio(security_name.lower(), name.lower())
#                 if ratio > 78 and max_ratio < ratio:
#                     max_ratio = ratio
#                     max_index = value
#             security_isin = security_details[max_index][0]
#         else:
#             security_isin = isin_details[0][0]
#     return security_isin
#
#
# def get_fund_portfolio():
#     fund_code, current_aum, no_of_clients, market_cap_type_code, portfolio_equity_allocation, \
#     portfolio_cash_allocation, portfolio_asset_allocation, perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, perf_3y, \
#     perf_5y, perf_inception, isLatest, effective_start_date, effective_end_date, created_ts, created_by, \
#     fund_nav = get_fund_performance()
#     portfoliodata = []
#     index = 22
#     while df.iloc[index, 3] != "nan":
#         portfolio_body = {}
#         portfolio_body.update({"fund_code": fund_code})
#         portfolio_body.update({"security_isin": get_isin(df.iloc[index, 1])})
#         portfolio_body.update({"exposure": round(float(df.iloc[index, 3]), 4)})
#         portfolio_body.update({"start_date": effective_start_date})
#         portfolio_body.update({"end_date": effective_end_date})
#         portfolio_body.update({"created_ts": created_ts})
#         portfolio_body.update({"action_by": created_by})
#         portfoliodata.append(portfolio_body)
#         index += 1
#     return portfoliodata
#
#
# def get_security_list():
#     isin_list = []
#     index = 22
#     while df.iloc[index, 3] != "nan":
#         security_name = df.iloc[index, 1]
#         security_isin = get_isin(security_name)
#         exposure = float(df.iloc[index, 3])
#         isin_list.append({"security_name": security_name, "security_isin":security_isin, "exposure": exposure})
#         index += 1
#     return isin_list
#
#
# def get_fund_sector(security_list):
#     sector_breakdown = []
#     sector_cursor = database.cursor()
#     for securityData in security_list:
#         sector_body = {"security": securityData["security_name"], "isin": securityData["security_isin"],
#                        "sector": None, "exposure": securityData["exposure"]}
#         if securityData["security_isin"] != "CASH":
#             sector_query = "select ms.sector_type_name as sector from mas_securities msec, mas_sectors ms where " \
#                            "msec.security_isin = '" + securityData["security_isin"]+ "' and ms.industry = " \
#                                                                                      "msec.industry and ms.isActive = 1"
#         else:
#             sector_query = "SELECT sector_type_name as sector FROM mas_sectors where industry = '" + \
#                            securityData["security_isin"] + "'"
#         sector_cursor.execute(sector_query)
#         sector_response = sector_cursor.fetchall()
#         sector_body["sector"] = sector_response[0][0]
#         sector_breakdown.append(sector_body)
#     sector_breakdown_result = {}
#     sum = 0
#     for i in sector_breakdown:
#         sum += i['exposure']
#         if sector_breakdown_result.__contains__(i["sector"]):
#             sector_breakdown_result[i["sector"]] += i["exposure"]
#         else:
#             sector_breakdown_result.update({i["sector"]: i["exposure"]})
#     return sector_breakdown_result
#
#
# def put_into_fintuple_db():
#     update_islatest()
#     # get fund performance
#     fund_code, current_aum, no_of_clients, market_cap_type_code, portfolio_equity_allocation, \
#     portfolio_cash_allocation, portfolio_asset_allocation, perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, perf_3y, \
#     perf_5y, perf_inception, isLatest, effective_start_date, effective_end_date, created_ts, created_by, \
#     fund_nav = get_fund_performance()
#     # get benchmark performance
#     benchmark_perf_1m, benchmark_perf_3m, benchmark_perf_6m, benchmark_perf_1y, benchmark_perf_2y, benchmark_perf_3y, \
#     benchmark_perf_5y, benchmark_perf_inception = get_benchmark_performance()
#     # get alternate benchmark performance
#     alt_benchmark_perf_1m, alt_benchmark_perf_3m, alt_benchmark_perf_6m, alt_benchmark_perf_1y, alt_benchmark_perf_2y, \
#     alt_benchmark_perf_3y, alt_benchmark_perf_5y, alt_benchmark_perf_inception = get_alt_benchmark_performance()
#     benchmark_index_code = get_benchmark_index()
#     alt_benchmark_index_code = get_alt_benchmark_index()
#     benchmark_nav, previous_benchmark_nav = get_benchmark_nav()
#     alt_benchmark_nav, alt_previous_benchmark_nav = get_alt_benchmark_nav()
#     marketcapData = get_market_cap()
#     portfolioData = get_fund_portfolio()
#     securityList = get_security_list()
#     sectorData = get_fund_sector(securityList)
#     sectorDataList = []
#     fundData = {}
#     navData = {}
#     fundData.update({"fund_code": fund_code, "current_aum": current_aum, "no_of_clients": no_of_clients,
#                      "market_cap_type_code": market_cap_type_code,
#                      "portfolio_equity_allocation": portfolio_equity_allocation,
#                      "portfolio_cash_allocation": portfolio_cash_allocation,
#                      "portfolio_asset_allocation": portfolio_asset_allocation, "perf_1m": perf_1m,
#                      "perf_3m": perf_3m, "perf_6m": perf_6m, "perf_1y": perf_1y, "perf_2y": perf_2y,
#                      "perf_3y": perf_3y, "perf_5y": perf_5y, "perf_inception": perf_inception, "isLatest": isLatest,
#                      "effective_start_date": effective_start_date, "effective_end_date": effective_end_date,
#                      "created_ts": created_ts, "created_by": created_by, "benchmark_perf_1m": benchmark_perf_1m,
#                      "benchmark_perf_3m": benchmark_perf_3m, "benchmark_perf_6m": benchmark_perf_6m,
#                      "benchmark_perf_1y": benchmark_perf_1y, "benchmark_perf_2y": benchmark_perf_2y,
#                      "benchmark_perf_3y": benchmark_perf_3y, "benchmark_perf_5y": benchmark_perf_5y,
#                      "benchmark_perf_inception": benchmark_perf_inception,
#                      "alt_benchmark_perf_1m": alt_benchmark_perf_1m, "alt_benchmark_perf_3m": alt_benchmark_perf_3m,
#                      "alt_benchmark_perf_6m": alt_benchmark_perf_6m, "alt_benchmark_perf_1y": alt_benchmark_perf_1y,
#                      "alt_benchmark_perf_2y": alt_benchmark_perf_2y, "alt_benchmark_perf_3y": alt_benchmark_perf_3y,
#                      "alt_benchmark_perf_5y": alt_benchmark_perf_5y,
#                      "alt_benchmark_perf_inception": alt_benchmark_perf_inception})
#     navData.update({"fund_code": fund_code, "benchmark_index_code": benchmark_index_code,
#                     "alt_benchmark_index_code": alt_benchmark_index_code, "fund_nav": fund_nav,
#                     "benchmark_nav": benchmark_nav, "alt_benchmark_nav": alt_benchmark_nav,
#                     "effective_end_date": effective_end_date})
#     for sector_name, exposure in sectorData.items():
#         sectorBody = {"fund_code": fund_code, "sector_type_name": sector_name, "exposure": round(exposure, 4),
#                       "start_date": effective_start_date, "end_date": effective_end_date, "created_ts": created_ts,
#                       "action_by": created_by}
#         sectorDataList.append(sectorBody)
#     return fundData, navData, marketcapData, portfolioData, sectorDataList
#
#
# try:
#     sheet_names = ["Flexi-cap", "Value", "Largecap", "Contra"]
#     os.chdir(r"C:\Users\pavithra\PycharmProjects\data_automation\excel files")
#     files = []
#     for file in glob.glob("*.xlsx"):
#         files.append(file)
#     for file in files:
#         for sheet in sheet_names:
#             df_read = pd.read_excel(file, sheet_name=sheet)
#             file_name = os.path.splitext(file)[0]
#             if " (1)" in file_name:
#                 file_name = file_name.replace(" (1)", "")
#             file_date = file_name.split('-')[1].strip()
#             df_str = df_read.astype(str)
#             df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x))
#             db_host, db_user, db_pass, db_name = env('DB_HOST'), env('DB_USER'), env('DB_PASS'), env('DB_NAME')
#             database = MySQLdb.connect(db_host, db_user, db_pass, db_name, use_unicode=True, charset="utf8")
#             fund_list = get_funds_list(get_inst_details("ICICI"))
#             fund_data, nav_data, marketcap_data, portfolioData, sectorDataList = put_into_fintuple_db()
#             put_fund_performance(fund_data, database)
#             put_nav_data(nav_data, database)
#             put_market_cap_data(marketcap_data, database)
#             put_fund_portfolio(portfolioData, database)
#             put_fund_sector(sectorDataList, database)
#             print(file_date, ": Fund code - ", fund_data['fund_code'], "Record inserted successfully")
#             database.commit()
#             database.close()
#
# except Exception as error:
#     print("Exception raised :", error)
