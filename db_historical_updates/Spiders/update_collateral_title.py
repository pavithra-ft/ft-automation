import MySQLdb
from envparse import env

from Spiders.db_actions import get_fintuple_template_code, get_collateral_data, get_fund_short_code, \
    put_collateral_title

try:
    # db_host, db_user, db_pass = env('DB_HOST'), env('DB_USER'), env('DB_PASS')
    db_host, db_user, db_pass = 'ft-dev.cr3pgf2uoi18.ap-south-1.rds.amazonaws.com', 'wyzeup', 'd0m#l1dZwhz!*9Iq0y1h'
    iq_db, fs_db, app_db = 'iq', 'fs', 'app'

    iq_database = MySQLdb.connect(db_host, db_user, db_pass, iq_db)
    fs_database = MySQLdb.connect(db_host, db_user, db_pass, fs_db)
    app_database = MySQLdb.connect(db_host, db_user, db_pass, app_db)

    template_code_list = get_fintuple_template_code(fs_database)
    for template_code in template_code_list:
        collateral_data = get_collateral_data(template_code[0], fs_database)
        for collateral in collateral_data:
            fund_short_code = get_fund_short_code(collateral[1], app_database)
            collateral_title = fund_short_code + ' Fintuple Factsheet'
            put_collateral_title(collateral[1], collateral_title, collateral[2], fs_database)

    # Commit changes
    fs_database.commit()
    # Close database connection
    iq_database.close()
    fs_database.close()
    app_database.close()

except Exception as error:
    print("Exception raised :", error)
