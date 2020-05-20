import MySQLdb

from glob import glob
from calendar import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

from services.db_actions import get_mas_indices
from services.index_performance import index_performance

try:
    iq_db, fs_db, app_db = 'iq', 'fs', 'app'
    # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', 'd0m#l1dZwhz!*9Iq0y1h'
    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db, use_unicode=True, charset="utf8")
    fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db, use_unicode=True, charset="utf8")
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db, use_unicode=True, charset="utf8")
    pdf_files = [file for file in glob(r"C:\Users\pavithra\Documents\fintuple-automation-projects\RatioExtraction"
                                       r"\ratio_extraction\ratio_extraction\pdf_files\*.pdf")]
    mas_indices = get_mas_indices(iq_database)
    del_indices = ['BSE30', 'NIFVIX']
    mas_indices = [index for index in mas_indices if index not in del_indices]
    date = datetime.today().date() - relativedelta(months=1)
    reporting_date = date.replace(day=calendar.monthrange(date.year, date.month)[1])
    for index_code in mas_indices:
        index_performance(index_code, reporting_date, pdf_files, iq_database)
        print(reporting_date, ": Index code - ", index_code, "Index updated successfully")
    # Database commit
    iq_database.commit()
    iq_database.close()
    fs_database.close()
    app_database.close()

except Exception as error:
    print("Exception raised :", error)
