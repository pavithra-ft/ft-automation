import datetime as dt

today = dt.datetime.today().date()
offset = max(1, (today.weekday() + 6) % 7 - 3)
timedelta = dt.timedelta(offset)
date_available = (today - timedelta)
recent_working_day = date_available.strftime("%d%m%y")

zip_ext, csv_ext = ".zip", ".csv"
zip_file_name = ["bse_bhav_copy" + "_" + str(recent_working_day)]
csv_file_name = ["bhav_copy" + "_" + str(recent_working_day)]
