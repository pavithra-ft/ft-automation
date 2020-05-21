import re
import os
import MySQLdb
import numpy as np
import pandas as pd

from glob import glob
from envparse import env

from Spiders.db_actions import get_nav_dates, put_fund_nav


def get_fund_nav(fund_code, reporting_date, df_dict, iq_database):
    for row in df_dict:
        if str(reporting_date) == row['date']:
            fund_nav = round(float(row['fund_nav.1']), 4)
            put_fund_nav(fund_code, fund_nav, reporting_date, iq_database)
            print(fund_nav, reporting_date)


try:
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\db_historical_updates\Excel")
    files = [file for file in glob("*.xlsx")]
    sheet_name = ['72966297']

    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet)
            # Excel clean-up
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
            df_dict = df.to_dict(orient='records')

            # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
            db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                        'd0m#l1dZwhz!*9Iq0y1h'
            iq_db = 'iq'
            fs_db = 'fs'
            app_db = 'app'

            iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db)
            fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db)
            app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db)
            fund_code_list = [sheet]
            for fund_code in fund_code_list:
                nav_dates_list = get_nav_dates(fund_code, iq_database)
                nav_dates_list.pop(0)
                for date in nav_dates_list:
                    get_fund_nav(fund_code, date, df_dict, iq_database)

            iq_database.commit()
            print("Commit success")
            iq_database.close()
            fs_database.close()
            app_database.close()

except Exception as error:
    print("Exception raised :", error)
