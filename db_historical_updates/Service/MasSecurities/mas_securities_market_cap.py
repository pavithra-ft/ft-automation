import os
import re
import numpy as np
import pandas as pd
from glob import glob
from database.db_queries import get_all_isin, put_mas_securities_mcap

try:
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\db_historical_updates\Excel")
    files = [file for file in glob("*.xlsx")]
    sheet_name = ['Average MCap Jan Jun 2020']
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet, skiprows=1)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
            isin_details = get_all_isin()
            for i in range(len(df)):
                security_name = df.iloc[i, 1]
                security_isin = df.iloc[i, 2]
                market_cap_value = round(float(float(df.iloc[i, 9]) * 10000000))
                market_cap_type_code = df.iloc[i, 10].replace('Cap', '').upper()
                for isin in isin_details:
                    if isin[0] == security_isin:
                        put_mas_securities_mcap(isin[0], market_cap_type_code, market_cap_value)

except Exception as error:
    print("Exception raised :", error)
