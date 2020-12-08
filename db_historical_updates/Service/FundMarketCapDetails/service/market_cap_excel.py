import re
import os
import numpy as np
import pandas as pd
from glob import glob
from datetime import datetime
from database.db_queries import put_market_cap_data, iq_session
from model.FundTablesModel import FundMarketCapDetails
from config.basic_config import file_loc, mcap_sheet_name


def calc_market_cap(fund_code, df_dict):
    market_cap_list = []
    for row in df_dict:
        if row['Date']:
            mcap_body = FundMarketCapDetails()
            mcap_body.set_fund_code(fund_code)
            mcap_body.set_type_market_cap(row['Market Cap'].strip().capitalize())
            mcap_body.set_exposure(round(float(row['%']), 4))
            mcap_body.set_start_date(datetime.strptime(row['Date'], '%Y-%m-%d').replace(day=1))
            mcap_body.set_end_date(row['Date'])
            mcap_body.set_created_ts(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            mcap_body.set_action_by('ft-automation')
            market_cap_list.append(mcap_body)
    try:
        put_market_cap_data(market_cap_list)
        iq_session.commit()
    except Exception as error:
        iq_session.rollback()
        print('Exception raised:', error)
    finally:
        iq_session.close()


def get_market_cap(fund_code_list):
    os.chdir(file_loc[0])
    files = [file for file in glob("*.xlsx")]
    sheet_name = [mcap_sheet_name[0]]
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet, skiprows=1)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
            df_dict = df.to_dict(orient='records')

            for fund_code in fund_code_list:
                calc_market_cap(fund_code, df_dict)
