import MySQLdb
from datetime import datetime
from Spiders.db_actions import get_sector_from_portfolio, put_fund_sector


def get_portfolio_dates(fund_code, iq_database):
    portfolio_date_cursor = iq_database.cursor()
    portfolio_date_query = "SELECT distinct end_date from iq.fund_portfolio_details where fund_code = '" \
                           + fund_code + "'"
    portfolio_date_cursor.execute(portfolio_date_query)
    portfolio_date_details = portfolio_date_cursor.fetchall()
    portfolio_date_list = [date[0] for date in portfolio_date_details]
    return portfolio_date_list


def get_portfolio_details(fund_code, reporting_date, iq_database):
    portfolio_cursor = iq_database.cursor()
    portfolio_query = "SELECT security_isin, exposure from iq.fund_portfolio_details where fund_code = '" + fund_code \
                      + "' and end_date = '" + str(reporting_date) + "'"
    portfolio_cursor.execute(portfolio_query)
    portfolio_details = portfolio_cursor.fetchall()
    portfolio_values = []
    for value in portfolio_details:
        value_body = {'security_isin': value[0], 'exposure': value[1]}
        portfolio_values.append(value_body)
    return portfolio_values


def get_fund_sector_from_portfolio(portfolio_values, iq_database):
    global sec_isin, sector_response
    sector_breakdown = []
    for securityData in portfolio_values:
        sector_body = {"isin": securityData["security_isin"], "sector": None, "exposure": securityData["exposure"]}
        if securityData["security_isin"]:
            sec_isin = securityData["security_isin"]
            sector_response = get_sector_from_portfolio(sec_isin, iq_database)
        sector_body["sector"] = sector_response[0][0]
        sector_breakdown.append(sector_body)
    sector_breakdown_result = {}
    sector_sum = 0
    for i in sector_breakdown:
        sector_sum += i['exposure']
        if sector_breakdown_result.__contains__(i["sector"]):
            sector_breakdown_result[i["sector"]] += i["exposure"]
        else:
            sector_breakdown_result.update({i["sector"]: i["exposure"]})
    for sec, exp in sector_breakdown_result.items():
        if exp == 0:
            sector_breakdown_result[sec] = None
        else:
            sector_breakdown_result[sec] = round(exp, 4)
    return sector_breakdown_result


try:
    # Database connection
    iq_db, fs_db, app_db = 'iq', 'fs', 'app'
    # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                'd0m#l1dZwhz!*9Iq0y1h'
    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db, use_unicode=True, charset="utf8")
    fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db, use_unicode=True, charset="utf8")
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db, use_unicode=True, charset="utf8")

    fund_code_list = ['80132873', '20132936', '48274904']
    for fund_code in fund_code_list:
        portfolio_date_list = get_portfolio_dates(fund_code, iq_database)
        for reporting_date in portfolio_date_list:
            portfolio_values = get_portfolio_details(fund_code, reporting_date, iq_database)
            sector_values = get_fund_sector_from_portfolio(portfolio_values, iq_database)
            sector_data_list = []
            for sector_name, exposure in sector_values.items():
                sectorBody = {"fund_code": fund_code, "sector_type_name": sector_name,
                              "exposure": exposure, "start_date": reporting_date.replace(day=1),
                              "end_date": reporting_date, "created_ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              "action_by": "ft-automation"}
                sector_data_list.append(sectorBody)
            put_fund_sector(sector_data_list, iq_database)

    iq_database.commit()
    fs_database.commit()
    # Closing the database connection
    iq_database.close()
    fs_database.close()
    app_database.close()

except Exception as error:
    print("Exception raised :", error)
