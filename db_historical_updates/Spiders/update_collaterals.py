import MySQLdb
from envparse import env
import datetime


def get_funds_list(iq_database):
    fund_cursor = iq_database.cursor()
    fund_query = "SELECT fund_code, effective_end_date from iq.fund_performance"
    fund_cursor.execute(fund_query)
    fund_list_details = fund_cursor.fetchall()
    fund_cursor.close()
    print(len(fund_list_details))
    return fund_list_details


def collateral_check(fund, fs_database):
    collateral_cursor = fs_database.cursor()
    collateral_check_query = "SELECT entity_code from fs.collaterals where entity_code = '" + fund[0] + \
                             "' and reporting_date = '" + str(fund[1]) + "'"
    collateral_cursor.execute(collateral_check_query)
    collateral_check_details = collateral_cursor.fetchall()
    collateral_cursor.close()
    return collateral_check_details


def get_collateral_code(fs_database):
    collateral_code_cursor = fs_database.cursor()
    collateral_code_query = "SELECT fs.codeGenerator('COLLATERAL')"
    collateral_code_cursor.execute(collateral_code_query)
    collateral_code_details = collateral_code_cursor.fetchall()
    collateral_code_cursor.close()
    collateral_code = collateral_code_details[0][0]
    return collateral_code


def get_collateral_view_code(fs_database):
    view_code_cursor = fs_database.cursor()
    view_code_query = "SELECT fs.codeGenerator('COLLATERAL-VIEW')"
    view_code_cursor.execute(view_code_query)
    view_code_details = view_code_cursor.fetchall()
    view_code_cursor.close()
    view_code = view_code_details[0][0]
    return view_code


def get_fund_short_code(fund, app_database):
    short_code_cursor = app_database.cursor()
    short_code_query = "SELECT fund_short_code from app.per_all_funds where fund_code = '" + fund[0] + "'"
    short_code_cursor.execute(short_code_query)
    short_code_details = short_code_cursor.fetchall()
    fund_short_code = short_code_details[0][0]
    short_code_cursor.close()
    return fund_short_code


def get_collateral_template_code(fund, fs_database):
    template_code_cursor = fs_database.cursor()
    template_code_query = "SELECT template_code from fs.collateral_templates ct WHERE ct.entity_code = '" + fund[0] + \
                          "' and ct.template_type_code = 'FINTUPLE' and (('" + str(fund[1]) + \
                          "' >= ct.effective_start_date and ct.effective_end_date IS NULL) or ('" + str(fund[1]) + \
                          "' BETWEEN ct.effective_start_date and ct.effective_end_date))"
    template_code_cursor.execute(template_code_query)
    template_code_details = template_code_cursor.fetchall()
    template_code = template_code_details[0][0]
    return template_code


def put_collateral_data(collateral_data, fs_database):
    db_cursor = fs_database.cursor()
    db_query = "INSERT INTO fs.collaterals (collateral_code, view_code, collateral_type_code, entity_type, " \
               "entity_code, collateral_title, visibility_code, template_code, collateral_date, " \
               "collateral_status, reporting_date, effective_start_date, is_premium, is_published, " \
               "published_ts, created_ts, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
               "%s, %s, %s, %s, %s, %s)"
    db_values = (collateral_data['collateral_code'], collateral_data['view_code'],
                 collateral_data['collateral_type_code'], collateral_data['entity_type'],
                 collateral_data['entity_code'], collateral_data['collateral_title'],
                 collateral_data['visibility_code'], collateral_data['template_code'],
                 collateral_data['collateral_date'], collateral_data['collateral_status'],
                 collateral_data['reporting_date'], collateral_data['effective_start_date'],
                 collateral_data['is_premium'], collateral_data['is_published'],
                 collateral_data['published_ts'], collateral_data['created_ts'], collateral_data['created_by'])
    db_cursor.execute(db_query, db_values)
    print(collateral_data['entity_code'], collateral_data['reporting_date'])
    db_cursor.close()


def get_collateral_data(fund, fs_database):
    collateral_code = get_collateral_code(fs_database)
    view_code = get_collateral_view_code(fs_database)
    collateral_type_code = "FACTSHEET"
    entity_type = "FUND"
    entity_code = fund[0]
    fund_short_code = get_fund_short_code(fund, app_database)
    title_date = datetime.datetime.strptime(str(fund[1]), '%Y-%m-%d').date()
    title_month = datetime.date(title_date.year, title_date.month, title_date.day).strftime('%b')
    title_year = title_date.year
    collateral_title = fund_short_code + " Fintuple Standard Factsheet - " + title_month + " " + str(title_year)
    visibility_code = "PUBLIC"
    template_code = get_collateral_template_code(fund, fs_database)
    collateral_date = fund[1] + datetime.timedelta(days=1)
    collateral_status = "PUBLISHED"
    reporting_date = fund[1]
    effective_start_date = collateral_date
    is_premium = 0
    is_published = 1
    published_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_by = "ft-automation"
    return collateral_code, view_code, collateral_type_code, entity_type, entity_code, collateral_title, \
           visibility_code, template_code, collateral_date, collateral_status, reporting_date, effective_start_date, \
           is_premium, is_published, published_ts, created_ts, created_by


try:
    db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    # app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db, use_unicode=True, charset="utf8")
    # db_host, db_user, db_pass= 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
    #                                    'd0m#l1dZwhz!*9Iq0y1h'
    iq_db = 'iq'
    fs_db = 'fs'
    app_db = 'app'

    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db)
    fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db)
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db)

    counter = 0
    fund_list = get_funds_list(iq_database)
    for fund in fund_list:
        # print(fund)
        collateral_value = collateral_check(fund, app_database)
        if len(collateral_value) == 0:
            # Collateral details
            collateral_code, view_code, collateral_type_code, entity_type, entity_code, collateral_title, visibility_code, \
            template_code, collateral_date, collateral_status, reporting_date, effective_start_date, is_premium, \
            is_published, published_ts, created_ts, created_by = get_collateral_data(fund, fs_database)

            collateral_data = {}
            collateral_data.update(({"collateral_code": collateral_code, "view_code": view_code,
                                     "collateral_type_code": collateral_type_code, "entity_type": entity_type,
                                     "entity_code": entity_code, "collateral_title": collateral_title,
                                     "visibility_code": visibility_code, "template_code": template_code,
                                     "collateral_date": collateral_date, "collateral_status": collateral_status,
                                     "reporting_date": reporting_date, "effective_start_date": effective_start_date,
                                     "is_premium": is_premium, "is_published": is_published,
                                     "published_ts": published_ts,
                                     "created_ts": created_ts, "created_by": created_by}))
            put_collateral_data(collateral_data, fs_database)
        else:
            counter += 1
    print(counter)
    # Close IQ database connection
    iq_database.commit()
    iq_database.close()
    # Close FS database connection
    fs_database.commit()
    fs_database.close()
    # Close App database connection
    app_database.commit()
    app_database.close()

except Exception as error:
    print("Exception raised :", error)
