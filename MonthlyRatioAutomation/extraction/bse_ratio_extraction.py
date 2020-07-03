import os
import json
import requests
from glob import glob
from config.base_logger import app_logger
from dictionary.bse_ratio_dict import bse_ratio_api


def get_bse_pe_ratio(pe_ratio_api_dict):
    app_logger.info('Index Performance - BSE : PE ratio extraction is started')
    bse_pe_list = []
    for index_code, api_url in pe_ratio_api_dict.items():
        pe_ratio_request = requests.get(url=api_url)
        pe_data = pe_ratio_request.json()
        for data in pe_data:
            if data.__contains__('PE'):
                pe_body = {'index_code': index_code, 'pe_ratio': float(data['PE'].replace(',', ''))}
                bse_pe_list.append(pe_body)
    app_logger.info('Index Performance - BSE : PE ratio extraction is completed')
    return bse_pe_list


def get_bse_data():
    app_logger.info('Index Performance - BSE : Sector/Holding extraction is started')
    bse_list = []
    bse_pe_list = get_bse_pe_ratio(bse_ratio_api)
    for pe_index in bse_pe_list:
        if pe_index['index_code'] == 'BSE30':
            bse_body = {'index_code': pe_index['index_code'], 'standard_deviation': None,
                        'pe_ratio': pe_index['pe_ratio'], 'top_sector_name': None, 'top_sector_exposure': None,
                        'top_holding_isin': None, 'top_holding_exposure': None}
            bse_list.append(bse_body)
        for sector_index in bse_sector_data:
            if sector_index['index_code'] == pe_index['index_code']:
                bse_body = {'index_code': pe_index['index_code'], 'standard_deviation': None,
                            'pe_ratio': pe_index['pe_ratio'], 'top_sector_name': sector_index['sector_name'],
                            'top_sector_exposure': round((float(sector_index['sector_exposure']) / 100), 4),
                            'top_holding_isin': None, 'top_holding_exposure': None}
                bse_list.append(bse_body)
    app_logger.info('Index Performance - BSE : Sector/Holding extraction is completed')
    return bse_list


try:
    os.chdir(r'C:\Users\pavithra\Documents\fintuple-automation-projects\RatioExtraction\ratio_extraction'
             r'\ratio_extraction\extracted_data')
    bse_sector_file = [file for file in glob("*.json")]
    for file in bse_sector_file:
        with open(file) as f:
            bse_sector_data = json.load(f)

except Exception as error:
    print("Exception raised :", error)
