import os
import re
import glob
import datetime
import numpy as np
import pandas as pd

from pyjarowinkler import distance

from model.FundTablesModel import FundPortfolio
from dictionary.portfolio_dictionary import portfolio_dict
from Service.date_calculation import get_effective_start_end_date
from database.db_queries import get_security_isin, get_all_isin, put_fund_portfolio


def get_isin(portfolio_value):
    if portfolio_dict.__contains__(portfolio_value['Security']):
        sec_name = portfolio_dict[portfolio_value['Security']]
    else:
        sec_name = portfolio_value['Security']
    isin_details = get_security_isin(sec_name)
    if len(isin_details) == 0:
        sec_name = sec_name.replace(".", " ").replace("'", " ")
        cleaned_sec_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', sec_name).lower()
        security_details = get_all_isin()
        max_ratio = 0
        max_index = 0
        for value in range(len(security_details)):
            name = security_details[value][1].replace(".", " ").replace("'", " ")
            cleaned_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', name).lower()
            ratio = distance.get_jaro_distance(cleaned_sec_name, cleaned_name, winkler=True, scaling=0.1)
            if ratio > 0 and max_ratio < ratio:
                max_ratio = ratio
                max_index = value
        security_isin = security_details[max_index][0]
    else:
        security_isin = isin_details[0][0]
    print(security_isin)
    return security_isin


def get_fund_portfolio(fund_code, portfolio_values):
    for row in portfolio_values:
        reporting_date = datetime.datetime.strptime(row['Date'], "%d-%m-%Y").date()
        effective_start_date, effective_end_date = get_effective_start_end_date(reporting_date)
        portfolio_body = FundPortfolio()
        portfolio_body.set_fund_code(fund_code)
        portfolio_body.set_security_isin(row['ISIN'])
        portfolio_body.set_exposure(round(float(row['%']), 4))
        portfolio_body.set_start_date(effective_start_date)
        portfolio_body.set_end_date(effective_end_date)
        portfolio_body.set_created_ts(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        portfolio_body.set_action_by('ft-automation')
        print(portfolio_body)
        put_fund_portfolio(portfolio_body)


try:
    sheet_names = ['Portfolio - Updated']
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\db_historical_updates\Excel")
    files = []
    for file in glob.glob("*.xlsx"):
        files.append(file)
    for file in files:
        for sheet in sheet_names:
            df_read = pd.read_excel(file, sheet_name=sheet)
            df_str = df_read.astype(str)
            df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x))
            fund_code_list = []
            for fund_code in fund_code_list:
                df_dict = df.to_dict(orient='records')
                get_fund_portfolio(fund_code, df_dict)

except Exception as error:
    print("Exception raised :", error)
