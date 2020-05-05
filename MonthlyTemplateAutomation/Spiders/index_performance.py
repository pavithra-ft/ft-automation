import numpy as np
import re
import os
import pandas as pd
import calendar
import MySQLdb

from envparse import env
from glob import glob
from dateutil.relativedelta import relativedelta
from datetime import datetime
from Spiders.db_actions import get_benchmark_index, get_index_price_as_on_date, get_alt_benchmark_index, \
    put_index_performance
from Spiders.template_excel_extraction import get_fund_info


def get_1m_date(effective_end_date):
    previous_1m_date = effective_end_date - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1])
    return previous_1m_end_date


def get_3m_date(effective_end_date):
    previous_3m_date = effective_end_date - relativedelta(months=3)
    previous_3m_end_date = previous_3m_date.replace(day=calendar.monthrange(previous_3m_date.year,
                                                                            previous_3m_date.month)[1])
    return previous_3m_end_date


def get_6m_date(effective_end_date):
    previous_6m_date = effective_end_date - relativedelta(months=6)
    previous_6m_end_date = previous_6m_date.replace(day=calendar.monthrange(previous_6m_date.year,
                                                                            previous_6m_date.month)[1])
    return previous_6m_end_date


def get_1y_date(effective_end_date):
    previous_1y_date = effective_end_date - relativedelta(years=1)
    previous_1y_end_date = (previous_1y_date.replace(day=calendar.monthrange(previous_1y_date.year,
                                                                             previous_1y_date.month)[1]))
    return previous_1y_end_date


def get_2y_date(effective_end_date):
    previous_2y_date = effective_end_date - relativedelta(years=2)
    previous_2y_end_date = previous_2y_date.replace(day=calendar.monthrange(previous_2y_date.year,
                                                                            previous_2y_date.month)[1])
    return previous_2y_end_date


def get_3y_date(effective_end_date):
    previous_3y_date = effective_end_date - relativedelta(years=3)
    previous_3y_end_date = previous_3y_date.replace(day=calendar.monthrange(previous_3y_date.year,
                                                                            previous_3y_date.month)[1])
    return previous_3y_end_date


def get_5y_date(effective_end_date):
    previous_5y_date = effective_end_date - relativedelta(years=5)
    previous_5y_end_date = previous_5y_date.replace(day=calendar.monthrange(previous_5y_date.year,
                                                                            previous_5y_date.month)[1])
    return previous_5y_end_date


def get_start_date(index_code, database):
    start_date_cursor = database.cursor()
    start_date_query = "SELECT index_price_as_on_date FROM iq.index_prices where index_code ='" + index_code \
                       + "' order by index_price_as_on_date asc limit 1"
    start_date_cursor.execute(start_date_query)
    start_date_details = start_date_cursor.fetchall()
    start_date = start_date_details[0][0]
    return start_date


def get_start_price(start_date, index_code, database):
    start_nav_cursor = database.cursor()
    start_index_price_query = "SELECT ip.index_price_close from index_prices ip where ip.index_code = '" + index_code \
                              + "' and index_price_as_on_date = '" + str(start_date) + "'"
    start_nav_cursor.execute(start_index_price_query)
    start_index_price_details = start_nav_cursor.fetchall()
    start_index_price = start_index_price_details[0][0]
    return start_index_price


def get_index_performance(fund_info, index_code, iq_database):
    start_date = get_start_date(index_code, iq_database)
    start_index_price = get_start_price(start_date, index_code, iq_database)
    effective_end_date = datetime.strptime(fund_info['reporting_date'], '%Y-%m-%d %H:%M:%S').date()
    curr_price = get_index_price_as_on_date(effective_end_date, index_code, iq_database)
    perf_1m_date = get_1m_date(effective_end_date)
    perf_3m_date = get_3m_date(effective_end_date)
    perf_6m_date = get_6m_date(effective_end_date)
    perf_1y_date = get_1y_date(effective_end_date)
    perf_2y_date = get_2y_date(effective_end_date)
    perf_3y_date = get_3y_date(effective_end_date)
    perf_5y_date = get_5y_date(effective_end_date)
    perf_1m = None
    perf_3m = None
    perf_6m = None
    perf_1y = None
    perf_2y = None
    perf_3y = None
    perf_5y = None
    # Calculation of 1 month index performance
    if start_date <= perf_1m_date:
        index_1m_price = get_index_price_as_on_date(perf_1m_date, index_code, iq_database)
        perf_1m = round(((curr_price[0][0] / index_1m_price[0][0]) - 1), 4)
    # Calculation of 3 months index performance
    if start_date <= perf_3m_date:
        index_3m_price = get_index_price_as_on_date(perf_3m_date, index_code, iq_database)
        perf_3m = round(((curr_price[0][0] / index_3m_price[0][0]) - 1), 4)
    # Calculation of 6 months index performance
    if start_date <= perf_6m_date:
        index_6m_price = get_index_price_as_on_date(perf_6m_date, index_code, iq_database)
        perf_6m = round(((curr_price[0][0] / index_6m_price[0][0]) - 1), 4)
    # Calculation of 1 year index performance
    if start_date <= perf_1y_date:
        index_1y_price = get_index_price_as_on_date(perf_1y_date, index_code, iq_database)
        date_power_1y = effective_end_date - perf_1y_date
        perf_1y = round((((curr_price[0][0] / index_1y_price[0][0]) ** (365 / date_power_1y.days)) - 1), 4)
    # Calculation of 2 years index performance
    if start_date <= perf_2y_date:
        index_2y_price = get_index_price_as_on_date(perf_2y_date, index_code, iq_database)
        date_power_2y = effective_end_date - perf_2y_date
        perf_2y = round((((curr_price[0][0] / index_2y_price[0][0]) ** (365 / date_power_2y.days)) - 1), 4)
    # Calculation of 3 years index performance
    if start_date <= perf_3y_date:
        index_3y_price = get_index_price_as_on_date(perf_3y_date, index_code, iq_database)
        date_power_3y = effective_end_date - perf_3y_date
        perf_3y = round((((curr_price[0][0] / index_3y_price[0][0]) ** (365 / date_power_3y.days)) - 1), 4)
    # Calculation of 5 years index performance
    if start_date <= perf_5y_date:
        index_5y_price = get_index_price_as_on_date(perf_5y_date, index_code, iq_database)
        date_power_5y = effective_end_date - perf_5y_date
        perf_5y = round((((curr_price[0][0] / index_5y_price[0][0]) ** (365 / date_power_5y.days)) - 1), 4)
    # Calculation of index performance inception
    power_inception = effective_end_date - start_date
    perf_inception = round((((curr_price[0][0] / start_index_price) ** (365 / power_inception.days)) - 1), 4)
    index_perf_data = {"index_code": index_code, "perf_1m": perf_1m, "perf_3m": perf_3m, "perf_6m": perf_6m,
                       "perf_1y": perf_1y, "perf_2y": perf_2y, "perf_3y": perf_3y, "perf_5y": perf_5y,
                       "perf_inception": perf_inception}
    return index_perf_data


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

            iq_db, fs_db, app_db = 'iq', 'fs', 'app'
            # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
            db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                        'd0m#l1dZwhz!*9Iq0y1h'
            iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db, use_unicode=True, charset="utf8")
            fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db, use_unicode=True, charset="utf8")
            app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db, use_unicode=True, charset="utf8")

            fund_info = get_fund_info(df)
            benchmark_index_code = get_benchmark_index(fund_info, iq_database)
            alt_benchmark_index_code = get_alt_benchmark_index(fund_info, iq_database)
            index_code_list = [benchmark_index_code, alt_benchmark_index_code]
            for index_code in index_code_list:
                index_perf_data = get_index_performance(fund_info, index_code, iq_database)
                put_index_performance(index_perf_data, iq_database)
                print(index_perf_data)

            # Database commit
            iq_database.commit()
            print(fund_info['reporting_date'], ": Fund code - ", fund_info['fund_code'], "Index updated successfully")
            # Closing the database connection
            iq_database.close()
            fs_database.close()
            app_database.close()

except Exception as error:
    print("Exception raised :", error)
