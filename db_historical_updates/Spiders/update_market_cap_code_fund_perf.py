import MySQLdb  # pip install mysqlclient
from envparse import env


def get_fund_code():
    fund_cursor = database.cursor()
    fund_query = "SELECT fund_code FROM fund_identity"
    fund_cursor.execute(fund_query)
    fund_list = fund_cursor.fetchall()
    fund_cursor.close()
    fund_code_list = []
    for fund in fund_list:
        fund_code_list.append(fund[0])
    print(fund_code_list)
    return fund_code_list


def get_date_list(fund_code):
    date_cursor = database.cursor()
    date_query = "SELECT DISTINCT(end_date) FROM fund_market_cap_details where fund_code = '" + fund_code \
                 + "' order by end_date asc"
    date_cursor.execute(date_query)
    date_list = date_cursor.fetchall()
    return date_list


def get_monthly_market_cap(fund_code, end_date):
    month_cap_cursor = database.cursor()
    month_cap_query = "SELECT type_market_cap, exposure from fund_market_cap_details where " \
                      "fund_code = '" + str(fund_code) + "' and end_date = '" + str(end_date) + "'"
    month_cap_cursor.execute(month_cap_query)
    monthly_details = month_cap_cursor.fetchall()
    cap_data = list(monthly_details)
    month_cap_cursor.close()
    return cap_data


def get_cap_type(type_desc, iq_database):
    cap_type_cursor = iq_database.cursor()
    cap_type_query = "SELECT market_cap_type_code from iq.mas_market_cap_types where market_cap_type_desc = '" + \
                     type_desc + "'"
    cap_type_cursor.execute(cap_type_query)
    cap_type_details = cap_type_cursor.fetchall()
    cap_type_code = cap_type_details[0][0]
    cap_type_cursor.close()
    return cap_type_code


def get_market_cap_type_code(market_cap_values, database):
    market_cap_type_code = None
    market_cap_values = dict(market_cap_values)
    mcap_check = not market_cap_values
    if mcap_check is True:
        market_cap_type_code = None
    elif mcap_check is False:
        if len(market_cap_values) == 1:
            if market_cap_values.__contains__('Cash'):
                del market_cap_values['Cash']
                market_cap_type_code = None
        else:
            for key in market_cap_values:
                market_cap_values[key] *= 100
            mega_value = market_cap_values['Mega'] if 'Mega' in market_cap_values.keys() else 0
            large_value = market_cap_values['Large'] if 'Large' in market_cap_values.keys() else 0
            small_value = market_cap_values['Small'] if 'Small' in market_cap_values.keys() else 0
            micro_value = market_cap_values['Micro'] if 'Micro' in market_cap_values.keys() else 0
            market_cap_values.update({"Large": mega_value + large_value})
            market_cap_values.update({"Small": small_value + micro_value})
            keys_to_remove = ["Cash", "Micro", "Mega", "ETF"]
            for key in keys_to_remove:
                if key in market_cap_values.keys():
                    del market_cap_values[key]
            large_exposure = market_cap_values['Large'] if 'Large' in market_cap_values.keys() else 0
            small_exposure = market_cap_values['Small'] if 'Small' in market_cap_values.keys() else 0
            mid_exposure = market_cap_values['Mid'] if 'Mid' in market_cap_values.keys() else 0
            if large_exposure >= 20 and mid_exposure >= 20 and small_exposure >= 20:
                market_cap_type_code = get_cap_type("Multi Cap", database)
            elif ((65 > large_exposure >= 25 and 65 > mid_exposure >= 25) or
                  (65 > mid_exposure >= 25 and 65 > small_exposure >= 25) or
                  (65 > small_exposure >= 25 and 65 > large_exposure >= 25)):
                if large_exposure < mid_exposure and large_exposure < small_exposure:
                    market_cap_type_code = get_cap_type("Mid-Small Cap", database)
                elif mid_exposure < large_exposure and mid_exposure < small_exposure:
                    market_cap_type_code = get_cap_type("Large-Small Cap", database)
                elif small_exposure < large_exposure and small_exposure < mid_exposure:
                    market_cap_type_code = get_cap_type("Large-Mid Cap", database)
            else:
                if large_exposure > mid_exposure and large_exposure > small_exposure:
                    market_cap_type_code = get_cap_type("Large Cap", database)
                elif mid_exposure > large_exposure and mid_exposure > small_exposure:
                    market_cap_type_code = get_cap_type("Mid Cap", database)
                else:
                    market_cap_type_code = get_cap_type("Small Cap", database)
    print(market_cap_type_code)
    market_cap = {}
    market_cap.update({"fund_code": fund_code})
    market_cap.update({"date": str(date[0])})
    market_cap.update({"market_cap_type_code": market_cap_type_code})
    return market_cap


def put_into_db(market_cap):
    db_cursor = database.cursor()
    db_query = "UPDATE fund_performance SET market_cap_type_code = %s where fund_code = %s and effective_end_date = %s"
    values = (market_cap['market_cap_type_code'], market_cap['fund_code'], market_cap['date'])
    db_cursor.execute(db_query, values)
    print(market_cap)
    db_cursor.close()


try:
    # db_host, db_user, db_pass, db_name = env('DB_HOST'), env('DB_USER'), env('DB_PASS'), env('DB_NAME')
    db_host, db_user, db_pass, db_name = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                         'd0m#l1dZwhz!*9Iq0y1h', 'iq'
    database = MySQLdb.connect(db_host, db_user, db_pass, db_name, use_unicode=True, charset="utf8")
    fund_code_list = get_fund_code()
    for fund_code in fund_code_list:
        start_date = get_date_list(fund_code)
        for date in start_date:
            monthly_cap = get_monthly_market_cap(fund_code, str(date[0]))
            market_cap = get_market_cap_type_code(monthly_cap, database)
            put_into_db(market_cap)
    database.commit()
    database.close()

except Exception as error:
    print("Exception raised :", error)
