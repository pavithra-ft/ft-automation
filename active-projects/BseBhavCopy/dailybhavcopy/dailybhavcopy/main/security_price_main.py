from dailybhavcopy.dailybhavcopy.service.bse_security_price import *

if __name__ == "__main__":
    security_info = get_mas_securities_info()
    put_securities_fw(security_info)
    put_securities_ac(security_info)
    remove_downloaded_files()
