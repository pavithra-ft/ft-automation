from collections import defaultdict

import pandas as pd
import os
import glob
import MySQLdb
from envparse import env
import datetime
import numpy as np
import re

from pyjarowinkler import distance
from sortedcontainers import SortedSet

from Spiders.date_calculation import get_effective_start_end_date
from Spiders.db_actions import get_isin_sector, get_all_isin, put_fund_portfolio
from dictionary.portfolio_dictionary import portfolio_dict


def get_isin(portfolio_value, iq_database):
    global security_isin, sec_name
    if portfolio_dict.__contains__(portfolio_value['Security']):
        sec_name = portfolio_dict[portfolio_value['Security']]
    else:
        sec_name = portfolio_value['Security']
    isin_details = get_isin_sector(sec_name.replace("'", " "), iq_database)
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
    security_data = {'security_isin': security_isin, 'exposure': portfolio_value['Exposure']}
    return security_data


def get_fund_portfolio(fund_code, portfolio_values, date):
    for isin, exp in portfolio_values.items():
        created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_by = "ft-automation"
        reporting_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)
        portfolio_body = {}
        portfolio_body.update({"fund_code": fund_code})
        portfolio_body.update({"security_isin": isin})
        exp = round(float(exp), 4)
        if exp == 0:
            exposure = None
        else:
            exposure = exp
        portfolio_body.update({"exposure": exposure})
        portfolio_body.update({"start_date": effective_start_date})
        portfolio_body.update({"end_date": effective_end_date})
        portfolio_body.update({"created_ts": created_ts})
        portfolio_body.update({"action_by": created_by})
        print(portfolio_body)
        put_fund_portfolio(portfolio_body, iq_database)
        iq_database.commit()


def get_portfolio_values(df):
    df_dict = df.to_dict(orient='records')
    fund_code = df['Fund Code '].iloc[0]
    date_list = SortedSet([i['Date'] for i in df_dict])
    for date in date_list:
        print(date)
        isin_values = []
        for fund in df_dict:
            if fund['Date'] == date:
                security_data = get_isin(fund, iq_database)
                isin_values.append(security_data)
        portfolio_values = defaultdict(float)
        for d in isin_values:
            portfolio_values[d['security_isin']] += float(d['exposure'])
        print(portfolio_values)
        get_fund_portfolio(fund_code, portfolio_values, date)


try:
    sheet_names = ["Portfolio - 80132873", "Portfolio - 20132936", "Portfolio - 48274904",
                   "Portfolio - 65637732", "Portfolio - 56352531", "Portfolio - 39737982"]
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\db_historical_updates\Excel")
    files = []
    for file in glob.glob("*.xlsx"):
        files.append(file)
    for file in files:
        for sheet in sheet_names:
            df_read = pd.read_excel(file, sheet_name=sheet)
            file_name = os.path.splitext(file)[0]
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x))
            # Database connection
            iq_db, fs_db, app_db = 'iq', 'fs', 'app'
            # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
            db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                        'd0m#l1dZwhz!*9Iq0y1h'
            iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db, use_unicode=True, charset="utf8")
            fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db, use_unicode=True, charset="utf8")
            app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db, use_unicode=True, charset="utf8")

            get_portfolio_values(df)

            iq_database.commit()
            fs_database.commit()
            # Closing the database connection
            iq_database.close()
            fs_database.close()
            app_database.close()

except Exception as error:
    print("Exception raised :", error)
