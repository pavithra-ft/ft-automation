from bhav_copy.config.bhav_copy_config import bse_bhav_copy_url
from bhav_copy.service.download_daily_bhav_copy import download_file, extract_zip_files

if __name__ == "__main__":
    zip_filename = download_file(bse_bhav_copy_url[0])
    extract_zip_files(zip_filename)
