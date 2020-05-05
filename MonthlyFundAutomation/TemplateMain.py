import os
import re
import MySQLdb
import numpy as np
import pandas as pd

from envparse import env
from glob import glob
from service.TemplateExtraction import get_fund_info, get_fund_allocation_values, get_market_cap_values, \
    get_fund_portfolio_values, get_fund_sector_values

try:
    os.chdir(r"C:\Users\pavithra\PycharmProjects\MonthlyFundAutomation\excel_files")
    files = [file for file in glob("*.xlsx")]
    sheet_name = ['Fund Performance Update']
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)

            # iq_db, fs_db, app_db = 'iq', 'fs', 'app'
            # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
            # db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
            #                             'd0m#l1dZwhz!*9Iq0y1h'
            # iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db, use_unicode=True, charset="utf8")
            # fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db, use_unicode=True, charset="utf8")
            # app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db, use_unicode=True, charset="utf8")

            fund_info = get_fund_info(df)
            allocation_values = get_fund_allocation_values(df)
            market_cap_values = get_market_cap_values(df)
            portfolio_values = get_fund_portfolio_values(df)
            sector_values = get_fund_sector_values(df)

            # iq_database.commit()
            # fs_database.commit()
            print("Record inserted successfully")
            # iq_database.close()
            # fs_database.close()
            # app_database.close()

except Exception as error:
    print("Exception raised :", error)
