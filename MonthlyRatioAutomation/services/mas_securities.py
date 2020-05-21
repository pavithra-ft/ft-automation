import re

import MySQLdb
from pyjarowinkler import distance

from dictionary.portfolio_dictionary import portfolio_dict
from extraction.security_ratio_bse_500 import get_security_ratio
from services.db_actions import get_security_isin, get_all_isin, put_mas_securities


def get_isin(security_name, iq_database):
    if portfolio_dict.__contains__(security_name):
        sec_name = portfolio_dict[security_name]
    else:
        sec_name = security_name
    isin_details = get_security_isin(sec_name.replace("'", " "), iq_database)
    if len(isin_details) == 0:
        sec_name = sec_name.replace(".", " ").replace("'", " ")
        cleaned_sec_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', sec_name).lower()
        security_details = get_all_isin(iq_database)
        max_ratio = 0
        max_index = 0
        for value in range(len(security_details)):
            name = security_details[value][1].replace(".", " ").replace("'", " ")
            cleaned_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', name).lower()
            ratio = distance.get_jaro_distance(cleaned_sec_name, cleaned_name, winkler=True, scaling=0.1)
            if ratio > 0 and max_ratio < ratio:
                max_ratio = ratio
                max_index = value
        security_isin = security_details[max_index][0]
    else:
        security_isin = isin_details[0][0]
    print(security_isin)
    return security_isin


def get_mas_security_ratio(security_ratio_list, iq_database):
    mas_security_ratio_list = []
    for security in security_ratio_list:
        security_isin = get_isin(security['securtiy_name'], iq_database)
        # Get pe_ratio
        if security['price_to_earnings'] == '--' or security['price_to_earnings'] is None:
            pe_ratio = None
        else:
            pe_ratio = security['price_to_earnings']
        # Get pb_ratio
        if security['price_to_book'] == '--' or security['price_to_book'] is None:
            pb_ratio = None
        else:
            pb_ratio = security['price_to_book']
        # Get Dividend yield
        if security['dividend_yield'] == '--' or security['dividend_yield'] is None:
            dividend_yield = None
        else:
            if float(security['dividend_yield']):
                dividend_yield = round((float(security['dividend_yield']) / 100), 4)
            else:
                dividend_yield = None

        # Get Earning Per Share
        if security['earning_per_share'] == '--' or security['earning_per_share'] is None:
            eps = None
        else:
            eps = security['earning_per_share']

        security_ratio_body = {'security_isin': security_isin,
                               'market_cap_value': int(float(security['market_cap'].replace(',', '')) * 10000000),
                               'pe_ratio': pe_ratio, 'pb_ratio': pb_ratio, 'eps': eps, 'dividend_yield': dividend_yield}
        mas_security_ratio_list.append(security_ratio_body)
    return mas_security_ratio_list


try:
    iq_db, fs_db, app_db = 'iq', 'fs', 'app'
    # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', 'd0m#l1dZwhz!*9Iq0y1h'
    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db, use_unicode=True, charset="utf8")
    fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db, use_unicode=True, charset="utf8")
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db, use_unicode=True, charset="utf8")

    security_ratio_list = get_security_ratio()
    mas_security_ratio_list = get_mas_security_ratio(security_ratio_list, iq_database)
    put_mas_securities(mas_security_ratio_list, iq_database)
    # Database commit
    iq_database.commit()
    print('Commit success')
    iq_database.close()
    fs_database.close()
    app_database.close()

except Exception as error:
    print("Exception raised :", error)
