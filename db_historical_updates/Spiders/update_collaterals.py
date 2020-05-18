import MySQLdb
from envparse import env
import datetime

from Spiders.db_actions import get_collateral_code, get_collateral_view_code, get_fund_short_code, \
    get_collateral_template_code, is_collaterals_exist, put_collateral_data, get_fund_dates


def get_collateral_data(fund_code, reporting_date, fs_database):
    collateral_code = get_collateral_code(fs_database)
    view_code = get_collateral_view_code(fs_database)
    collateral_type_code = "FACTSHEET"
    entity_type = "FUND"
    fund_short_code = get_fund_short_code(fund_code, app_database)
    collateral_title = fund_short_code + " Fintuple Factsheet"
    visibility_code = "PUBLIC"
    template_code = get_collateral_template_code(fund_code, reporting_date, fs_database)
    collateral_date = reporting_date + datetime.timedelta(days=1)
    collateral_status = "PUBLISHED"
    is_premium = 1
    is_published = 1
    is_data_changed = 1
    published_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = "ft-automation"
    collateral_data = {"collateral_code": collateral_code, "view_code": view_code,
                       "collateral_type_code": collateral_type_code, "entity_type": entity_type,
                       "entity_code": fund_code, "collateral_title": collateral_title,
                       "visibility_code": visibility_code, "template_code": template_code,
                       "collateral_date": collateral_date, "collateral_status": collateral_status,
                       "reporting_date": reporting_date, "effective_start_date": collateral_date,
                       "is_premium": is_premium, "is_published": is_published, "is_data_changed": is_data_changed,
                       "published_ts": published_ts, "created_ts": created_ts, "created_by": created_by}
    return collateral_data


try:
    # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', 'd0m#l1dZwhz!*9Iq0y1h'
    iq_db = 'iq'
    fs_db = 'fs'
    app_db = 'app'

    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db)
    fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db)
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db)
    fund_code_list = ['72966297']
    for fund_code in fund_code_list:
        fund_dates = get_fund_dates(fund_code, iq_database)
        for reporting_date in fund_dates:
            collateral_value = is_collaterals_exist(fund_code, reporting_date, fs_database)
            if collateral_value == 0:
                collateral_data = get_collateral_data(fund_code, reporting_date, fs_database)
                put_collateral_data(collateral_data, fs_database)

    fs_database.commit()

    iq_database.close()
    fs_database.close()
    app_database.close()

except Exception as error:
    print("Exception raised :", error)
