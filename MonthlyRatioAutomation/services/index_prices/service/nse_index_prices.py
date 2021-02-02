import calendar
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database.db_queries import iq_session
from dateutil.relativedelta import relativedelta
from database.db_queries import put_index_prices
from config.base_logger import app_logger, sql_logger
from dictionary.nse_index_prices_dict import nse_index_prices_urls


def get_index_data(index_code, html_content):
    app_logger.info('Index Prices - Extraction ' + '(' + index_code + ')' + 'of NSE index prices is started')

    soup = BeautifulSoup(html_content.text, features="lxml")
    table = soup.find('table')
    table_row = table.find_all('tr')
    t_headers = ['Date', 'Open', 'High', 'Low', 'Close']
    table_data = []

    for tr in table_row:
        t_row = {}
        for td, th in zip(tr.find_all('td'), t_headers):
            t_row[th] = td.text.replace('\n', '').strip()
            t_row.update({'index_code': index_code})
        table_data.append(t_row)

    if index_code != 'NIFVIX':
        index_price_data = table_data[3:-1]
        for row in index_price_data:
            row['Date'] = datetime.strptime(row['Date'], '%d-%b-%Y').date()
    else:
        index_price_data = table_data[4:-1]
        for row in index_price_data:
            row['Date'] = datetime.strptime(row['Date'], '%d-%b-%Y').date()
    try:
        put_index_prices(index_price_data)
        iq_session.commit()
    except Exception as error:
        iq_session.rollback()
        app_logger.info('Exception raised in queries : ' + str(error))
    finally:
        iq_session.close()
    app_logger.info('Index Prices - Extraction ' + '(' + index_code + ')' + ' of NSE index prices is completed')


def get_nse_index(historical_url):
    app_logger.info('Index Prices - NSE is started')
    sql_logger.info('Index Prices - NSE is started')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.61 Safari/537.36'}

    current_date = datetime.now() - relativedelta(months=1)

    for index_code, url in nse_index_prices_urls.items():
        if index_code != 'NIFVIX':
            start_date = datetime.strftime(current_date.replace(day=1), '%d-%m-%Y')
            end_date = datetime.strftime(current_date.replace(day=calendar.
                                                              monthrange(current_date.year,
                                                                         current_date.month)[1]), '%d-%m-%Y')
            html_content = requests.get(historical_url[0] + url.format(start_date, end_date), headers=headers)
            get_index_data(index_code, html_content)
        else:
            start_date = datetime.strftime(current_date.replace(day=1), '%d-%b-%Y')
            end_date = datetime.strftime(current_date.replace(day=calendar.
                                                              monthrange(current_date.year,
                                                                         current_date.month)[1]), '%d-%b-%Y')
            html_content = requests.get(historical_url[0] + url.format(start_date, end_date), headers=headers)
            get_index_data(index_code, html_content)
    app_logger.info('Index Prices - NSE is completed')
    sql_logger.info('Index Prices - NSE is completed')
