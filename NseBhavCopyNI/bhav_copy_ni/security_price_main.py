from bhav_copy_ni.service.nse_security_price import *

if __name__ == "__main__":
    security_info = get_mas_securities_info()
    put_securities(security_info)
    remove_downloaded_files()
