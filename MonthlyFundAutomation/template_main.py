import os
import re
import numpy as np
import pandas as pd
import database.db_actions as query
import service.template_extraction as extraction
from glob import glob
from config.base_logger import app_logger, sql_logger
from service.date_calculation import get_1m_date
from service.fund_calculation import table_records
from database.db_actions import iq_session, app_session, fs_session


def get_fund_record(file, sheet):
    fund_data = fund_info = None
    try:
        app_logger.info('Conversion of Excel to Dataframe string is started')
        df_read = pd.read_excel(file, sheet_name=sheet)
        df_str = df_read.astype(str)
        df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
        app_logger.info('Conversion of Excel to Dataframe string is completed')

        app_logger.info('Extraction of Fund information is started')
        fund_info = extraction.get_fund_info(df)
        allocation_values = extraction.get_fund_allocation_values(df)
        market_cap_values = extraction.get_market_cap_values(df)
        portfolio_values = extraction.get_fund_portfolio_values(df)
        sector_values = extraction.get_fund_sector_values(df)
        app_logger.info('Extraction of Fund information is completed')

        app_logger.info('Fund calculation is started')
        fund_data = table_records(fund_info, allocation_values, market_cap_values, portfolio_values, sector_values)
        app_logger.info('Fund calculation is success and completed')
    except Exception as error:
        app_logger.info('Exception raised in calculation: '+str(error))
    return fund_data, fund_info


def put_fund_record(fund_data, fund_info):
    try:
        previous_1m_end_date = get_1m_date(fund_info.get_reporting_date())
        query.update_islatest(fund_info.get_fund_code(), previous_1m_end_date)
        query.put_fund_benchmark_nav(fund_data['nav'])
        query.put_fund_performance(fund_data['fund_perf'], fund_data['benchmark_perf'], fund_data['alt_benchmark_perf'])
        query.put_market_cap(fund_data['market_cap'])
        query.put_fund_portfolio(fund_data['portfolio'])
        query.put_fund_sector(fund_data['sector'])
        query.put_fund_ratios(fund_data['ratios'])
        query.put_collaterals(fund_data['collaterals'])
        app_logger.info(str(fund_info.get_reporting_date()) + ' - ' + fund_info.get_fund_code() +
                        ' Record inserted successfully')
        sql_logger.info(str(fund_info.get_reporting_date()) + ' - ' + fund_info.get_fund_code() +
                        ' Record inserted successfully')
        fs_session.commit()
        iq_session.commit()
    except Exception as error:
        fs_session.rollback()
        iq_session.rollback()
        app_logger.info('Exception raised in queries: '+str(error))
    finally:
        app_session.close()
        fs_session.close()
        iq_session.close()


if __name__ == "__main__":
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\MonthlyFundAutomation\excel_files")
    files = [file for file in glob("*.xlsx")]
    sheet_name = ['Fund Perf Update - Template']
    for file in files:
        for sheet in sheet_name:
            app_logger.info('Fund code - ' + file.split('_')[0])
            sql_logger.info('Fund code - ' + file.split('_')[0])
            fund_data, fund_info = get_fund_record(file, sheet)
            put_fund_record(fund_data, fund_info)