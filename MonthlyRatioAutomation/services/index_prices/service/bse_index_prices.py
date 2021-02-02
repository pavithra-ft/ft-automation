import calendar
from datetime import datetime
import requests
from dateutil.relativedelta import relativedelta
from config.base_logger import app_logger, sql_logger
from database.db_queries import iq_session, put_index_prices
from dictionary.bse_index_prices_dict import bse_index_prices_urls


def get_bse_index(historical_url):
    app_logger.info('Index Prices - Extraction of BSE index prices is started')
    sql_logger.info('Index Prices - Extraction of BSE index prices is started')
    current_date = datetime.now() - relativedelta(months=1)
    start_date = datetime.strftime(current_date.replace(day=1), '%d-%m-%Y').split('-')
    end_date = datetime.strftime(current_date.replace(day=calendar.monthrange(
        current_date.year, current_date.month)[1]), '%d-%m-%Y').split('-')

    for index_code, url in bse_index_prices_urls.items():
        headers = {'accept': 'application/json, text/plain, */*',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'en-US,en;q=0.9',
                   'origin': 'https://www.bseindia.com',
                   'referer': 'https://www.bseindia.com/Indices/IndexArchiveData.html',
                   'sec-fetch-dest': 'empty',
                   'sec-fetch-mode': 'cors',
                   'sec-fetch-site': 'same-site',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/84.0.4147.135 Safari/537.36'}

        app_logger.info('Index Prices - Extraction(' + index_code + ') from site is started')
        html_content = requests.get(url=historical_url[0] + url.format(start_date[0], start_date[1], start_date[2],
                                                                       end_date[0], end_date[1], end_date[2]),
                                    headers=headers)
        json_data = html_content.json()
        index_price_data = []
        for data in json_data['Table']:
            index_body = {}
            index_body.update({'index_code': index_code})
            index_body.update({'Open': data['I_open']})
            index_body.update({'High': data['I_high']})
            index_body.update({'Low': data['I_low']})
            index_body.update({'Close': data['I_close']})
            index_body.update({'Date': data['tdate'][0:10]})
            index_price_data.append(index_body)
        app_logger.info('Index Prices - Extraction(' + index_code + ') from site is completed')
        try:
            put_index_prices(index_price_data)
            iq_session.commit()
        except Exception as error:
            iq_session.rollback()
            app_logger.info('Exception raised in queries : ' + str(error))
        finally:
            iq_session.close()
    app_logger.info('Index Prices - Extraction of BSE index prices is completed')
    sql_logger.info('Index Prices - Extraction of BSE index prices is completed')
