import datetime as dt

today = dt.datetime.today().date()
offset = max(1, (today.weekday() + 6) % 7 - 3)
timedelta = dt.timedelta(offset)
recent_working_day = (today - timedelta).strftime("%d%m%y")

zip_file_dir = [r"C:\Users\pavithra\Documents\fintuple-automation-projects\BseBhavCopyNI\bhav_copy_ni\zip_files"]
csv_file_dir = [r"C:\Users\pavithra\Documents\fintuple-automation-projects\BseBhavCopyNI\bhav_copy_ni\csv_files"]

file_extensions = [".zip", ".csv"]

zip_file_name = ["nse_" + recent_working_day]
csv_file_name = ["bhav_copy_" + recent_working_day]

nse_bhav_copy_url = ["https://www.bseindia.com/download/BhavCopy/Equity/EQ_ISINCODE_"]
