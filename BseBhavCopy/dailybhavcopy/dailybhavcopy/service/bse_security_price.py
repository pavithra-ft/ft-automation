import os
import re
import numpy as np
import pandas as pd
from dailybhavcopy.dailybhavcopy.database.onboarding_ac_dev.db_queries import put_mas_securities_price as ms_ac, ac_on_session
from dailybhavcopy.dailybhavcopy.database.onboarding_fw_dev.db_queries import put_mas_securities_price as ms_fw, fw_on_session
from dailybhavcopy.dailybhavcopy.csv_extraction.file_extraction import get_security_info
from dailybhavcopy.dailybhavcopy.config.selenium_chrome import *
from dailybhavcopy.dailybhavcopy.config.file_config import *


def get_mas_securities_info():
    df_read = pd.read_csv(EXTRACTED_DIR + "/" + csv_file_name[0] + csv_ext)
    df_str = df_read.astype(str)
    df = df_str.applymap(lambda x: re.sub(r'^-$', str(np.NaN), x)).where(pd.notnull(df_read), None)
    security_info = get_security_info(df)
    return security_info


def put_securities_fw(security_info):
    try:
        ms_fw(security_info)
        fw_on_session.commit()
    except Exception as error:
        fw_on_session.rollback()
        print("Exception raised :", error)
    finally:
        fw_on_session.close()


def put_securities_ac(security_info):
    try:
        ms_ac(security_info)
        ac_on_session.commit()
    except Exception as error:
        ac_on_session.rollback()
        print("Exception raised :", error)
    finally:
        ac_on_session.close()


def remove_downloaded_files():
    if os.path.exists(EXTRACTED_DIR + "/" + csv_file_name[0] + csv_ext):
        os.remove(EXTRACTED_DIR + "/" + csv_file_name[0] + csv_ext)
    if os.path.exists(ZIP_DIR + "/" + zip_file_name[0] + zip_ext):
        os.remove(ZIP_DIR + "/" + zip_file_name[0] + zip_ext)
