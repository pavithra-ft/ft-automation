import os
from glob import glob
from config.base_logger import app_logger, sql_logger
from config.elements import fund_files, template_sheet_name
from service.put_fund import get_fund_record, put_fund_record, delete_files

if __name__ == "__main__":
    os.chdir(fund_files[0])
    files = [file for file in glob("*.xlsx")]
    sheet_name = [template_sheet_name[0]]
    for file in files:
        for sheet in sheet_name:
            app_logger.info('Fund code - ' + file.split('_')[0])
            sql_logger.info('Fund code - ' + file.split('_')[0])
            fund_data, fund_info = get_fund_record(file, sheet)
            put_fund_record(fund_data, fund_info)
            delete_files(fund_info)
