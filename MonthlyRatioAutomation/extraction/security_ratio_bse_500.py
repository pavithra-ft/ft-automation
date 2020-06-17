import json

from requests import get
from bs4 import BeautifulSoup

security_ratio_url = "https://www.valueresearchonline.com/stocks/selector-data/indices/46/bse-500-index/?custom-cols" \
                     "=pe%2Cpb%2Cdy%2Ceps&output=html-data&draw=1&start=0&length=501 "


def get_security_ratio():
    response = get(security_ratio_url)
    security_ratio_list = []
    for data in json.loads(response.content)['data']:
        text_label = ['securtiy_name', 'price_to_earnings', 'price_to_book', 'dividend_yield', 'earning_per_share']
        text_values = []
        for index, row in enumerate(data):
            if index != 1:
                text = BeautifulSoup(row, 'html.parser').text
                if index == 0:
                    text = text.split('\n')[0]
                text_values.append(text)
        security_values = [i for i in text_values if i]
        security_ratio_list.append(dict(zip(text_label, security_values)))
    return security_ratio_list
