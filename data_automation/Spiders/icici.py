from glob import glob
import os
import re
import MySQLdb
import numpy as np
import pandas as pd
from envparse import env

from Spiders.db_actions import get_inst_details, get_funds_list, put_fund_performance, put_nav_data, \
    put_market_cap_data, put_fund_portfolio, put_fund_sector
from Spiders.calculation import put_into_iq_db
from Spiders.icici_excel_extraction import get_fund_info, get_market_cap_values, get_fund_portfolio_values, \
    get_fund_code

try:
    os.chdir(r"C:\Users\pavithra\PycharmProjects\data_automation\excel files")
    sheet_names = ["Flexi-cap", "Value", "Largecap", "Contra"]
    files = [file for file in glob("*.xlsx")]
    for file in files:
        for sheet in sheet_names:
            df_read = pd.read_excel(file, sheet_name=sheet)
            file_name = os.path.splitext(file)[0]
            if " (1)" in file_name:
                file_name = file_name.replace(" (1)", "")
            file_date = file_name.split('-')[1].strip()
            df_str = df_read.astype(str)
            dataframe = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x))
            db_host, db_user, db_pass, db_name = env('DB_HOST'), env('DB_USER'), env('DB_PASS'), env('DB_NAME')
            database = MySQLdb.connect(db_host, db_user, db_pass, db_name, use_unicode=True, charset="utf8")
            fund_info = get_fund_info(dataframe)
            market_cap_data = get_market_cap_values(dataframe)
            portfolio_values = get_fund_portfolio_values(dataframe)
            inst_code = get_inst_details("ICICI", database)
            fund_list = get_funds_list(inst_code, database)
            fund_code = get_fund_code(fund_info, fund_list)
            fund_data, nav_data, marketcap_data, portfolio_data, sector_dataList = \
                put_into_iq_db(fund_code, fund_info, portfolio_values, market_cap_data, database, file_date)
            put_fund_performance(fund_data, database)
            put_nav_data(nav_data, database)
            put_market_cap_data(marketcap_data, database)
            put_fund_portfolio(portfolio_data, database)
            put_fund_sector(sector_dataList, database)
            print(file_date, ": Fund code - ", fund_data['fund_code'], "Record inserted successfully")
            database.commit()
            database.close()

except Exception as error:
    print("Exception raised :", error)
