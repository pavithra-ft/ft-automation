import os
import re
import datetime
import numpy as np
import pandas as pd
from glob import glob
from datetime import datetime
from config.basic_config import sector_sheet_name, file_loc
from model.FundTablesModel import FundSector
from database.db_queries import put_fund_sector, iq_session


def calc_fund_sector(fund_code, df_dict):
    sector_data_list = []
    for row in df_dict:
        if row['%']:
            sectorBody = FundSector()
            sectorBody.set_fund_code(fund_code)
            sectorBody.set_sector_type_name(row['Sector'])
            sectorBody.set_exposure(round(float(row['%']), 4))
            sectorBody.set_start_date(datetime.strptime(row['Date'], '%Y-%m-%d').replace(day=1))
            sectorBody.set_end_date(row['Date'])
            sectorBody.set_created_ts(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            sectorBody.set_action_by('ft-automation')
            sector_data_list.append(sectorBody)
    try:
        put_fund_sector(sector_data_list)
        iq_session.commit()
    except Exception as error:
        iq_session.rollback()
        print("Exception raised :", error)
    finally:
        iq_session.close()


def get_fund_sector_details(fund_code_list):
    os.chdir(file_loc[0])
    files = [file for file in glob("*.xlsx")]
    sheet_names = [sector_sheet_name[0]]
    for file in files:
        for sheet in sheet_names:
            df_read = pd.read_excel(file, sheet_name=sheet, skiprows=1)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
            df_dict = df.to_dict(orient='records')

            for fund_code in fund_code_list:
                calc_fund_sector(fund_code, df_dict)
