import numpy as np
import datetime
import os
from glob import glob
import pandas as pd
import re
import MySQLdb
from envparse import env
from pyjarowinkler import distance


def get_all_isin(database):
    isin_cursor = database.cursor()
    isin_query = "SELECT security_id, security_isin, security_name from iq.mas_securities"
    isin_cursor.execute(isin_query)
    security_details = isin_cursor.fetchall()
    isin_cursor.close()
    return security_details


def get_isin(company_name, database):
    comp_name = company_name.replace(".", " ")
    cleaned_comp_name = re.sub(r'(?<=\b[a-z]) (?=[a-z]\b)', '', comp_name).lower()
    security_details = get_all_isin(database)
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


def put_sf_data(sf_data, database):
    sf_cursor = database.cursor()
    sf_query = "INSERT INTO iq.securities_fundamentals (security_id, security_isin, as_on_date, market_cap, pe_ratio)" \
               " VALUES (%s, %s, %s, %s, %s)"
    sf_values = (sf_data['security_id'], sf_data['security_isin'], sf_data['as_on_date'], sf_data['market_cap'],
                 sf_data['pe_ratio'])
    sf_cursor.execute(sf_query, sf_values)
    print(sf_data)
    # sf_cursor.close()


try:
    os.chdir(r"C:\Users\pavithra\PycharmProjects\db_updates\Excel")
    files = [file for file in glob("*.xlsx")]
    # db_host, db_user, db_pass, db_name = env('DB_HOST'), env('DB_USER'), env('DB_PASS'), env('DB_NAME')
    db_host, db_user, db_pass, db_name = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                         'd0m#l1dZwhz!*9Iq0y1h', 'iq'
    database = MySQLdb.connect(db_host, db_user, db_pass, db_name, use_unicode=True, charset="utf8")
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
            if price_earnings is not None:
                pe_ratio = price_earnings
            else:
                pe_ratio = None
            for db_name, excel_name in comp_name_dict.items():
                if company_name == excel_name:
                    company_name = db_name
            security_id, security_isin = get_isin(company_name, database)
            sf_data = {"security_id": security_id, "security_isin": security_isin, "as_on_date": as_on_date,
                       "market_cap": market_cap, "pe_ratio": pe_ratio}
            put_sf_data(sf_data, database)
    database.commit()
    database.close()

except Exception as error:
    print("Exception raised :", error)
