import os
import re
import glob
import datetime
import numpy as np
import pandas as pd
from database.db_queries import put_current_aum


def get_current_aum(fund_code, aum_values):
    for row in aum_values:
        reporting_date = datetime.datetime.strptime(row['Month End'], "%Y-%m-%d").date()
        if row['AUM']:
            current_aum = round(float(float(row['AUM']) * 10000000), 4)
            put_current_aum(fund_code, current_aum, reporting_date)


try:
    sheet_names = ['AUM']
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\db_historical_updates\Excel")
    files = []
    for file in glob.glob("*.xlsx"):
        files.append(file)
    for file in files:
        for sheet in sheet_names:
            df_read = pd.read_excel(file, sheet_name=sheet)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x))
            fund_code_list = []
            for fund_code in fund_code_list:
                df_dict = df.to_dict(orient='records')
                get_current_aum(fund_code, df_dict)

except Exception as error:
    print("Exception raised :", error)
