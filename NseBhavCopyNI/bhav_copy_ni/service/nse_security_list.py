import re
import numpy as np
import pandas as pd
from bhav_copy_ni.database.db_queries import put_mas_securities_list, ni_on_session
from bhav_copy_ni.csv_extraction.file_extraction import get_bse_security_list


def get_security_list():
    df_read = pd.read_csv(
        r"C:\Users\pavithra\Documents\fintuple-automation-projects\NseBhavCopyNI\bhav_copy_ni\csv_files\eq_etfseclist.csv")
    df_str = df_read.astype(str)
    df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
    security_info = get_bse_security_list(df)
    return security_info


def put_security_list(security_info):
    try:
        put_mas_securities_list(security_info)
        ni_on_session.commit()
    except Exception as error:
        ni_on_session.rollback()
        print("Exception raised :", error)
    finally:
        ni_on_session.close()
