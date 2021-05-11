import os
import re
import datetime
import numpy as np
import pandas as pd
from glob import glob
from pyjarowinkler import distance
from database.db_queries import get_all_isin, put_sec_fundamental_data


def get_isin(company_name):
    comp_name = company_name.replace(".", " ")
    cleaned_comp_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', comp_name).lower()
    security_details = get_all_isin()
    max_ratio = 0
    max_index = 0
    for value in range(len(security_details)):
        name = security_details[value][2].replace(".", " ")
        cleaned_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', name).lower()
        ratio = distance.get_jaro_distance(cleaned_comp_name, cleaned_name, winkler=True, scaling=0.1)
        if ratio > 0 and max_ratio < ratio:
            max_ratio = ratio
            max_index = value
    security_isin = security_details[max_index][1]
    security_id = security_details[max_index][0]
    return security_id, security_isin


try:
    os.chdir(r"C:\Users\pavithra\Documents\fintuple-automation-projects\db_historical_updates\Excel")
    files = [file for file in glob("*.xlsx")]
    comp_name_dict = {"D.B.Corp Limited": "DB Corporation Ltd.", "EID Parry India Limited": "EID-Parry (India) Ltd.",
                      "K.P.R. Mill Limited": "KPR Mills Ltd.", "NTPC Limited": "National Thermal Power Corp. Ltd.",
                      "Reliance Nippon Life Asset Management Ltd": "Nippon Life India Asset Management Ltd.",
                      "The Phoenix Mills Ltd": "Phoenix Mills Ltd.", "Tata Motors  Ltd - DVR": "Tata Motors DVR",
                      "VIP Industries Limited": "VIP Industries Ltd."}
    for file in files:
        df_read = pd.read_excel(file)
        df_str = df_read.astype(str)
        df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
        for i in range(len(df)):
            company_name, date, market_cap, price_earnings = df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 3]
            as_on_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            pe_ratio = price_earnings if price_earnings is not None else None
            for db_name, excel_name in comp_name_dict.items():
                if company_name == excel_name:
                    company_name = db_name
            security_id, security_isin = get_isin(company_name)
            sf_data = {"security_id": security_id, "security_isin": security_isin, "as_on_date": as_on_date,
                       "market_cap": market_cap, "pe_ratio": pe_ratio}
            put_sec_fundamental_data(sf_data)

except Exception as error:
    print("Exception raised :", error)
