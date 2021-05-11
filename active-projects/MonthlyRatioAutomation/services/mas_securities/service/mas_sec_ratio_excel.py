import os
import re
import numpy as np
import pandas as pd
from glob import glob
from database.db_queries import get_all_isin, put_mas_securities_mcap


def get_mas_securities_ratio_excel():
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\db_historical_updates\Excel")
    files = [file for file in glob("*.xlsx")]
    sheet_name = ['Worksheet']
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet, skiprows=5)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
            isin_details = get_all_isin()
            for i in range(len(df)):
                security_isin = df.iloc[i, 3]
                market_cap_value = round(float(float(df.iloc[i, 8]) * 10000000))
                pe_ratio, pb_ratio, dividend_yield, eps = df.iloc[i, 9], df.iloc[i, 10], df.iloc[i, 11], df.iloc[i, 12]
                for isin in isin_details:
                    if isin[0] == security_isin:
                        try:
                            put_mas_securities_mcap(isin[0], market_cap_value, pe_ratio, pb_ratio, dividend_yield, eps)
                        except Exception as error:
                            print("Exception raised :", error)
