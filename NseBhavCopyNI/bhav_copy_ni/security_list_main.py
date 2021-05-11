from bhav_copy_ni.service.nse_security_list import get_security_list, put_security_list

if __name__ == "__main__":
    security_info = get_security_list()
    put_security_list(security_info)
