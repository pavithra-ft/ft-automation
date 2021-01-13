import re
import os
import numpy as np
import pandas as pd
from glob import glob
from model.FundTablesModel import FundBenchmarkNav
from config.basic_config import file_loc, nav_sheet_name
from database.db_queries import get_benchmark_index, get_alt_benchmark_index, put_fund_nav, iq_session


def calc_fund_nav(fund_code, df_dict):
    for index, row in enumerate(df_dict):
        if index == 0:
            fund_bm_data = FundBenchmarkNav()
            fund_bm_data.set_fund_code(fund_code)
            fund_bm_data.set_benchmark_index_code(get_benchmark_index(fund_code))
            fund_bm_data.set_alt_benchmark_index_code(get_alt_benchmark_index(fund_code))
            fund_bm_data.set_fund_nav(round((float(row['NAV']) / 100), 6))
            fund_bm_data.set_benchmark_nav('1')
            fund_bm_data.set_alt_benchmark_nav('1')
            fund_bm_data.set_effective_end_date(row['Date '])
        else:
            fund_bm_data = FundBenchmarkNav()
            fund_bm_data.set_fund_code(fund_code)
            fund_bm_data.set_benchmark_index_code(get_benchmark_index(fund_code))
            fund_bm_data.set_alt_benchmark_index_code(get_alt_benchmark_index(fund_code))
            fund_bm_data.set_fund_nav(round((float(row['NAV']) / 100), 6))
            fund_bm_data.set_effective_end_date(row['Date '])
        try:
            put_fund_nav(fund_bm_data)
            iq_session.commit()
        except Exception as error:
            iq_session.rollback()
            print('Exception raised:', error)
        finally:
            iq_session.close()


def get_fund_nav(fund_code_list):
    os.chdir(file_loc[0])
    files = [file for file in glob("*.xlsx")]
    sheet_name = [nav_sheet_name[0]]
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
            df_dict = df.to_dict(orient='records')

            for fund_code in fund_code_list:
                calc_fund_nav(fund_code, df_dict)
