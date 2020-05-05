from glob import glob
import os
import re
import MySQLdb
import numpy as np
import pandas as pd
from envparse import env

from Spiders.template_excel_extraction import get_fund_info, get_fund_allocation_values, get_market_cap_values, \
    get_fund_portfolio_values, get_fund_sector_values

try:
    os.chdir(r"C:\Users\pavithra\PycharmProjects\data_automation\excel files")
    files = [file for file in glob("*.xlsx")]
    sheet_name = ['Fund Performance Update']
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x))
            fund_info = get_fund_info(df)
            allocation_data = get_fund_allocation_values(df)
            market_cap_data = get_market_cap_values(df)
            portfolio_values = get_fund_portfolio_values(df)
            sector_values = get_fund_sector_values(df)

except Exception as error:
    print("Exception raised :", error)
