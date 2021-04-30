import os
import glob
import time
import scrapy
import zipfile
from ..config.urls import *
from selenium import webdriver
from ..config.file_config import *
from ..config.web_elements import *
from ..config.selenium_chrome import *
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class BseDailyBhavCopy(scrapy.Spider):
    name = 'daily_bhav_copy_crawler'
    allowed_domains = [allowed_domains[0]]
    start_urls = [start_url[0]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = Options()
        self.options.add_experimental_option('prefs', DOWNLOAD_PREFERENCES)
        self.options.add_argument(HEADLESS_OPTIONS['headless'])
        self.options.add_argument(HEADLESS_OPTIONS['window_size'])
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=BINARY_LOCATION,
                                       chrome_options=self.options)

    def parse(self, response, **kwargs):
        enable_download(self.driver, ZIP_DIR)
        self.driver.get(self.start_urls[0])
        self.driver.find_element_by_xpath(download_url_path[0]).click()
        time.sleep(10)
        rename_file(ZIP_DIR)
        time.sleep(10)
        extract_zip_files(ZIP_DIR, EXTRACTED_DIR)


def rename_file(source_dir):
    files_path = source_dir + '/*' + zip_ext
    latest_file = max(glob.iglob(files_path), key=os.path.getmtime)
    if os.path.isfile(source_dir + '/' + zip_file_name[0] + zip_ext):
        os.remove(source_dir + '/' + zip_file_name[0] + zip_ext)
    os.rename(latest_file, source_dir + '/' + zip_file_name[0] + zip_ext)


def extract_zip_files(source_dir, target_dir):
    file_list = []
    with zipfile.ZipFile(source_dir + '/' + zip_file_name[0] + zip_ext, 'r') as zipObj:
        list_of_files = zipObj.namelist()
        for elem in list_of_files:
            file_list.append(elem.split('/')[-1])

    for item in os.listdir(source_dir):
        if item.endswith(zip_ext):
            file_path = os.path.join(source_dir, item)
            with zipfile.ZipFile(file_path) as zf:
                for target_file in file_list:
                    if target_file in zf.namelist():
                        target_name = csv_file_name[0] + csv_ext
                        target_path = os.path.join(target_dir, target_name)
                        with open(target_path, "wb") as f:
                            f.write(zf.read(target_file))
