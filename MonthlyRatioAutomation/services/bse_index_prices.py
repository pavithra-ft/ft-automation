import MySQLdb
import calendar
import requests

from envparse import env
from datetime import datetime
from dateutil.relativedelta import relativedelta

from dictionary.bse_index_prices_dict import bse_index_prices_urls
from services.db_actions import put_index_prices


def get_bse_index():
    historical_url = ['https://api.bseindia.com/BseIndiaAPI/api/IndexArchDaily']
    current_date = datetime.now() - relativedelta(months=1)
    start_date = datetime.strftime(current_date.replace(day=1), '%d-%m-%Y').split('-')
    end_date = datetime.strftime(current_date.replace(day=calendar.
                                                      monthrange(current_date.year,
                                                                 current_date.month)[1]), '%d-%m-%Y').split('-')
    for index_code, url in bse_index_prices_urls.items():
        html_content = requests.get(url=historical_url[0] + url.format(start_date[0], start_date[1], start_date[2],
                                                                       end_date[0], end_date[1], end_date[2]))
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
        put_index_prices(index_price_data, iq_database)
        print(index_price_data)


try:
    iq_db, fs_db, app_db = 'iq', 'fs', 'app'
    db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    # db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', 'd0m#l1dZwhz!*9Iq0y1h'
    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db, use_unicode=True, charset="utf8")
    fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db, use_unicode=True, charset="utf8")
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db, use_unicode=True, charset="utf8")

    get_bse_index()
    # Database commit
    iq_database.commit()
    print('Commit success')
    iq_database.close()
    fs_database.close()
    app_database.close()

except Exception as error:
    print('Exception raised:', error)
