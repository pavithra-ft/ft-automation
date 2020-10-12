import os
from glob import glob
from config.base_logger import app_logger, sql_logger
from service.put_fund import get_fund_record, put_fund_record

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
