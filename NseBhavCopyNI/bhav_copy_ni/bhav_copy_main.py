from bhav_copy_ni.config.bhav_copy_config import nse_bhav_copy_url
from bhav_copy_ni.service.nse_security_price import remove_downloaded_files
from bhav_copy_ni.service.download_daily_bhav_copy import download_file, extract_zip_files

if __name__ == "__main__":
    remove_downloaded_files()
    zip_filename = download_file(nse_bhav_copy_url[0])
    extract_zip_files(zip_filename)
