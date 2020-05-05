import MySQLdb
from envparse import env
import datetime
import calendar
from dateutil.relativedelta import relativedelta


def get_nav_start_date(fund_code, database):
    nav_cursor = database.cursor()
    nav_query = "SELECT nav_start_date from app.per_all_funds where fund_code = '" + fund_code + "'"
    nav_cursor.execute(nav_query)
    nav_details = nav_cursor.fetchall()
    print("nav_details", nav_details)
    nav_start_date = nav_details[0][0]
    return nav_start_date


def get_1m_date(nav_start_date):
    eff_end_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d")
    previous_1m_date = eff_end_date - relativedelta(months=1)
    previous_1m_end_date = previous_1m_date.replace(day=calendar.monthrange(previous_1m_date.year,
                                                                            previous_1m_date.month)[1]).date()
    return previous_1m_end_date


def get_3m_date(nav_start_date):
    eff_end_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d")
    previous_3m_date = eff_end_date - relativedelta(months=3)
    previous_3m_end_date = previous_3m_date.replace(day=calendar.monthrange(previous_3m_date.year,
                                                                            previous_3m_date.month)[1]).date()
    return previous_3m_end_date


def get_6m_date(nav_start_date):
    eff_end_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d")
    previous_6m_date = eff_end_date - relativedelta(months=6)
    previous_6m_end_date = previous_6m_date.replace(day=calendar.monthrange(previous_6m_date.year,
                                                                            previous_6m_date.month)[1]).date()
    return previous_6m_end_date


def get_1y_date(nav_start_date):
    eff_end_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d")
    previous_1y_date = eff_end_date - relativedelta(years=1)
    previous_1y_end_date = (previous_1y_date.replace(day=calendar.monthrange(previous_1y_date.year,
                                                                             previous_1y_date.month)[1])).date()
    return previous_1y_end_date


def get_2y_date(nav_start_date):
    eff_end_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d")
    previous_2y_date = eff_end_date - relativedelta(years=2)
    previous_2y_end_date = previous_2y_date.replace(day=calendar.monthrange(previous_2y_date.year,
                                                                            previous_2y_date.month)[1]).date()
    return previous_2y_end_date


def get_3y_date(nav_start_date):
    eff_end_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d")
    previous_3y_date = eff_end_date - relativedelta(years=3)
    previous_3y_end_date = previous_3y_date.replace(day=calendar.monthrange(previous_3y_date.year,
                                                                            previous_3y_date.month)[1]).date()
    return previous_3y_end_date


def get_5y_date(nav_start_date):
    eff_end_date = datetime.datetime.strptime(str(nav_start_date), "%Y-%m-%d")
    previous_5y_date = eff_end_date - relativedelta(years=5)
    previous_5y_end_date = previous_5y_date.replace(day=calendar.monthrange(previous_5y_date.year,
                                                                            previous_5y_date.month)[1]).date()
    return previous_5y_end_date


def get_inception_date():
    since_inception_cursor = database.cursor()
    since_inception_query = "SELECT nav_start_date from app.per_all_funds where fund_code = '" + fund_code + "'"
    since_inception_cursor.execute(since_inception_query)
    inception_date = since_inception_cursor.fetchall()
    print("inception_date")
    since_inception_cursor.close()
    temp = str(inception_date[0][0])
    inception_date = datetime.datetime.strptime(temp, '%Y-%m-%d').date()
    return inception_date


def get_alt_benchmark_index(fund_code):
    alt_benchmark_index_cursor = database.cursor()
    alt_benchmark_index_query = "SELECT fund_code, alt_benchmark_index_code, effective_end_date FROM " \
                                "fund_benchmark_nav where fund_code = '" + fund_code + \
                                "' order by effective_end_date asc"
    alt_benchmark_index_cursor.execute(alt_benchmark_index_query)
    alt_bm_details = alt_benchmark_index_cursor.fetchall()
    print("alt_bm_details", alt_bm_details)
    alt_benchmark_index_cursor.close()
    alternate_benchmark = []
    for details in alt_bm_details:
        alt_bm = {"fund_code": details[0], "alt_bm_index": str(details[1]), "date": str(details[2])}
        alternate_benchmark.append(alt_bm)
    alternate_benchmark.pop(0)
    return alternate_benchmark


def get_prev_alt_bm_nav(fund_code, eff_end_date):
    alt_benchmark_nav_cursor = database.cursor()
    alt_previous_month_end_date = get_1m_date(eff_end_date)
    alt_benchmark_nav_query = "SELECT alt_benchmark_nav FROM fund_benchmark_nav where fund_code = '" + \
                              fund_code + "' and effective_end_date = '" + \
                              str(alt_previous_month_end_date) + "'"
    alt_benchmark_nav_cursor.execute(alt_benchmark_nav_query)
    prev_alt_benchmark_nav_details = alt_benchmark_nav_cursor.fetchall()
    print("eff_end_date", eff_end_date)
    print("prev_alt_benchmark_nav_details", prev_alt_benchmark_nav_details)
    alt_benchmark_previous_nav = prev_alt_benchmark_nav_details[0][0]
    alt_benchmark_nav_cursor.close()
    return alt_benchmark_previous_nav


def get_alt_bm_nav(fund_code, eff_end_date):
    alt_benchmark_nav_cursor = database.cursor()
    alt_benchmark_nav_query = "SELECT alt_benchmark_nav FROM fund_benchmark_nav where fund_code = '" + \
                              fund_code + "' and effective_end_date = '" + \
                              str(eff_end_date) + "'"
    alt_benchmark_nav_cursor.execute(alt_benchmark_nav_query)
    alt_benchmark_nav_details = alt_benchmark_nav_cursor.fetchall()
    print("alt_benchmark_nav_details", alt_benchmark_nav_details)
    alt_benchmark_nav = alt_benchmark_nav_details[0][0]
    alt_benchmark_nav_cursor.close()
    return alt_benchmark_nav


def get_alt_benchmark_performance(fund_code, alt_bm_index, eff_end_date):
    alt_benchmark_nav = get_alt_bm_nav(fund_code, eff_end_date)
    alt_benchmark_previous_nav = get_prev_alt_bm_nav(fund_code, eff_end_date)
    # alternate benchmark performance of 1 month
    alt_benchmark_perf_1m = round(((alt_benchmark_nav / alt_benchmark_previous_nav) - 1), 4)
    # alternate benchmark performance of 3 months
    alt_benchmark_3m_end_date = get_3m_date(eff_end_date)
    alt_benchmark_3m_cursor = database.cursor()
    alt_benchmark_3m_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_3m_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_bm_index + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_3m_cursor.execute(alt_benchmark_3m_query)
    alt_benchmark_3m = alt_benchmark_3m_cursor.fetchall()
    print("alt_benchmark_3m", alt_benchmark_3m)
    alt_benchmark_3m_cursor.close()
    if len(alt_benchmark_3m) == 0:
        alt_benchmark_perf_3m = None
    else:
        alt_benchmark_3m_final = alt_benchmark_3m[0][0]
        alt_benchmark_perf_3m = round(((alt_benchmark_nav / alt_benchmark_3m_final) - 1), 4)
    # alternate benchmark performance of 6 months
    alt_benchmark_6m_end_date = get_6m_date(eff_end_date)
    alt_benchmark_6m_cursor = database.cursor()
    alt_benchmark_6m_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_6m_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_bm_index + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_6m_cursor.execute(alt_benchmark_6m_query)
    alt_benchmark_6m = alt_benchmark_6m_cursor.fetchall()
    print("alt_benchmark_6m", alt_benchmark_6m)
    alt_benchmark_6m_cursor.close()
    if len(alt_benchmark_6m) == 0:
        alt_benchmark_perf_6m = None
    else:
        alt_benchmark_6m_final = alt_benchmark_6m[0][0]
        alt_benchmark_perf_6m = round(((alt_benchmark_nav / alt_benchmark_6m_final) - 1), 4)
    # alternate benchmark performance of 1 year
    effective_end_date = datetime.datetime.strptime(eff_end_date, "%Y-%m-%d").date()
    alt_benchmark_1y_end_date = get_1y_date(eff_end_date)
    alt_benchmark_1y_cursor = database.cursor()
    alt_benchmark_1y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_1y_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_bm_index + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_1y_cursor.execute(alt_benchmark_1y_query)
    alt_benchmark_1y = alt_benchmark_1y_cursor.fetchall()
    print("alt_benchmark_1y", alt_benchmark_1y)
    alt_benchmark_1y_cursor.close()
    if len(alt_benchmark_1y) == 0:
        alt_benchmark_perf_1y = None
    else:
        alt_benchmark_1y_final = alt_benchmark_1y[0][0]
        alt_benchmark_date_power_1y = effective_end_date - alt_benchmark_1y_end_date
        alt_benchmark_perf_1y = round((((alt_benchmark_nav / alt_benchmark_1y_final) **
                                        (365 / alt_benchmark_date_power_1y.days)) - 1), 4)
    # alternate benchmark performance of 2 years
    alt_benchmark_2y_end_date = get_2y_date(eff_end_date)
    alt_benchmark_2y_cursor = database.cursor()
    alt_benchmark_2y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_2y_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_bm_index + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_2y_cursor.execute(alt_benchmark_2y_query)
    alt_benchmark_2y = alt_benchmark_2y_cursor.fetchall()
    print("alt_benchmark_2y", alt_benchmark_2y)
    alt_benchmark_2y_cursor.close()
    if len(alt_benchmark_2y) == 0:
        alt_benchmark_perf_2y = None
    else:
        alt_benchmark_2y_final = alt_benchmark_2y[0][0]
        alt_benchmark_date_power_2y = effective_end_date - alt_benchmark_2y_end_date
        alt_benchmark_perf_2y = round((((alt_benchmark_nav / alt_benchmark_2y_final) **
                                        (365 / alt_benchmark_date_power_2y.days)) - 1), 4)
    # alternate benchmark performance of 3 years
    alt_benchmark_3y_end_date = get_3y_date(eff_end_date)
    alt_benchmark_3y_cursor = database.cursor()
    alt_benchmark_3y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_3y_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_bm_index + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_3y_cursor.execute(alt_benchmark_3y_query)
    alt_benchmark_3y = alt_benchmark_3y_cursor.fetchall()
    print("alt_benchmark_3y", alt_benchmark_3y)
    alt_benchmark_3y_cursor.close()
    if len(alt_benchmark_3y) == 0:
        alt_benchmark_perf_3y = None
    else:
        alt_benchmark_3y_final = alt_benchmark_3y[0][0]
        alt_benchmark_date_power_3y = effective_end_date - alt_benchmark_3y_end_date
        alt_benchmark_perf_3y = round((((alt_benchmark_nav / alt_benchmark_3y_final) **
                                        (365 / alt_benchmark_date_power_3y.days)) - 1), 4)
    # alternate benchmark performance of 5 years
    alt_benchmark_5y_end_date = get_5y_date(eff_end_date)
    alt_benchmark_5y_cursor = database.cursor()
    alt_benchmark_5y_query = "SELECT alt_benchmark_nav from fund_benchmark_nav where effective_end_date = '" + \
                             str(alt_benchmark_5y_end_date) + "' and alt_benchmark_index_code = '" + \
                             alt_bm_index + "' and fund_code = '" + fund_code + "' "
    alt_benchmark_5y_cursor.execute(alt_benchmark_5y_query)
    alt_benchmark_5y = alt_benchmark_5y_cursor.fetchall()
    print("alt_benchmark_5y", alt_benchmark_5y)
    alt_benchmark_5y_cursor.close()
    if len(alt_benchmark_5y) == 0:
        alt_benchmark_perf_5y = None
    else:
        alt_benchmark_5y_final = alt_benchmark_5y[0][0]
        alt_benchmark_date_power_5y = effective_end_date - alt_benchmark_5y_end_date
        alt_benchmark_perf_5y = round((((alt_benchmark_nav / alt_benchmark_5y_final) **
                                        (365 / alt_benchmark_date_power_5y.days)) - 1), 4)
    # alternate benchmark inception
    inception_date = get_inception_date()
    alt_benchmark_power_inception = effective_end_date - inception_date
    alt_benchmark_perf_inception = round((((alt_benchmark_nav / 1) ** (365 / alt_benchmark_power_inception.days)) - 1),
                                         4)
    update_cursor = database.cursor()
    update_query = "UPDATE fund_performance SET alt_benchmark_perf_1m = %s, alt_benchmark_perf_3m = %s, " \
                   "alt_benchmark_perf_6m = %s, alt_benchmark_perf_1y = %s, alt_benchmark_perf_2y = %s, " \
                   "alt_benchmark_perf_3y = %s, alt_benchmark_perf_5y = %s, alt_benchmark_perf_inception = %s " \
                   "where fund_code = '" + str(fund_code) + "' and effective_end_date = '" + str(eff_end_date) + "'"
    update_values = (alt_benchmark_perf_1m, alt_benchmark_perf_3m, alt_benchmark_perf_6m, alt_benchmark_perf_1y,
                     alt_benchmark_perf_2y, alt_benchmark_perf_3y, alt_benchmark_perf_5y, alt_benchmark_perf_inception)
    update_cursor.execute(update_query, update_values)
    print(fund_code, eff_end_date)
    return alt_benchmark_perf_1m, alt_benchmark_perf_3m, alt_benchmark_perf_6m, alt_benchmark_perf_1y, \
           alt_benchmark_perf_2y, alt_benchmark_perf_3y, alt_benchmark_perf_5y, alt_benchmark_perf_inception


try:
    db_host, db_user, db_pass, db_name = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', \
                                         'd0m#l1dZwhz!*9Iq0y1h', 'iq'
    # db_host, db_user, db_pass, db_name = env('DB_HOST'), env('DB_USER'), env('DB_PASS'), env('DB_NAME')
    database = MySQLdb.connect(db_host, db_user, db_pass, db_name, use_unicode=True, charset="utf8")
    fund_code_list = ["65609123", "83249718"]

    for fund_code in fund_code_list:
        print(fund_code)
        alt_bm_info = get_alt_benchmark_index(fund_code)
        print(fund_code)
        for alt_value in alt_bm_info:
            alt_bm_index = alt_value['alt_bm_index']
            eff_end_date = alt_value['date']
            nav_start_date = get_nav_start_date(fund_code, database)
            get_alt_benchmark_performance(fund_code, alt_bm_index, eff_end_date)
    database.commit()
    database.close()

except Exception as error:
    print("Exception raised :", error)
