import MySQLdb
from envparse import env
import datetime


def get_fintuple_template(fs_database):
    template_cursor = fs_database.cursor()
    template_query = "SELECT template_code from fs.collateral_templates where template_type_code = 'FINTUPLE' order " \
                     "by template_code"
    template_cursor.execute(template_query)
    template_code = template_cursor.fetchall()
    template_code_list = list(template_code)
    return template_code_list


def get_collateral_data(template_code, fs_database):
    collateral_cursor = fs_database.cursor()
    collateral_query = "SELECT collateral_title, entity_code, reporting_date from fs.collaterals where " \
                       "template_code = '" + template_code + "' order by reporting_date"
    collateral_cursor.execute(collateral_query)
    collateral_details = collateral_cursor.fetchall()
    collateral_list = list(collateral_details)
    collateral_cursor.close()
    return collateral_list


def get_fund_short_code(entity_code, app_database):
    print(entity_code)
    short_code_cursor = app_database.cursor()
    short_code_query = "SELECT fund_short_code from app.per_all_funds where fund_code = '" + entity_code + "'"
    short_code_cursor.execute(short_code_query)
    fund_short_code = short_code_cursor.fetchall()
    short_code_cursor.close()
    return fund_short_code[0][0]


def update_collateral_title(entity_code, fund_short_code, reporting_date, fs_database):
    title_cursor = fs_database.cursor()
    collateral_title = fund_short_code + ' Fintuple Factsheet'
    title_query = "UPDATE fs.collaterals SET collateral_title = '" + collateral_title + "' where reporting_date = '" + \
                  str(reporting_date) + "' and entity_type = 'FUND' and created_by = 'ft-automation' and entity_code " \
                                        "= '" + entity_code + "'"
    title_cursor.execute(title_query)
    title_cursor.close()


try:
    db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    # db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', 'd0m#l1dZwhz!*9Iq0y1h'
    iq_db, fs_db, app_db = 'iq', 'fs', 'app'

    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db)
    fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db)
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db)

    template_code_list = get_fintuple_template(fs_database)
    for template_code in template_code_list:
        collateral_data = get_collateral_data(template_code[0], fs_database)
        for collateral in collateral_data:
            print(collateral)
            fund_short_code = get_fund_short_code(collateral[1], app_database)
            update_collateral_title(collateral[1], fund_short_code, collateral[2], fs_database)

    # Commit changes
    fs_database.commit()
    # Close database connection
    iq_database.close()
    fs_database.close()
    app_database.close()

except Exception as error:
    print("Exception raised :", error)
