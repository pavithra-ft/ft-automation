import MySQLdb
import calendar
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta

from dictionary.index_prices_dictionary import index_urls
from services.db_actions import put_index_prices


def get_index_data(index_code, html_content):
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
    put_index_prices(index_price_data, iq_database)
    print(index_price_data)
    return index_price_data


def get_index_main():
    historical_url = ['https://www1.nseindia.com/products/dynaContent/equities/indices']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.61 Safari/537.36'}

    current_date = datetime.now() - relativedelta(months=1)

    for index_code, url in index_urls.items():
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


try:
    iq_db, fs_db, app_db = 'iq', 'fs', 'app'
    # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    # db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', 'd0m#l1dZwhz!*9Iq0y1h'
    db_host, db_user, db_pass = '127.0.0.1', 'pavi', 'root'
    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db, use_unicode=True, charset="utf8")
    fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db, use_unicode=True, charset="utf8")
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db, use_unicode=True, charset="utf8")

    get_index_main()
    # Database commit
    iq_database.commit()
    print('Commit success')
    iq_database.close()
    fs_database.close()
    app_database.close()

except Exception as error:
    print('Exception raised:', error)
