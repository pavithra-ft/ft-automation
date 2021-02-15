from bhav_copy.config.bhav_copy_config import bse_bhav_copy_url
from bhav_copy.service.bse_security_price import remove_downloaded_files
from bhav_copy.service.download_daily_bhav_copy import get_recent_working_day, download_file, extract_zip_files

if __name__ == "__main__":
    remove_downloaded_files()
    download_url = get_recent_working_day(bse_bhav_copy_url[0])
    zip_filename = download_file(download_url)
    extract_zip_files(zip_filename)
