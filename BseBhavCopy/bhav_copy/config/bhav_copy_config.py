import datetime as dt

zip_file_dir = [r"C:\Users\pavithra\Documents\fintuple-automation-projects\BseBhavCopy\bhav_copy\zip_files"]
csv_file_dir = [r"C:\Users\pavithra\Documents\fintuple-automation-projects\BseBhavCopy\bhav_copy\csv_files"]

file_extensions = [".zip", ".csv"]

zip_file_name = ["bse_" + str(dt.datetime.now().date())]
csv_file_name = ["bhav_copy_" + str(dt.datetime.now().date())]

bse_bhav_copy_url = ["https://www.bseindia.com/download/BhavCopy/Equity/EQ_ISINCODE_110221.zip"]
