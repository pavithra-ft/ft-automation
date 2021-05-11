import os
import re
import datetime
import numpy as np
import pandas as pd
from glob import glob
from config.basic_config import client_sheet_name, file_loc
from database.db_queries import put_no_of_clients, iq_session


def calc_no_of_clients(fund_code, no_of_clients_values):
    for row in no_of_clients_values:
        reporting_date = datetime.datetime.strptime(row['Month End'], "%Y-%m-%d").date()
        try:
            put_no_of_clients(fund_code, row['No of clients'], reporting_date)
            iq_session.commit()
        except Exception as error:
            iq_session.rollback()
            print("Exception raised :", error)
        finally:
            iq_session.close()


def get_no_of_clients(fund_code_list):
    os.chdir(file_loc[0])
    files = [file for file in glob("*.xlsx")]
    sheet_names = [client_sheet_name[0]]
    for file in files:
        for sheet in sheet_names:
            df_read = pd.read_excel(file, sheet_name=sheet)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x))
            df_dict = df.to_dict(orient='records')

            for fund_code in fund_code_list:
                calc_no_of_clients(fund_code, df_dict)
