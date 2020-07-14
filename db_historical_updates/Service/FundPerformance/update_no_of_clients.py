import os
import re
import glob
import datetime
import numpy as np
import pandas as pd
from database.db_queries import put_no_of_clients


def get_no_of_clients(fund_code, no_of_clients_values):
    for row in no_of_clients_values:
        reporting_date = datetime.datetime.strptime(row['Month End'], "%Y-%m-%d").date()
        put_no_of_clients(fund_code, row['No of clients'], reporting_date)


try:
    sheet_names = ['No of clients']
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
                get_no_of_clients(fund_code, df_dict)

except Exception as error:
    print("Exception raised :", error)
