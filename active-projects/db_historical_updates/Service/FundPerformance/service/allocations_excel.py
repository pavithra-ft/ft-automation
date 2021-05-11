import re
import os
import numpy as np
import pandas as pd
from glob import glob
from model.FundTablesModel import FundPerformance
from config.basic_config import file_loc, allocation_sheet_name
from database.db_queries import put_equity_allocation, put_cash_allocation, iq_session


def get_equity_allocation(fund_code, row):
    allocation_body = FundPerformance()
    allocation_body.set_fund_code(fund_code)
    allocation_body.set_portfolio_equity_allocation(round(float(row['%']), 6))
    allocation_body.set_effective_end_date(row['Date'])
    try:
        put_equity_allocation(allocation_body)
        iq_session.commit()
    except Exception as error:
        iq_session.rollback()
        print("Exception raised :", error)
    finally:
        iq_session.close()


def get_cash_allocation(fund_code, row):
    allocation_body = FundPerformance()
    allocation_body.set_fund_code(fund_code)
    allocation_body.set_portfolio_cash_allocation(round(float(row['%']), 6))
    allocation_body.set_effective_end_date(row['Date'])
    try:
        put_cash_allocation(allocation_body)
    except Exception as error:
        iq_session.rollback()
        print("Exception raised :", error)
    finally:
        iq_session.close()


def get_allocations(fund_code_list):
    os.chdir(file_loc[0])
    files = [file for file in glob("*.xlsx")]
    sheet_name = [allocation_sheet_name[0]]
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet, skiprows=1)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
            df_dict = df.to_dict(orient='records')

            for fund_code in fund_code_list:
                for row in df_dict:
                    if row['Allocation'] == 'EQUITY':
                        get_equity_allocation(fund_code, row)
                    elif row['Allocation'] == 'CASH':
                        get_cash_allocation(fund_code, row)
