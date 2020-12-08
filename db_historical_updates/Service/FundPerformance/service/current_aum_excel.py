import os
import re
import datetime
import numpy as np
import pandas as pd
from glob import glob
from database.db_queries import put_current_aum, iq_session
from config.basic_config import aum_sheet_name, file_loc


def calc_current_aum(fund_code, aum_values):
    for row in aum_values:
        reporting_date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d").date()
        if row['AUM']:
            current_aum = round(float(float(row['AUM']) * 10000000), 4)
            try:
                put_current_aum(fund_code, current_aum, reporting_date)
            except Exception as error:
                iq_session.rollback()
                print("Exception raised :", error)
            finally:
                iq_session.close()


def get_current_aum(fund_code_list):
    os.chdir(file_loc[0])
    files = [file for file in glob("*.xlsx")]
    sheet_name = [aum_sheet_name[0]]
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x))
            df_dict = df.to_dict(orient='records')

            for fund_code in fund_code_list:
                calc_current_aum(fund_code, df_dict)
