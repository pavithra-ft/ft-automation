import requests


def get_bse_data(pe_ratio_dict):
    bse_list = []
    for index_code, api_url in pe_ratio_dict.items():
        pe_ratio_request = requests.get(url=api_url)
        pe_data = pe_ratio_request.json()
        for data in pe_data:
            if data.__contains__('PE'):
                pe_body = {'index_code': index_code, 'standard_deviation': None, 'pe_ratio': data['PE'],
                           'sector_name': None, 'sector_exposure': None,
                           'portfolio_name': None, 'portfolio_exposure': None,
                           'reporting_date': None}
                bse_list.append(pe_body)
    return bse_list
