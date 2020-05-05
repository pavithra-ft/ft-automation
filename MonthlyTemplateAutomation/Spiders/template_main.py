import os
import re
import MySQLdb
import numpy as np
import pandas as pd

from envparse import env
from glob import glob
from Spiders.db_actions import put_fund_performance, put_nav_data
from Spiders.template_calculation import table_records, get_fund_performance
from Spiders.template_excel_extraction import get_fund_info, get_fund_allocation_values, get_market_cap_values, \
    get_fund_portfolio_values, get_fund_sector_values

try:
    os.chdir(r"C:\Users\pavithra\PycharmProjects\MonthlyTemplateAutomation\Excel files")
    files = [file for file in glob("*.xlsx")]
    sheet_name = ['Fund Performance Update']
    for file in files:
        for sheet in sheet_name:
            df_read = pd.read_excel(file, sheet_name=sheet)
            # Excel clean-up
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
            # Database connection
            iq_db, fs_db, app_db = 'iq', 'fs', 'app'
            # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
            db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                        'd0m#l1dZwhz!*9Iq0y1h'
            iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db, use_unicode=True, charset="utf8")
            fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db, use_unicode=True, charset="utf8")
            app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db, use_unicode=True, charset="utf8")
            # Excel extraction
            fund_info = get_fund_info(df)
            allocation_values = get_fund_allocation_values(df)
            market_cap_values = get_market_cap_values(df)
            portfolio_values = get_fund_portfolio_values(df)
            sector_values = get_fund_sector_values(df)
            excel_values = {"fund_info": fund_info, "allocation_values": allocation_values,
                            "market_cap_values": market_cap_values, "portfolio_values": portfolio_values,
                            "sector_values": sector_values}
            # Calculation of the tables
            final_data = table_records(excel_values, iq_database, fs_database, app_database)

            # Inserting all the records of tables
            put_fund_performance(final_data['fund_perf_data'], final_data['benchmark_perf_data'],
                                 final_data['alt_benchmark_perf_data'], iq_database)
            put_nav_data(final_data['nav_data'], iq_database)

            # Database commit
            iq_database.commit()
            fs_database.commit()
            print(fund_info['reporting_date'], ": Fund code - ", fund_info['fund_code'], "Record inserted successfully")
            # Closing the database connection
            iq_database.close()
            fs_database.close()
            app_database.close()


except Exception as error:
    print("Exception raised :", error)
