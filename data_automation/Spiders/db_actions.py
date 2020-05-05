import datetime


def get_inst_details(key_term, database):
    inst_cursor = database.cursor()
    inst_query = "SELECT inst_code FROM per_all_institutions where inst_display_name like '%" + key_term + "%' "
    inst_cursor.execute(inst_query)
    inst_details = inst_cursor.fetchall()
    inst_code = inst_details[0][0]
    inst_cursor.close()
    return inst_code


def get_funds_list(inst_code, database):
    fund_cursor = database.cursor()
    fund_query = "SELECT paf.fund_code, paf.inst_code, paf.fund_name, paf.fund_type_code FROM per_all_funds paf, " \
                 "per_all_institutions pai where pai.inst_code = paf.inst_code and pai.inst_code='" + inst_code + "' "
    fund_cursor.execute(fund_query)
    funds_list = fund_cursor.fetchall()
    fund_cursor.close()
    return funds_list


def get_benchmark_index(fund_code, database, end_date):
    benchmark_index_cursor = database.cursor()
    benchmark_index_query = "SELECT benchmark_index_code FROM fund_benchmark_nav where fund_code = '" + \
                            fund_code + "' and effective_end_date = '" + str(end_date) + "'"
    benchmark_index_cursor.execute(benchmark_index_query)
    benchmark_index_details = benchmark_index_cursor.fetchall()
    benchmark_index_code = benchmark_index_details[0][0]
    benchmark_index_cursor.close()
    return benchmark_index_code


def get_index_price(benchmark_index, database, effective_last_date):
    index_price_cursor = database.cursor()
    index_price_query = "SELECT index_price_close FROM index_prices where index_code = '" + benchmark_index + \
                        "' and index_price_as_on_date = '" + str(effective_last_date) + "'"
    index_price_cursor.execute(index_price_query)
    index_price_details = index_price_cursor.fetchall()
    index_price = index_price_details[0][0]
    index_price_cursor.close()
    return index_price


def get_previous_index_price(benchmark_index, database, previous_month_end_date):
    previous_index_price_cursor = database.cursor()
    previous_index_price_query = "SELECT index_price_close FROM index_prices where index_code = '" + \
                                 benchmark_index + "' and index_price_as_on_date = '" + \
                                 str(previous_month_end_date) + "'"
    previous_index_price_cursor.execute(previous_index_price_query)
    previous_index_price_details = previous_index_price_cursor.fetchall()
    previous_index_price = previous_index_price_details[0][0]
    previous_index_price_cursor.close()
    return previous_index_price


def get_benchmark_nav(fund_code, database, previous_month_end_date):
    benchmark_nav_cursor = database.cursor()
    benchmark_nav_query = "SELECT benchmark_nav FROM fund_benchmark_nav where fund_code = '" + \
                          fund_code + "' and effective_end_date = '" + \
                          str(previous_month_end_date) + "'"
    benchmark_nav_cursor.execute(benchmark_nav_query)
    benchmark_nav_details = benchmark_nav_cursor.fetchall()
    benchmark_previous_nav = benchmark_nav_details[0][0]
    benchmark_nav_cursor.close()
    return benchmark_previous_nav


def get_alt_benchmark_index(fund_code, database, end_date):
    alt_benchmark_index_cursor = database.cursor()
    alt_benchmark_index_query = "SELECT alt_benchmark_index_code FROM fund_benchmark_nav where fund_code = '" + \
                                fund_code + "' and effective_end_date = '" + str(end_date) + "'"
    alt_benchmark_index_cursor.execute(alt_benchmark_index_query)
    alt_benchmark_index_details = alt_benchmark_index_cursor.fetchall()
    alt_benchmark_index_code = alt_benchmark_index_details[0][0]
    alt_benchmark_index_cursor.close()
    return alt_benchmark_index_code


def get_alt_index_price(alt_benchmark_index, database, effective_last_date):
    alt_index_price_cursor = database.cursor()
    alt_index_price_query = "SELECT index_price_close FROM index_prices where index_code = '" + \
                            alt_benchmark_index + "' and index_price_as_on_date = '" + str(effective_last_date) \
                            + "'"
    alt_index_price_cursor.execute(alt_index_price_query)
    alt_index_price_details = alt_index_price_cursor.fetchall()
    alt_index_price = alt_index_price_details[0][0]
    alt_index_price_cursor.close()
    return alt_index_price


def get_alt_previous_index_price(alt_benchmark_index, database, alt_previous_month_end_date):
    alt_previous_index_price_cursor = database.cursor()
    alt_previous_index_price_query = "SELECT index_price_close FROM index_prices where index_code = '" + \
                                     alt_benchmark_index + "' and index_price_as_on_date = '" + \
                                     str(alt_previous_month_end_date) + "'"
    alt_previous_index_price_cursor.execute(alt_previous_index_price_query)
    alt_previous_index_price_details = alt_previous_index_price_cursor.fetchall()
    alt_previous_index_price = alt_previous_index_price_details[0][0]
    alt_previous_index_price_cursor.close()
    return alt_previous_index_price


def get_alt_benchmark_nav(fund_code, database, alt_previous_month_end_date):
    alt_benchmark_nav_cursor = database.cursor()
    alt_benchmark_nav_query = "SELECT alt_benchmark_nav FROM fund_benchmark_nav where fund_code = '" + \
                              fund_code + "' and effective_end_date = '" + \
                              str(alt_previous_month_end_date) + "'"
    alt_benchmark_nav_cursor.execute(alt_benchmark_nav_query)
    alt_benchmark_nav_details = alt_benchmark_nav_cursor.fetchall()
    alt_benchmark_previous_nav = alt_benchmark_nav_details[0][0]
    alt_benchmark_nav_cursor.close()
    return alt_benchmark_previous_nav


def get_inception_date(fund_code, database):
    since_inception_cursor = database.cursor()
    since_inception_query = "SELECT nav_start_date from per_all_funds where fund_code = '" + fund_code + "'"
    since_inception_cursor.execute(since_inception_query)
    inception_date = since_inception_cursor.fetchall()
    since_inception_cursor.close()
    temp = str(inception_date[0][0])
    inception_date = datetime.datetime.strptime(temp, '%Y-%m-%d').date()
    return inception_date


def update_islatest(database, previous_1m_end_date):
    update_cursor = database.cursor()
    update_query = "UPDATE fund_performance SET isLatest = NULL where effective_end_date = '" + \
                   str(previous_1m_end_date) + "'"
    update_cursor.execute(update_query)


def get_previous_1m_nav(fund_code, previous_1m_end_date, database):
    previous_1m_cursor = database.cursor()
    previous_1m_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
                        str(previous_1m_end_date) + "' and fund_code = '" + fund_code + "'"
    previous_1m_cursor.execute(previous_1m_query)
    previous_1m_nav = previous_1m_cursor.fetchall()
    previous_1m_cursor.close()
    return previous_1m_nav


def get_previous_3m_nav(fund_code, previous_3m_end_date, database):
    previous_3m_cursor = database.cursor()
    previous_3m_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
                        str(previous_3m_end_date) + "' and fund_code = '" + fund_code + "'"
    previous_3m_cursor.execute(previous_3m_query)
    previous_3m = previous_3m_cursor.fetchall()
    previous_3m_cursor.close()
    return previous_3m


def get_previous_6m_nav(fund_code, previous_6m_end_date, database):
    previous_6m_cursor = database.cursor()
    previous_6m_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
                        str(previous_6m_end_date) + "' and fund_code = '" + fund_code + "'"
    previous_6m_cursor.execute(previous_6m_query)
    previous_6m = previous_6m_cursor.fetchall()
    previous_6m_cursor.close()
    return previous_6m


def get_previous_1y_nav(fund_code, previous_1y_end_date, database):
    previous_1y_cursor = database.cursor()
    previous_1y_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
                        str(previous_1y_end_date) + "' and fund_code = '" + fund_code + "'"
    previous_1y_cursor.execute(previous_1y_query)
    previous_1y = previous_1y_cursor.fetchall()
    previous_1y_cursor.close()
    return previous_1y


def get_previous_2y_nav(fund_code, previous_2y_end_date, database):
    previous_2y_cursor = database.cursor()
    previous_2y_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
                        str(previous_2y_end_date) + "' and fund_code = '" + fund_code + "'"
    previous_2y_cursor.execute(previous_2y_query)
    previous_2y = previous_2y_cursor.fetchall()
    previous_2y_cursor.close()
    return previous_2y


def get_previous_3y_nav(fund_code, previous_3y_end_date, database):
    previous_3y_cursor = database.cursor()
    previous_3y_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
                        str(previous_3y_end_date) + "' and fund_code = '" + fund_code + "'"
    previous_3y_cursor.execute(previous_3y_query)
    previous_3y = previous_3y_cursor.fetchall()
    previous_3y_cursor.close()
    return previous_3y


def get_previous_5y_nav(fund_code, previous_5y_end_date, database):
    previous_5y_cursor = database.cursor()
    previous_5y_query = "SELECT fund_nav from fund_benchmark_nav where effective_end_date = '" + \
                        str(previous_5y_end_date) + "' and fund_code = '" + fund_code + "'"
    previous_5y_cursor.execute(previous_5y_query)
    previous_5y = previous_5y_cursor.fetchall()
    previous_5y_cursor.close()
    return previous_5y


def get_benchmark_3m_nav(fund_code, benchmark_index_code, benchmark_3m_end_date, database):
    benchmark_3m_cursor = database.cursor()
    benchmark_3m_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                         str(benchmark_3m_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
                         + "' and fund_code = '" + fund_code + "' "
    benchmark_3m_cursor.execute(benchmark_3m_query)
    benchmark_3m = benchmark_3m_cursor.fetchall()
    benchmark_3m_cursor.close()
    return benchmark_3m


def get_benchmark_6m_nav(fund_code, benchmark_index_code, benchmark_6m_end_date, database):
    benchmark_6m_cursor = database.cursor()
    benchmark_6m_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                         str(benchmark_6m_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
                         + "' and fund_code = '" + fund_code + "' "
    benchmark_6m_cursor.execute(benchmark_6m_query)
    benchmark_6m = benchmark_6m_cursor.fetchall()
    benchmark_6m_cursor.close()
    return benchmark_6m


def get_benchmark_1y_nav(fund_code, benchmark_index_code, benchmark_1y_end_date, database):
    benchmark_1y_cursor = database.cursor()
    benchmark_1y_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                         str(benchmark_1y_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
                         + "' and fund_code = '" + fund_code + "' "
    benchmark_1y_cursor.execute(benchmark_1y_query)
    benchmark_1y = benchmark_1y_cursor.fetchall()
    benchmark_1y_cursor.close()
    return benchmark_1y


def get_benchmark_2y_nav(fund_code, benchmark_index_code, benchmark_2y_end_date, database):
    benchmark_2y_cursor = database.cursor()
    benchmark_2y_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                         str(benchmark_2y_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
                         + "' and fund_code = '" + fund_code + "' "
    benchmark_2y_cursor.execute(benchmark_2y_query)
    benchmark_2y = benchmark_2y_cursor.fetchall()
    benchmark_2y_cursor.close()
    return benchmark_2y


def get_benchmark_3y_nav(fund_code, benchmark_index_code, benchmark_3y_end_date, database):
    benchmark_3y_cursor = database.cursor()
    benchmark_3y_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                         str(benchmark_3y_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
                         + "' and fund_code = '" + fund_code + "' "
    benchmark_3y_cursor.execute(benchmark_3y_query)
    benchmark_3y = benchmark_3y_cursor.fetchall()
    benchmark_3y_cursor.close()
    return benchmark_3y


def get_benchmark_5y_nav(fund_code, benchmark_index_code, benchmark_5y_end_date, database):
    benchmark_5y_cursor = database.cursor()
    benchmark_5y_query = "SELECT benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                         str(benchmark_5y_end_date) + "' and benchmark_index_code = '" + benchmark_index_code \
                         + "' and fund_code = '" + fund_code + "' "
    benchmark_5y_cursor.execute(benchmark_5y_query)
    benchmark_5y = benchmark_5y_cursor.fetchall()
    benchmark_5y_cursor.close()
    return benchmark_5y


def get_alt_benchmark_3m_nav(fund_code, alt_benchmark_index_code, alt_benchmark_3m_end_date, database):
    alt_benchmark_3m_cursor = database.cursor()
    alt_benchmark_3m_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_3m_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_3m_cursor.execute(alt_benchmark_3m_query)
    alt_benchmark_3m = alt_benchmark_3m_cursor.fetchall()
    alt_benchmark_3m_cursor.close()
    return alt_benchmark_3m


def get_alt_benchmark_6m_nav(fund_code, alt_benchmark_index_code, alt_benchmark_6m_end_date, database):
    alt_benchmark_6m_cursor = database.cursor()
    alt_benchmark_6m_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_6m_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_6m_cursor.execute(alt_benchmark_6m_query)
    alt_benchmark_6m = alt_benchmark_6m_cursor.fetchall()
    alt_benchmark_6m_cursor.close()
    return alt_benchmark_6m


def get_alt_benchmark_1y_nav(fund_code, alt_benchmark_index_code, alt_benchmark_1y_end_date, database):
    alt_benchmark_1y_cursor = database.cursor()
    alt_benchmark_1y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_1y_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_1y_cursor.execute(alt_benchmark_1y_query)
    alt_benchmark_1y = alt_benchmark_1y_cursor.fetchall()
    alt_benchmark_1y_cursor.close()
    return alt_benchmark_1y


def get_alt_benchmark_2y_nav(fund_code, alt_benchmark_index_code, alt_benchmark_2y_end_date, database):
    alt_benchmark_2y_cursor = database.cursor()
    alt_benchmark_2y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_2y_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_2y_cursor.execute(alt_benchmark_2y_query)
    alt_benchmark_2y = alt_benchmark_2y_cursor.fetchall()
    alt_benchmark_2y_cursor.close()
    return alt_benchmark_2y


def get_alt_benchmark_3y_nav(fund_code, alt_benchmark_index_code, alt_benchmark_3y_end_date, database):
    alt_benchmark_3y_cursor = database.cursor()
    alt_benchmark_3y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_3y_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_3y_cursor.execute(alt_benchmark_3y_query)
    alt_benchmark_3y = alt_benchmark_3y_cursor.fetchall()
    alt_benchmark_3y_cursor.close()
    return alt_benchmark_3y


def get_alt_benchmark_5y_nav(fund_code, alt_benchmark_index_code, alt_benchmark_5y_end_date, database):
    alt_benchmark_5y_cursor = database.cursor()
    alt_benchmark_5y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_5y_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_benchmark_index_code + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_5y_cursor.execute(alt_benchmark_5y_query)
    alt_benchmark_5y = alt_benchmark_5y_cursor.fetchall()
    alt_benchmark_5y_cursor.close()
    return alt_benchmark_5y


def get_isin_sector(security_name, database):
    security_cursor = database.cursor()
    security_query = "SELECT security_isin from mas_securities where security_name = '" + security_name + "'"
    security_cursor.execute(security_query)
    isin_details = security_cursor.fetchall()
    security_cursor.close()
    return isin_details


def get_all_isin(database):
    isin_cursor = database.cursor()
    isin_query = "SELECT security_isin, security_name from mas_securities"
    isin_cursor.execute(isin_query)
    security_details = isin_cursor.fetchall()
    isin_cursor.close()
    return security_details


def get_sector_type(sec_isin, database):
    sector_cursor = database.cursor()
    sector_query = "select ms.sector_type_name as sector from mas_securities msec, mas_sectors ms where " \
                   "msec.security_isin = '" + sec_isin + "' and ms.industry = msec.industry and ms.isActive = 1"
    sector_cursor.execute(sector_query)
    sector_response = sector_cursor.fetchall()
    sector_cursor.close()
    return sector_response


def get_sector_cash_type(sec_isin, database):
    sector_cash_cursor = database.cursor()
    sector_query = "SELECT sector_type_name as sector FROM mas_sectors where industry = '" + sec_isin + "'"
    sector_cash_cursor.execute(sector_query)
    sector_cash_response = sector_cash_cursor.fetchall()
    sector_cash_cursor.close()
    return sector_cash_response


def put_fund_performance(fundData, database):
    fund_cursor = database.cursor()
    insert_query = "INSERT INTO fund_performance (fund_code, current_aum, no_of_clients, market_cap_type_code, " \
                   "portfolio_equity_allocation, portfolio_cash_allocation, portfolio_asset_allocation, perf_1m, " \
                   "perf_3m, perf_6m, perf_1y, perf_2y, perf_3y, perf_5y, perf_inception, benchmark_perf_1m, " \
                   "benchmark_perf_3m, benchmark_perf_6m, benchmark_perf_1y, benchmark_perf_2y, benchmark_perf_3y, " \
                   "benchmark_perf_5y, benchmark_perf_inception, alt_benchmark_perf_1m, alt_benchmark_perf_3m, " \
                   "alt_benchmark_perf_6m, alt_benchmark_perf_1y, alt_benchmark_perf_2y, alt_benchmark_perf_3y, " \
                   "alt_benchmark_perf_5y, alt_benchmark_perf_inception, isLatest, effective_start_date, " \
                   "effective_end_date, created_ts, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                   "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                   "%s) "
    insert_values = (fundData['fund_code'], fundData['current_aum'], fundData['no_of_clients'],
                     fundData['market_cap_type_code'], fundData['portfolio_equity_allocation'],
                     fundData['portfolio_cash_allocation'], fundData['portfolio_asset_allocation'],
                     fundData['perf_1m'], fundData['perf_3m'], fundData['perf_6m'], fundData['perf_1y'],
                     fundData['perf_2y'], fundData['perf_3y'], fundData['perf_5y'], fundData['perf_inception'],
                     fundData['benchmark_perf_1m'], fundData['benchmark_perf_3m'], fundData['benchmark_perf_6m'],
                     fundData['benchmark_perf_1y'], fundData['benchmark_perf_2y'], fundData['benchmark_perf_3y'],
                     fundData['benchmark_perf_5y'], fundData['benchmark_perf_inception'],
                     fundData['alt_benchmark_perf_1m'], fundData['alt_benchmark_perf_3m'],
                     fundData['alt_benchmark_perf_6m'], fundData['alt_benchmark_perf_1y'],
                     fundData['alt_benchmark_perf_2y'], fundData['alt_benchmark_perf_3y'],
                     fundData['alt_benchmark_perf_5y'], fundData['alt_benchmark_perf_inception'], fundData['isLatest'],
                     fundData['effective_start_date'], fundData['effective_end_date'], fundData['created_ts'],
                     fundData['created_by'])
    fund_cursor.execute(insert_query, insert_values)
    fund_cursor.close()


def put_nav_data(navData, database):
    nav_cursor = database.cursor()
    nav_query = "INSERT INTO fund_benchmark_nav (fund_code, benchmark_index_code, alt_benchmark_index_code, " \
                "fund_nav, benchmark_nav, alt_benchmark_nav, effective_end_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    nav_values = (navData['fund_code'], navData['benchmark_index_code'], navData['alt_benchmark_index_code'],
                  navData['fund_nav'], navData['benchmark_nav'], navData['alt_benchmark_nav'],
                  navData['effective_end_date'])
    nav_cursor.execute(nav_query, nav_values)
    nav_cursor.close()


def put_market_cap_data(marketcapData, database):
    market_cap_cursor = database.cursor()
    for data in marketcapData:
        market_cap_query = "INSERT INTO fund_market_cap_details (fund_code, type_market_cap, exposure, start_date, " \
                           "end_date, created_ts, action_by) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        market_cap_values = (data['fund_code'], data['type_market_cap'], data['exposure'], data['start_date'],
                             data['end_date'], data['created_ts'], data['action_by'])
        market_cap_cursor.execute(market_cap_query, market_cap_values)
    market_cap_cursor.close()


def put_fund_portfolio(portfolioData, database):
    portfolio_cursor = database.cursor()
    for data in portfolioData:
        portfolio_query = "INSERT INTO fund_portfolio_details (fund_code, security_isin, exposure, start_date, " \
                          "end_date, created_ts, action_by) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        portfolio_values = (data['fund_code'], data['security_isin'], data['exposure'], data['start_date'],
                            data['end_date'], data['created_ts'], data['action_by'])
        portfolio_cursor.execute(portfolio_query, portfolio_values)
    portfolio_cursor.close()


def put_fund_sector(sectorDataList, database):
    sector_cursor = database.cursor()
    for data in sectorDataList:
        sector_query = "INSERT INTO fund_sector_details (fund_code, sector_type_name, exposure, start_date, " \
                       "end_date, created_ts, action_by) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        sector_values = (data['fund_code'], data['sector_type_name'], data['exposure'], data['start_date'],
                         data['end_date'], data['created_ts'], data['action_by'])
        sector_cursor.execute(sector_query, sector_values)
    sector_cursor.close()
