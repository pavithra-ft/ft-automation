import os
import re
import numpy as np
import pandas as pd
from bhav_copy_ac.database.db_queries import put_mas_securities_price, ac_on_session
from bhav_copy_ac.csv_extraction.file_extraction import get_security_info
from bhav_copy_ac.config.bhav_copy_config import *


def get_mas_securities_info():
    df_read = pd.read_csv(csv_file_dir[0] + "/" + csv_file_name[0] + file_extensions[1])
    df_str = df_read.astype(str)
    df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
    security_info = get_security_info(df)
    return security_info


def put_securities(security_info):
    try:
        put_mas_securities_price(security_info)
        ac_on_session.commit()
    except Exception as error:
        ac_on_session.rollback()
        print("Exception raised :", error)
    finally:
        ac_on_session.close()


def remove_downloaded_files():
    if os.path.exists(csv_file_dir[0] + "/" + csv_file_name[0] + file_extensions[1]):
        os.remove(csv_file_dir[0] + "/" + csv_file_name[0] + file_extensions[1])
    if os.path.exists(zip_file_dir[0] + "/" + zip_file_name[0] + file_extensions[0]):
        os.remove(zip_file_dir[0] + "/" + zip_file_name[0] + file_extensions[0])
