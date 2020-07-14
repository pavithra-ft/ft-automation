import os
import re
import numpy as np
import pandas as pd
from glob import glob
from database.db_queries import get_all_isin, put_mas_securities_mcap

try:
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\db_historical_updates\Excel")
    files = [file for file in glob("*.xlsx")]
    sheet_name = ['Master File']
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
            isin_details = get_all_isin()
            for i in range(len(df)):
                security_isin, market_cap_type_code, market_cap_value = df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 3]
                for isin in isin_details:
                    if isin[0] == security_isin:
                        put_mas_securities_mcap(isin[0], market_cap_type_code, market_cap_value)

except Exception as error:
    print("Exception raised :", error)
