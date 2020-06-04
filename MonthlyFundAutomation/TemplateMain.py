import os
import re
import numpy as np
import pandas as pd

from glob import glob

from service.DateCalculation import get_1m_date
from service.FundCalculation import table_records
from service.TemplateExtraction import get_fund_info, get_fund_allocation_values, get_market_cap_values, \
    get_fund_portfolio_values, get_fund_sector_values
from database.db_actions import put_fund_benchmark_nav, put_fund_performance, put_market_cap, put_fund_portfolio, \
    put_fund_sector, put_fund_ratios, put_collaterals, update_islatest

try:
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\MonthlyFundAutomation\excel_files")
    files = [file for file in glob("*.xlsx")]
    sheet_name = ['Fund Perf Update - Template']
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)

            fund_info = get_fund_info(df)
            allocation_values = get_fund_allocation_values(df)
            market_cap_values = get_market_cap_values(df)
            portfolio_values = get_fund_portfolio_values(df)
            sector_values = get_fund_sector_values(df)
            previous_1m_end_date = get_1m_date(fund_info.get_reporting_date())

            fund_data = table_records(fund_info, allocation_values, market_cap_values, portfolio_values, sector_values)

            update_islatest(fund_info.get_fund_code(), previous_1m_end_date)
            put_fund_benchmark_nav(fund_data['nav'])
            put_fund_performance(fund_data['fund_perf'], fund_data['benchmark_perf'], fund_data['alt_benchmark_perf'])
            put_market_cap(fund_data['market_cap'])
            put_fund_portfolio(fund_data['portfolio'])
            put_fund_sector(fund_data['sector'])
            put_fund_ratios(fund_data['ratios'])
            put_collaterals(fund_data['collaterals'])

            print(fund_info.get_reporting_date(), '-', fund_info.get_fund_code(), 'Record inserted successfully')

except Exception as error:
    print("Exception raised :", error)
