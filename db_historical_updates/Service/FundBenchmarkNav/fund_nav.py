import re
import os
import numpy as np
import pandas as pd
from glob import glob
from database.db_queries import get_nav_dates, put_fund_nav


def get_fund_nav(fund_code, reporting_date, df_dict):
    for row in df_dict:
        if str(reporting_date) == row['date']:
            fund_nav = round(float(row['fund_nav']), 4)
            put_fund_nav(fund_code, fund_nav, reporting_date)
            print(fund_nav, reporting_date)


try:
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\db_historical_updates\Excel")
    files = [file for file in glob("*.xlsx")]
    sheet_name = []
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
            df_dict = df.to_dict(orient='records')

            fund_code_list = []
            for fund_code in fund_code_list:
                nav_dates_list = get_nav_dates(fund_code)
                nav_dates_list.pop(0)
                for date in nav_dates_list:
                    get_fund_nav(fund_code, date, df_dict)

except Exception as error:
    print("Exception raised :", error)
