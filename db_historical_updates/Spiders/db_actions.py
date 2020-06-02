import datetime


def get_benchmark_info(fund_code, app_database):
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


def get_nav_dates(fund_code, iq_database):
    nav_dates_cursor = iq_database.cursor()
    nav_dates_query = "SELECT effective_end_date from iq.fund_benchmark_nav where fund_code = '" \
                      + fund_code + "' order by effective_end_date"
    nav_dates_cursor.execute(nav_dates_query)
    nav_dates = nav_dates_cursor.fetchall()
    nav_dates_list = [date[0] for date in nav_dates]
    return nav_dates_list


def get_alt_benchmark_info(fund_code, app_database):
    alt_benchmark_index_cursor = app_database.cursor()
    alt_benchmark_index_query = "SELECT fund_code, nav_start_date, benchmark_alt_index_code FROM " \
                                "app.per_all_funds where fund_code = '" + fund_code + "'"
    alt_benchmark_index_cursor.execute(alt_benchmark_index_query)
    alt_bm_details = alt_benchmark_index_cursor.fetchall()
    alt_benchmark_index_cursor.close()
    alt_benchmark = {}
    for details in alt_bm_details:
        alt_benchmark = {"fund_code": details[0], "nav_start_date": str(details[1]), "alt_bm_index": details[2]}
    return alt_benchmark


def get_fintuple_template_code(fs_database):
    template_cursor = fs_database.cursor()
    template_query = "SELECT template_code from fs.collateral_templates where template_type_code = 'FINTUPLE' order " \
                     "by template_code"
    template_cursor.execute(template_query)
    template_code = template_cursor.fetchall()
    template_code_list = list(template_code)
    return template_code_list


def get_collateral_data(template_code, fs_database):
    collateral_cursor = fs_database.cursor()
    collateral_query = "SELECT collateral_title, entity_code, reporting_date from fs.collaterals where " \
                       "template_code = '" + template_code + "' order by reporting_date"
    collateral_cursor.execute(collateral_query)
    collateral_details = collateral_cursor.fetchall()
    collateral_list = list(collateral_details)
    collateral_cursor.close()
    return collateral_list


def get_cap_type(type_desc, iq_database):
    cap_type_cursor = iq_database.cursor()
    cap_type_query = "SELECT market_cap_type_code from iq.mas_market_cap_types where market_cap_type_desc = '" + \
                     type_desc + "'"
    cap_type_cursor.execute(cap_type_query)
    cap_type_details = cap_type_cursor.fetchall()
    cap_type_code = cap_type_details[0][0]
    cap_type_cursor.close()
    return cap_type_code


def get_mas_indices(iq_database):
    mas_indices_cursor = iq_database.cursor()
    mas_indices_query = "SELECT distinct(index_code) from iq.mas_indices"
    mas_indices_cursor.execute(mas_indices_query)
    mas_indices_details = mas_indices_cursor.fetchall()
    mas_indices = []
    for index in mas_indices_details:
        mas_indices.append(index[0])
    mas_indices_cursor.close()
    return mas_indices


def get_start_price(start_date, index_code, iq_database):
    start_price_cursor = iq_database.cursor()
    start_index_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + \
                              index_code + "' and index_price_as_on_date = '" + str(start_date) + "'"
    start_price_cursor.execute(start_index_price_query)
    start_index_price_details = start_price_cursor.fetchall()
    start_index_price = start_index_price_details[0][0]
    start_price_cursor.close()
    return start_index_price


def get_index_start_date(index_code, iq_database):
    start_date_cursor = iq_database.cursor()
    start_date_query = "SELECT index_price_as_on_date FROM iq.index_prices where index_code ='" + index_code \
                       + "' order by index_price_as_on_date asc limit 1"
    start_date_cursor.execute(start_date_query)
    start_date = start_date_cursor.fetchall()
    start_date_cursor.close()
    return start_date[0][0]


def get_benchmark_index(fund_code, app_database):
    benchmark_index_cursor = app_database.cursor()
    benchmark_index_query = "SELECT benchmark_index_code FROM app.per_all_funds where fund_code = '" + fund_code + "'"
    benchmark_index_cursor.execute(benchmark_index_query)
    benchmark_index_details = benchmark_index_cursor.fetchall()
    benchmark_index_code = benchmark_index_details[0][0]
    benchmark_index_cursor.close()
    return benchmark_index_code


def get_alt_benchmark_index(fund_code, iq_database):
    alt_benchmark_index_cursor = iq_database.cursor()
    alt_benchmark_index_query = "SELECT benchmark_alt_index_code FROM app.per_all_funds where fund_code = '" + \
                                fund_code + "'"
    alt_benchmark_index_cursor.execute(alt_benchmark_index_query)
    alt_benchmark_index_details = alt_benchmark_index_cursor.fetchall()
    alt_benchmark_index_code = alt_benchmark_index_details[0][0]
    alt_benchmark_index_cursor.close()
    return alt_benchmark_index_code


def get_index_price_as_on_date(date, index_code, iq_database):
    index_price_cursor = iq_database.cursor()
    index_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                        + "' and year(ip.index_price_as_on_date) = year('" + str(date) \
                        + "') and month(ip.index_price_as_on_date) = month('" + str(date) \
                        + "') order by ip.index_price_as_on_date desc limit 1"
    index_price_cursor.execute(index_price_query)
    index_price = index_price_cursor.fetchall()
    index_price_cursor.close()
    return index_price


def get_benchmark_nav(fund_info, previous_1m_date, iq_database):
    benchmark_nav_cursor = iq_database.cursor()
    benchmark_nav_query = "SELECT benchmark_nav FROM iq.fund_benchmark_nav where fund_code = '" + \
                          fund_info["fund_code"] + "' and effective_end_date = '" + str(previous_1m_date) + "'"
    benchmark_nav_cursor.execute(benchmark_nav_query)
    benchmark_nav_details = benchmark_nav_cursor.fetchall()
    benchmark_previous_nav = benchmark_nav_details[0][0]
    benchmark_nav_cursor.close()
    return benchmark_previous_nav


def get_alt_benchmark_nav(fund_info, alt_previous_1m_date, iq_database):
    alt_benchmark_nav_cursor = iq_database.cursor()
    alt_benchmark_nav_query = "SELECT alt_benchmark_nav FROM iq.fund_benchmark_nav where fund_code = '" + \
                              fund_info["fund_code"] + "' and effective_end_date = '" + str(alt_previous_1m_date) + "'"
    alt_benchmark_nav_cursor.execute(alt_benchmark_nav_query)
    alt_benchmark_nav_details = alt_benchmark_nav_cursor.fetchall()
    alt_benchmark_previous_nav = alt_benchmark_nav_details[0][0]
    alt_benchmark_nav_cursor.close()
    return alt_benchmark_previous_nav


def get_nav_start_date(fund_code, app_database):
    nav_start_date_cursor = app_database.cursor()
    nav_start_date_query = "SELECT nav_start_date from app.per_all_funds where fund_code = '" + fund_code + "'"
    nav_start_date_cursor.execute(nav_start_date_query)
    nav_start_date = nav_start_date_cursor.fetchall()
    temp = str(nav_start_date[0][0])
    nav_start_date_cursor.close()
    nav_start_date = datetime.datetime.strptime(temp, '%Y-%m-%d').date()
    return nav_start_date


def get_investment_style(fund_code, app_database):
    investment_style_cursor = app_database.cursor()
    investment_style_query = "SELECT investment_style FROM app.per_all_funds where fund_code = '" + fund_code + "'"
    investment_style_cursor.execute(investment_style_query)
    investment_style_details = investment_style_cursor.fetchall()
    investment_style = investment_style_details[0][0]
    investment_style_cursor.close()
    return investment_style


def get_fund_nav(fund_code, date, iq_database):
    fund_1m_cursor = iq_database.cursor()
    fund_1m_query = "SELECT fund_nav from iq.fund_benchmark_nav where effective_end_date = '" + \
                    str(date) + "' and fund_code = '" + fund_code + "'"
    fund_1m_cursor.execute(fund_1m_query)
    fund_1m_nav = fund_1m_cursor.fetchall()
    fund_1m_cursor.close()
    return fund_1m_nav


def get_current_fund_nav(fund_code, date, iq_database):
    fund_1m_cursor = iq_database.cursor()
    fund_1m_query = "SELECT fund_nav from iq.fund_benchmark_nav where effective_end_date = '" + \
                    str(date) + "' and fund_code = '" + fund_code + "'"
    fund_1m_cursor.execute(fund_1m_query)
    fund_1m_nav = fund_1m_cursor.fetchall()
    fund_1m_cursor.close()
    return fund_1m_nav


def get_isin_sector(security_name, iq_database):
    security_cursor = iq_database.cursor()
    security_query = "SELECT security_isin from iq.mas_securities where security_name = '" + security_name \
                     + "' or bse_security_symbol = '" + security_name + "'"
    security_cursor.execute(security_query)
    isin_details = security_cursor.fetchall()
    security_cursor.close()
    return isin_details


def get_all_isin(iq_database):
    isin_cursor = iq_database.cursor()
    isin_query = "SELECT security_isin, security_name from iq.mas_securities"
    isin_cursor.execute(isin_query)
    security_details = isin_cursor.fetchall()
    isin_cursor.close()
    return security_details


def get_sector_from_portfolio(sec_isin, iq_database):
    sector_cursor = iq_database.cursor()
    sector_query = "select ms.sector as sector from iq.mas_securities msec, iq.mas_sectors ms where " \
                   "msec.security_isin = '" + sec_isin + "' and ms.industry = msec.industry"
    sector_cursor.execute(sector_query)
    sector_response = sector_cursor.fetchall()
    sector_cursor.close()
    return sector_response


def get_sector_from_industry(industry, iq_database):
    industry_cursor = iq_database.cursor()
    industry_query = "SELECT sector from iq.mas_sectors where industry = '" + industry + "'"
    industry_cursor.execute(industry_query)
    sector_details = industry_cursor.fetchall()
    industry_cursor.close()
    return sector_details


def get_fund_short_code(fund_code, app_database):
    short_code_cursor = app_database.cursor()
    short_code_query = "SELECT fund_short_code from app.per_all_funds where fund_code = '" + fund_code + "'"
    short_code_cursor.execute(short_code_query)
    short_code_details = short_code_cursor.fetchall()
    fund_short_code = short_code_details[0][0]
    short_code_cursor.close()
    return fund_short_code


def get_collateral_code(fs_database):
    collateral_code_cursor = fs_database.cursor()
    collateral_code_query = "SELECT fs.codeGenerator('COLLATERAL')"
    collateral_code_cursor.execute(collateral_code_query)
    collateral_code_details = collateral_code_cursor.fetchall()
    collateral_code_cursor.close()
    collateral_code = collateral_code_details[0][0]
    return collateral_code


def get_collateral_view_code(fs_database):
    view_code_cursor = fs_database.cursor()
    view_code_query = "SELECT fs.codeGenerator('COLLATERAL-VIEW')"
    view_code_cursor.execute(view_code_query)
    view_code_details = view_code_cursor.fetchall()
    view_code_cursor.close()
    view_code = view_code_details[0][0]
    return view_code


def get_collateral_template_code(fund_code, reporting_date, fs_database):
    # reporting_date = datetime.datetime.strptime(reporting_date'], '%Y-%m-%d %H:%M:%S').date()
    template_code_cursor = fs_database.cursor()
    template_code_query = "SELECT template_code from fs.collateral_templates ct WHERE ct.entity_code = '" + \
                          fund_code + "' and ct.template_type_code = 'FINTUPLE' and (('" + str(reporting_date) \
                          + "' >= ct.effective_start_date and ct.effective_end_date IS NULL) or ('" + \
                          str(reporting_date) + "' BETWEEN ct.effective_start_date and ct.effective_end_date))"
    template_code_cursor.execute(template_code_query)
    template_code_details = template_code_cursor.fetchall()
    template_code = template_code_details[0][0]
    return template_code


def get_default_visibility_code(fund_code, fs_database):
    visibility_code_cursor = fs_database.cursor()
    visibility_code_query = "SELECT default_visibility_code from fs.collateral_templates where entity_code = '" + \
                            fund_code + "' and entity_type = 'FUND' and template_type_code = 'FINTUPLE'"
    visibility_code_cursor.execute(visibility_code_query)
    visibility_code = visibility_code_cursor.fetchall()
    visibility_code_cursor.close()
    return visibility_code[0][0]


def get_fund_codes(iq_database):
    fund_code_cursor = iq_database.cursor()
    fund_code_query = "SELECT fund_code, effective_end_date from iq.fund_performance where " \
                      "effective_end_date >= '2020-04-30'"
    fund_code_cursor.execute(fund_code_query)
    fund_code_details = fund_code_cursor.fetchall()
    fund_code_cursor.close()
    return fund_code_details


def get_pe_ratio(security_isin_list, iq_database):
    pe_ratio_cursor = iq_database.cursor()
    pe_ratio_list = []
    for security in security_isin_list:
        pe_ratio_query = "SELECT pe_ratio from iq.securities_fundamentals where security_isin = '" + \
                         security['security_isin'] + "' order by as_on_date desc limit 1"
        pe_ratio_cursor.execute(pe_ratio_query)
        pe_ratio_details = pe_ratio_cursor.fetchall()
        if any(pe_ratio_details) is False:
            pe_ratio_body = {"security_isin": security['security_isin'], "pe_ratio": 0}
        elif pe_ratio_details[0][0] is None:
            pe_ratio_body = {"security_isin": security['security_isin'], "pe_ratio": 0}
        else:
            pe_ratio_body = {"security_isin": security['security_isin'], "pe_ratio": pe_ratio_details[0][0]}
        pe_ratio_list.append(pe_ratio_body)
    pe_ratio_cursor.close()
    return pe_ratio_list


def get_fund_ratio_mcap(security_isin_list, iq_database):
    fund_ratio_mcap_cursor = iq_database.cursor()
    fund_ratio_mcap_list = []
    for security in security_isin_list:
        fund_ratio_mcap_query = "SELECT market_cap from iq.securities_fundamentals where security_isin = '" + \
                                security['security_isin'] + "' order by as_on_date desc limit 1"
        fund_ratio_mcap_cursor.execute(fund_ratio_mcap_query)
        fund_ratio_mcap_details = fund_ratio_mcap_cursor.fetchall()
        if any(fund_ratio_mcap_details) is False:
            fund_ratio_mcap_body = {"security_isin": security['security_isin'], "market_cap": 0}
        elif fund_ratio_mcap_details[0][0] is None:
            fund_ratio_mcap_body = {"security_isin": security['security_isin'], "market_cap": 0}
        else:
            fund_ratio_mcap_body = {"security_isin": security['security_isin'],
                                    "market_cap": fund_ratio_mcap_details[0][0]}
        fund_ratio_mcap_list.append(fund_ratio_mcap_body)
    fund_ratio_mcap_cursor.close()
    return fund_ratio_mcap_list


def get_all_fund_return(fund_code, iq_database):
    fund_return_cursor = iq_database.cursor()
    fund_return_query = "SELECT perf_1m from iq.fund_performance where fund_code = '" + fund_code + "'"
    fund_return_cursor.execute(fund_return_query)
    fund_return_details = fund_return_cursor.fetchall()
    fund_return_list = []
    for return_value in fund_return_details:
        if return_value[0] is None:
            value = 0
            fund_return_list.append(value)
        else:
            fund_return_list.append(return_value[0])
    return fund_return_list


def get_risk_free_rate(iq_database):
    risk_free_cursor = iq_database.cursor()
    risk_free_query = "SELECT risk_free_return_rate from iq.ratio_basis"
    risk_free_cursor.execute(risk_free_query)
    risk_free_details = risk_free_cursor.fetchall()
    risk_free_rate = risk_free_details[0][0]
    return risk_free_rate


def get_fund_dates(fund_code, iq_database):
    fund_dates_cursor = iq_database.cursor()
    fund_dates_query = "SELECT effective_end_date from iq.fund_performance where fund_code = '" + fund_code + \
                       "' order by effective_end_date"
    fund_dates_cursor.execute(fund_dates_query)
    fund_dates_details = fund_dates_cursor.fetchall()
    fund_dates_cursor.close()
    fund_dates_list = []
    for date in fund_dates_details:
        fund_dates_list.append(date[0])
    return fund_dates_list


def get_fund_portfolio(fund_code, reporting_date, iq_database):
    portfolio_cursor = iq_database.cursor()
    portfolio_query = "SELECT security_isin, exposure from iq.fund_portfolio_details where fund_code = '" + \
                      fund_code + "' and reporting_date = '" + str(reporting_date) + "'"
    portfolio_cursor.execute(portfolio_query)
    portfolio_details = portfolio_cursor.fetchall()
    portfolio_cursor.close()
    return portfolio_details


def get_benchmark_perf_1m(fund_code, reporting_date, iq_database):
    bm_perf_cursor = iq_database.cursor()
    bm_perf_query = "SELECT benchmark_perf_1m from iq.fund_performance where fund_code = '" + fund_code \
                    + "' and effective_end_date = '" + str(reporting_date) + "'"
    bm_perf_cursor.execute(bm_perf_query)
    bm_perf_details = bm_perf_cursor.fetchall()
    bm_perf_cursor.close()
    return bm_perf_details[0][0]


def update_islatest(fund_code, previous_1m_end_date, iq_database):
    update_cursor = iq_database.cursor()
    update_query = "UPDATE iq.fund_performance SET isLatest = NULL where effective_end_date = '" + \
                   str(previous_1m_end_date) + "' and fund_code = '" + fund_code + "'"
    update_cursor.execute(update_query)
    update_cursor.close()


def is_fund_performance_exist(fund_code, effective_end_date, iq_database):
    is_fund_performance_cursor = iq_database.cursor()
    is_fund_performance_query = "SELECT count(*) from iq.fund_performance where fund_code = '" + fund_code \
                                + "' and effective_end_date = '" + str(effective_end_date) + "'"
    is_fund_performance_cursor.execute(is_fund_performance_query)
    fund_performance_details = is_fund_performance_cursor.fetchall()
    return fund_performance_details[0][0]


def put_fund_performance(fund_perf_data, benchmark_perf_data, alt_benchmark_perf_data, iq_database):
    fund_cursor = iq_database.cursor()
    if is_fund_performance_exist(fund_perf_data['fund_code'], fund_perf_data['effective_end_date'], iq_database):
        fund_perf_query = "UPDATE iq.fund_performance SET investment_style_type_code = %s, perf_1m = %s, " \
                          "perf_3m = %s, perf_6m = %s, perf_1y = %s, perf_2y = %s, perf_3y = %s, perf_5y = %s, " \
                          "perf_inception = %s, benchmark_perf_1m = %s, benchmark_perf_3m = %s, " \
                          "benchmark_perf_6m = %s, benchmark_perf_1y = %s, benchmark_perf_2y = %s, " \
                          "benchmark_perf_3y = %s, benchmark_perf_5y = %s, benchmark_perf_inception = %s, " \
                          "alt_benchmark_perf_1m = %s, alt_benchmark_perf_3m = %s, alt_benchmark_perf_6m = %s, " \
                          "alt_benchmark_perf_1y = %s, alt_benchmark_perf_2y = %s, alt_benchmark_perf_3y = %s, " \
                          "alt_benchmark_perf_5y = %s, alt_benchmark_perf_inception = %s where " \
                          "fund_code = '" + fund_perf_data['fund_code'] + "' and effective_end_date = '" + \
                          str(fund_perf_data['effective_end_date']) + "'"
        insert_values = (fund_perf_data['investment_style_type_code'], fund_perf_data['perf_1m'],
                         fund_perf_data['perf_3m'], fund_perf_data['perf_6m'], fund_perf_data['perf_1y'],
                         fund_perf_data['perf_2y'], fund_perf_data['perf_3y'], fund_perf_data['perf_5y'],
                         fund_perf_data['perf_inception'], benchmark_perf_data['benchmark_perf_1m'],
                         benchmark_perf_data['benchmark_perf_3m'], benchmark_perf_data['benchmark_perf_6m'],
                         benchmark_perf_data['benchmark_perf_1y'], benchmark_perf_data['benchmark_perf_2y'],
                         benchmark_perf_data['benchmark_perf_3y'], benchmark_perf_data['benchmark_perf_5y'],
                         benchmark_perf_data['benchmark_perf_inception'],
                         alt_benchmark_perf_data['alt_benchmark_perf_1m'],
                         alt_benchmark_perf_data['alt_benchmark_perf_3m'],
                         alt_benchmark_perf_data['alt_benchmark_perf_6m'],
                         alt_benchmark_perf_data['alt_benchmark_perf_1y'],
                         alt_benchmark_perf_data['alt_benchmark_perf_2y'],
                         alt_benchmark_perf_data['alt_benchmark_perf_3y'],
                         alt_benchmark_perf_data['alt_benchmark_perf_5y'],
                         alt_benchmark_perf_data['alt_benchmark_perf_inception'])
    else:
        fund_perf_query = "INSERT INTO iq.fund_performance (fund_code, current_aum, no_of_clients, " \
                          "market_cap_type_code, investment_style_type_code, portfolio_equity_allocation, " \
                          "portfolio_cash_allocation, portfolio_asset_allocation, portfolio_other_allocations, " \
                          "perf_1m, perf_3m, perf_6m, perf_1y, perf_2y, perf_3y, perf_5y, perf_inception, " \
                          "benchmark_perf_1m, benchmark_perf_3m, benchmark_perf_6m, benchmark_perf_1y, " \
                          "benchmark_perf_2y, benchmark_perf_3y, benchmark_perf_5y, benchmark_perf_inception, " \
                          "alt_benchmark_perf_1m, alt_benchmark_perf_3m, alt_benchmark_perf_6m, " \
                          "alt_benchmark_perf_1y, alt_benchmark_perf_2y, alt_benchmark_perf_3y, " \
                          "alt_benchmark_perf_5y, alt_benchmark_perf_inception, isLatest, effective_start_date, " \
                          "effective_end_date, created_ts, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                          "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                          "%s, %s, %s, %s, %s, %s, %s)"
        insert_values = (fund_perf_data['fund_code'], fund_perf_data['current_aum'], fund_perf_data['no_of_clients'],
                         fund_perf_data['market_cap_type_code'], fund_perf_data['investment_style_type_code'],
                         fund_perf_data['portfolio_equity_allocation'], fund_perf_data['portfolio_cash_allocation'],
                         fund_perf_data['portfolio_asset_allocation'], fund_perf_data['portfolio_other_allocations'],
                         fund_perf_data['perf_1m'], fund_perf_data['perf_3m'], fund_perf_data['perf_6m'],
                         fund_perf_data['perf_1y'], fund_perf_data['perf_2y'], fund_perf_data['perf_3y'],
                         fund_perf_data['perf_5y'], fund_perf_data['perf_inception'],
                         benchmark_perf_data['benchmark_perf_1m'], benchmark_perf_data['benchmark_perf_3m'],
                         benchmark_perf_data['benchmark_perf_6m'], benchmark_perf_data['benchmark_perf_1y'],
                         benchmark_perf_data['benchmark_perf_2y'], benchmark_perf_data['benchmark_perf_3y'],
                         benchmark_perf_data['benchmark_perf_5y'], benchmark_perf_data['benchmark_perf_inception'],
                         alt_benchmark_perf_data['alt_benchmark_perf_1m'],
                         alt_benchmark_perf_data['alt_benchmark_perf_3m'],
                         alt_benchmark_perf_data['alt_benchmark_perf_6m'],
                         alt_benchmark_perf_data['alt_benchmark_perf_1y'],
                         alt_benchmark_perf_data['alt_benchmark_perf_2y'],
                         alt_benchmark_perf_data['alt_benchmark_perf_3y'],
                         alt_benchmark_perf_data['alt_benchmark_perf_5y'],
                         alt_benchmark_perf_data['alt_benchmark_perf_inception'], fund_perf_data['isLatest'],
                         fund_perf_data['effective_start_date'], fund_perf_data['effective_end_date'],
                         fund_perf_data['created_ts'], fund_perf_data['created_by'])
    fund_cursor.execute(fund_perf_query, insert_values)
    fund_cursor.close()


def is_nav_exist(fund_code, effective_end_date, iq_database):
    is_nav_cursor = iq_database.cursor()
    is_nav_query = "SELECT count(*) from iq.fund_benchmark_nav where fund_code = '" + fund_code \
                   + "' and effective_end_date = '" + str(effective_end_date) + "'"
    is_nav_cursor.execute(is_nav_query)
    nav_details = is_nav_cursor.fetchall()
    return nav_details[0][0]


def put_nav_data(nav_data, iq_database):
    nav_cursor = iq_database.cursor()
    if is_nav_exist(nav_data['fund_code'], nav_data['effective_end_date'], iq_database):
        nav_query = "UPDATE iq.fund_benchmark_nav SET benchmark_index_code = %s, " \
                    "alt_benchmark_index_code = %s, fund_nav = %s, benchmark_nav = %s, alt_benchmark_nav = %s, " \
                    "where fund_code = '" + nav_data['fund_code'] + "' and effective_end_date = '" + \
                    str(nav_data['effective_end_date']) + "'"
        nav_values = (nav_data['benchmark_index_code'], nav_data['alt_benchmark_index_code'], nav_data['fund_nav'],
                      nav_data['benchmark_nav'], nav_data['alt_benchmark_nav'])
    else:
        nav_query = "INSERT INTO iq.fund_benchmark_nav (fund_code, benchmark_index_code, alt_benchmark_index_code, " \
                    "fund_nav, benchmark_nav, alt_benchmark_nav, effective_end_date) VALUES (%s, %s, %s, %s, %s, %s, " \
                    "%s)"
        nav_values = (nav_data['fund_code'], nav_data['benchmark_index_code'], nav_data['alt_benchmark_index_code'],
                      nav_data['fund_nav'], nav_data['benchmark_nav'], nav_data['alt_benchmark_nav'],
                      nav_data['effective_end_date'])
    nav_cursor.execute(nav_query, nav_values)
    nav_cursor.close()


def is_market_cap_exist(fund_code, end_date, type_market_cap, iq_database):
    is_market_cap_cursor = iq_database.cursor()
    is_market_cap_query = "SELECT count(*) from iq.fund_market_cap_details where fund_code = '" + fund_code \
                          + "' and end_date = '" + str(end_date) + "' and type_market_cap = '" + type_market_cap + "'"
    is_market_cap_cursor.execute(is_market_cap_query)
    market_cap_details = is_market_cap_cursor.fetchall()
    return market_cap_details[0][0]


def put_market_cap_data(marketcap_data, iq_database):
    market_cap_cursor = iq_database.cursor()
    for data in marketcap_data:
        if is_market_cap_exist(data['fund_code'], data['end_date'], data['type_market_cap'], iq_database):
            market_cap_query = "UPDATE iq.fund_market_cap_details SET type_market_cap = %s, " \
                               "exposure = %s where fund_code = '" + data['fund_code'] + "' and end_date = '" + \
                               str(data['end_date']) + "' and type_market_cap = '" + data['type_market_cap'] + "'"
            market_cap_values = (data['type_market_cap'], data['exposure'])
        else:
            market_cap_query = "INSERT INTO iq.fund_market_cap_details (fund_code, type_market_cap, exposure, " \
                               "start_date, end_date, created_ts, action_by) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            market_cap_values = (data['fund_code'], data['type_market_cap'], data['exposure'], data['start_date'],
                                 data['end_date'], data['created_ts'], data['action_by'])
        market_cap_cursor.execute(market_cap_query, market_cap_values)
    market_cap_cursor.close()


def is_fund_portfolio_exist(fund_code, end_date, security_isin, iq_database):
    is_fund_portfolio_cursor = iq_database.cursor()
    is_fund_portfolio_query = "SELECT count(*) from iq.fund_portfolio_details where fund_code = '" + fund_code \
                              + "' and end_date = '" + str(end_date) + "' and security_isin = '" + security_isin + "'"
    is_fund_portfolio_cursor.execute(is_fund_portfolio_query)
    fund_portfolio_details = is_fund_portfolio_cursor.fetchall()
    return fund_portfolio_details[0][0]


def put_fund_portfolio(portfolio_data, iq_database):
    portfolio_cursor = iq_database.cursor()
    # for data in portfolio_data:
    if is_fund_portfolio_exist(portfolio_data['fund_code'], portfolio_data['end_date'], portfolio_data['security_isin'],
                               iq_database):
        portfolio_query = "UPDATE iq.fund_portfolio_details SET security_isin = %s, exposure = %s where " \
                          "fund_code = '" + portfolio_data['fund_code'] + "' and end_date = '" + \
                          str(portfolio_data['end_date']) + "' and security_isin = '" + \
                          portfolio_data['security_isin'] + "'"
        portfolio_values = (portfolio_data['security_isin'], portfolio_data['exposure'])
    else:
        portfolio_query = "INSERT INTO iq.fund_portfolio_details (fund_code, security_isin, exposure, " \
                          "start_date, end_date, created_ts, action_by) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        portfolio_values = (portfolio_data['fund_code'], portfolio_data['security_isin'], portfolio_data['exposure'],
                            portfolio_data['start_date'], portfolio_data['end_date'], portfolio_data['created_ts'],
                            portfolio_data['action_by'])
    portfolio_cursor.execute(portfolio_query, portfolio_values)
    portfolio_cursor.close()


def is_fund_sector_exist(fund_code, end_date, sector_type_name, iq_database):
    is_fund_sector_cursor = iq_database.cursor()
    is_fund_sector_query = "SELECT count(*) from iq.fund_sector_details where fund_code = '" + fund_code \
                           + "' and end_date = '" + str(end_date) + "' and sector_type_name = '" + sector_type_name \
                           + "'"
    is_fund_sector_cursor.execute(is_fund_sector_query)
    fund_sector_details = is_fund_sector_cursor.fetchall()
    return fund_sector_details[0][0]


def put_fund_sector(sector_data, iq_database):
    sector_cursor = iq_database.cursor()
    for data in sector_data:
        if is_fund_sector_exist(data['fund_code'], data['end_date'], data['sector_type_name'], iq_database):
            sector_query = "UPDATE iq.fund_sector_details SET sector_type_name = %s, exposure = %s where " \
                           "fund_code = '" + data['fund_code'] + "' and end_date = '" + str(data['end_date']) + \
                           "' and sector_type_name = '" + data['sector_type_name'] + "'"
            sector_values = (data['sector_type_name'], data['exposure'])
        else:
            sector_query = "INSERT INTO iq.fund_sector_details (fund_code, sector_type_name, exposure, start_date, " \
                           "end_date, created_ts, action_by) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            sector_values = (data['fund_code'], data['sector_type_name'], data['exposure'], data['start_date'],
                             data['end_date'], data['created_ts'], data['action_by'])
        sector_cursor.execute(sector_query, sector_values)
    sector_cursor.close()


def is_collaterals_exist(fund_code, reporting_date, fs_database):
    collateral_cursor = fs_database.cursor()
    collateral_query = "SELECT count(*) from fs.collaterals where entity_code = '" + fund_code + \
                       "' and reporting_date = '" + str(reporting_date) + "'"
    collateral_cursor.execute(collateral_query)
    collateral_details = collateral_cursor.fetchall()
    collateral_cursor.close()
    return collateral_details[0][0]


def put_collateral_data(collateral_data, fs_database):
    collateral_cursor = fs_database.cursor()
    collateral_query = "INSERT INTO fs.collaterals (collateral_code, view_code, collateral_type_code, entity_type, " \
                       "entity_code, collateral_title, visibility_code, template_code, collateral_date, " \
                       "collateral_status, reporting_date, effective_start_date, is_premium, is_published, " \
                       "is_data_changed, published_ts, created_ts, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    collateral_values = (collateral_data['collateral_code'], collateral_data['view_code'],
                         collateral_data['collateral_type_code'], collateral_data['entity_type'],
                         collateral_data['entity_code'], collateral_data['collateral_title'],
                         collateral_data['visibility_code'], collateral_data['template_code'],
                         collateral_data['collateral_date'], collateral_data['collateral_status'],
                         collateral_data['reporting_date'], collateral_data['effective_start_date'],
                         collateral_data['is_premium'], collateral_data['is_published'],
                         collateral_data['is_data_changed'], collateral_data['published_ts'],
                         collateral_data['created_ts'], collateral_data['created_by'])
    collateral_cursor.execute(collateral_query, collateral_values)
    collateral_cursor.close()


def is_fund_ratio_exist(fund_code, reporting_date, iq_database):
    is_fund_ratio_cursor = iq_database.cursor()
    is_fund_ratio_query = "SELECT count(*) from iq.fund_ratios where fund_code = '" + fund_code \
                          + "' and reporting_date = '" + str(reporting_date) + "'"
    is_fund_ratio_cursor.execute(is_fund_ratio_query)
    fund_ratio_details = is_fund_ratio_cursor.fetchall()
    return fund_ratio_details[0][0]


def put_fund_ratio_data(fund_ratio_data, iq_database):
    ratio_cursor = iq_database.cursor()
    ratio_query = "INSERT INTO iq.fund_ratios (fund_code, reporting_date, top5_pe_ratio, top10_pe_ratio, " \
                  "top5_market_cap, top10_market_cap, standard_deviation, median, sigma, sortino_ratio, " \
                  "negative_excess_returns_risk_free, fund_alpha, updated_ts, updated_by) VALUES (%s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    fund_ratio_values = (str(fund_ratio_data['fund_code']), fund_ratio_data['reporting_date'],
                         fund_ratio_data['top5_pe_ratio'], fund_ratio_data['top10_pe_ratio'],
                         fund_ratio_data['top5_market_cap'], fund_ratio_data['top10_market_cap'],
                         fund_ratio_data['standard_deviation'], fund_ratio_data['median'], fund_ratio_data['sigma'],
                         fund_ratio_data['sortino_ratio'], fund_ratio_data['negative_excess_returns_risk_free'],
                         fund_ratio_data['fund_alpha'], fund_ratio_data['updated_ts'],
                         fund_ratio_data['updated_by'])
    ratio_cursor.execute(ratio_query, fund_ratio_values)
    ratio_cursor.close()


def is_index_performance_exist(index_code, reporting_date, iq_database):
    is_index_cursor = iq_database.cursor()
    is_index_query = "SELECT count(*) from iq.index_performance where index_code = '" + index_code \
                     + "' and reporting_date = '" + str(reporting_date) + "'"
    is_index_cursor.execute(is_index_query)
    index_details = is_index_cursor.fetchall()
    return index_details[0][0]


def put_index_performance(index_perf_data, iq_database):
    index_perf_cursor = iq_database.cursor()
    if is_index_performance_exist(index_perf_data['index_code'], index_perf_data['reporting_date'], iq_database):
        index_perf_query = "UPDATE iq.index_performance SET perf_1m = %s, perf_3m = %s, " \
                           "perf_6m = %s, perf_1y = %s, perf_2y = %s, perf_3y = %s, perf_5y = %s, " \
                           "perf_inception = %s where reporting_date = '" + str(index_perf_data['reporting_date']) \
                           + "' and index_code = '" + index_perf_data['index_code'] + "'"
        index_perf_values = (index_perf_data['perf_1m'], index_perf_data['perf_3m'], index_perf_data['perf_6m'],
                             index_perf_data['perf_1y'], index_perf_data['perf_2y'], index_perf_data['perf_3y'],
                             index_perf_data['perf_5y'], index_perf_data['perf_inception'])
    else:
        index_perf_query = "INSERT INTO iq.index_performance (index_code, perf_1m, perf_3m, perf_6m, perf_1y, " \
                           "perf_2y, perf_3y, perf_5y, perf_inception, reporting_date) VALUES (%s, %s, %s, %s, " \
                           "%s, %s, %s, %s, %s, %s)"
        index_perf_values = (index_perf_data['index_code'], index_perf_data['perf_1m'], index_perf_data['perf_3m'],
                             index_perf_data['perf_6m'], index_perf_data['perf_1y'], index_perf_data['perf_2y'],
                             index_perf_data['perf_3y'], index_perf_data['perf_5y'], index_perf_data['perf_inception'],
                             index_perf_data['reporting_date'])
    index_perf_cursor.execute(index_perf_query, index_perf_values)
    index_perf_cursor.close()


def put_fund_bm_nav(fund_code, benchmark_nav, date, iq_database):
    insert_cursor = iq_database.cursor()
    insert_query = "UPDATE iq.fund_benchmark_nav SET benchmark_nav = '" + str(benchmark_nav) + \
                   "' where fund_code = '" + fund_code + "' and effective_end_date = '" + str(date) + "'"
    insert_cursor.execute(insert_query)
    insert_cursor.close()


def put_fund_alt_bm_nav(fund_code, alt_benchmark_nav, date, iq_database):
    insert_cursor = iq_database.cursor()
    insert_query = "UPDATE iq.fund_benchmark_nav SET alt_benchmark_nav = '" + str(alt_benchmark_nav) + \
                   "' where fund_code = '" + fund_code + "' and effective_end_date = '" + str(date) + "'"
    insert_cursor.execute(insert_query)
    insert_cursor.close()


def put_fund_nav(fund_code, fund_nav, date, iq_database):
    insert_cursor = iq_database.cursor()
    insert_query = "UPDATE iq.fund_benchmark_nav SET fund_nav = '" + str(fund_nav) + \
                   "' where fund_code = '" + fund_code + "' and effective_end_date = '" + str(date) + "'"
    insert_cursor.execute(insert_query)
    insert_cursor.close()


def put_collateral_title(entity_code, collateral_title, reporting_date, fs_database):
    title_cursor = fs_database.cursor()
    title_query = "UPDATE fs.collaterals SET collateral_title = '" + collateral_title + "' where reporting_date = '" + \
                  str(reporting_date) + "' and entity_type = 'FUND' and created_by = 'ft-automation' and entity_code " \
                                        "= '" + entity_code + "'"
    title_cursor.execute(title_query)
    title_cursor.close()
