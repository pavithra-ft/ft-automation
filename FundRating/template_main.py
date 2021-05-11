import os
import re
import numpy as np
import pandas as pd
from glob import glob
from config.base_logger import app_logger, sql_logger
from Service.template_extraction import get_fund_info, get_fund_portfolio_values
from Service.credit_risk_fund_calculation import get_security_rating, get_fund_rating, put_rating_record

if __name__ == "__main__":
    os.chdir(r"/excel")
    files = [file for file in glob("*.xlsx")]
    sheet_names = ['Sheet1']

    for file in files:
        for sheet in sheet_names:
            app_logger.info('Fund code - ' + file.split('_')[0])
            sql_logger.info('Fund code - ' + file.split('_')[0])

            df_read = pd.read_excel(file, sheet_name=sheet, skiprows=2)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)

            fund_info = get_fund_info(df)
            portfolio_values = get_fund_portfolio_values(df)

            security_rating_list = get_security_rating(fund_info, portfolio_values)
            fund_rating_data = get_fund_rating(fund_info)
            put_rating_record(fund_info, security_rating_list, fund_rating_data)
