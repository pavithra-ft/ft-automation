# def get_mas_indices(iq_database):
#     mas_indices_cursor = iq_database.cursor()
#     mas_indices_query = "SELECT distinct(index_code) from iq.mas_indices"
#     mas_indices_cursor.execute(mas_indices_query)
#     mas_indices_details = mas_indices_cursor.fetchall()
#     mas_indices = []
#     for index in mas_indices_details:
#         mas_indices.append(index[0])
#     mas_indices_cursor.close()
#     return mas_indices
#
#
# def get_index_start_price(start_date, index_code, iq_database):
#     start_price_cursor = iq_database.cursor()
#     start_index_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + \
#                               index_code + "' and index_price_as_on_date = '" + str(start_date) + "'"
#     start_price_cursor.execute(start_index_price_query)
#     start_index_price_details = start_price_cursor.fetchall()
#     start_index_price = start_index_price_details[0][0]
#     start_price_cursor.close()
#     return start_index_price
#
#
# def get_index_start_date(index_code, database):
#     start_date_cursor = database.cursor()
#     start_date_query = "SELECT index_price_as_on_date FROM iq.index_prices where index_code ='" + index_code \
#                        + "' order by index_price_as_on_date asc limit 1"
#     start_date_cursor.execute(start_date_query)
#     start_date = start_date_cursor.fetchall()
#     start_date_cursor.close()
#     return start_date[0][0]
#
#
# def get_index_price_as_on_date(date, index_code, iq_database):
#     index_price_cursor = iq_database.cursor()
#     index_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
#                         + "' and year(ip.index_price_as_on_date) = year('" + str(date) \
#                         + "') and month(ip.index_price_as_on_date) = month('" + str(date) \
#                         + "') order by ip.index_price_as_on_date desc limit 1"
#     index_price_cursor.execute(index_price_query)
#     index_price = index_price_cursor.fetchall()
#     index_price_cursor.close()
#     return index_price
#
#
# def get_security_isin(security_name, iq_database):
#     security_cursor = iq_database.cursor()
#     security_query = "SELECT security_isin from iq.mas_securities where security_name = '" + security_name + "'"
#     security_cursor.execute(security_query)
#     isin_details = security_cursor.fetchall()
#     security_cursor.close()
#     return isin_details
#
#
# def get_all_isin(iq_database):
#     isin_cursor = iq_database.cursor()
#     isin_query = "SELECT security_isin, security_name from iq.mas_securities"
#     isin_cursor.execute(isin_query)
#     security_details = isin_cursor.fetchall()
#     isin_cursor.close()
#     return security_details
#
#
# def get_security_sector(industry, iq_database):
#     industry_cursor = iq_database.cursor()
#     industry_query = "SELECT sector from iq.mas_sectors where industry = '" + industry + "'"
#     industry_cursor.execute(industry_query)
#     sector_details = industry_cursor.fetchall()
#     industry_cursor.close()
#     return sector_details[0][0]
#
#
# def is_index_performance_exist(index_code, reporting_date, iq_database):
#     is_index_cursor = iq_database.cursor()
#     is_index_query = "SELECT count(*) from iq.index_performance where index_code = '" + index_code \
#                      + "' and reporting_date = '" + str(reporting_date) + "'"
#     is_index_cursor.execute(is_index_query)
#     index_details = is_index_cursor.fetchall()
#     return index_details[0][0]
#
#
# def put_index_performance(index_perf_data, iq_database):
#     index_perf_cursor = iq_database.cursor()
#     for data in index_perf_data:
#         if is_index_performance_exist(data['index_code'], data['reporting_date'], iq_database):
#             index_perf_query = "UPDATE iq.index_performance SET index_code = %s, standard_deviation = %s," \
#                                "pe_ratio = %s, top_sector_name = %s, top_sector_exposure = %s, top_holding_isin = %s," \
#                                " top_holding_exposure = %s, perf_1m = %s, perf_3m = %s, perf_6m = %s, perf_1y = %s, " \
#                                "perf_2y = %s, perf_3y = %s, perf_5y = %s, perf_inception = %s, reporting_date = %s " \
#                                "where reporting_date = '" + str(data['reporting_date']) + "' and index_code = '" + \
#                                data['index_code'] + "'"
#         else:
#             index_perf_query = "INSERT INTO iq.index_performance (index_code, standard_deviation, pe_ratio, " \
#                                "top_sector_name, top_sector_exposure, top_holding_isin, top_holding_exposure, " \
#                                "perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, perf_3y, perf_5y, perf_inception, " \
#                                "reporting_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#
#         index_perf_values = (data['index_code'], data['standard_deviation'], data['pe_ratio'], data['top_sector_name'],
#                              data['top_sector_exposure'], data['top_holding_isin'], data['top_holding_exposure'],
#                              data['perf_1m'], data['perf_3m'], data['perf_6m'], data['perf_1y'], data['perf_2y'],
#                              data['perf_3y'], data['perf_5y'], data['perf_inception'], data['reporting_date'])
#         index_perf_cursor.execute(index_perf_query, index_perf_values)
#     index_perf_cursor.close()
#
#
# def put_mas_securities(mas_security_ratio_list, iq_database):
#     security_ratio_cursor = iq_database.cursor()
#     for ratio in mas_security_ratio_list:
#         print(ratio)
#         index_perf_query = "UPDATE iq.mas_securities SET market_cap_value = %s, pe_ratio = %s," \
#                            "pb_ratio = %s, eps = %s, dividend_yield = %s where security_isin = '" + \
#                            ratio['security_isin'] + "'"
#         index_perf_values = (ratio['market_cap_value'], ratio['pe_ratio'], ratio['pb_ratio'], ratio['eps'],
#                              ratio['dividend_yield'])
#         security_ratio_cursor.execute(index_perf_query, index_perf_values)
#     security_ratio_cursor.close()
#
#
# def put_index_prices(index_price_data, iq_database):
#     index_price_cursor = iq_database.cursor()
#     for index in index_price_data:
#         index_price_query = "INSERT INTO iq.index_prices (index_code, index_price_open, index_price_high, " \
#                             "index_price_low, index_price_close, index_price_as_on_date) VALUES (%s, %s, %s, %s, %s, " \
#                             "%s)"
#         index_price_values = (index['index_code'], index['Open'], index['High'], index['Low'], index['Close'],
#                               index['Date'])
#         index_price_cursor.execute(index_price_query, index_price_values)
#     index_price_cursor.close()
