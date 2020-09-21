import os
import time
import scrapy
from ..config.urls import *
from selenium import webdriver
from ..config.selenium_chrome import *
from ..config.file_extensions import xlsx_ext
from ..config.amc_dictionary import franklin_dict
from selenium.webdriver.chrome.options import Options
from ..config.web_elements import franklin_dropdown, franklin_select, franklin_link


class FranklinAdvisorKhoj(scrapy.Spider):
    name = 'franklin_crawler'
    allowed_domains = [allowed_domains[0]]
    start_urls = [start_url[0]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = Options()
        self.options.add_experimental_option('prefs', DOWNLOAD_PREFERENCES)
        self.options.add_argument(HEADLESS_OPTIONS['headless'])
        self.options.add_argument(HEADLESS_OPTIONS['window_size'])
        self.driver = webdriver.Chrome(desired_capabilities=BINARY_LOCATION, chrome_options=self.options,
                                       executable_path=CHROME_DRIVER_PATH)

    def parse(self, response, **kwargs):
        for index, amc in franklin_dict.items():
            enable_download(self.driver, EXTRACTED_DIR)
            self.driver.get(amc)
            self.driver.find_element_by_xpath(franklin_dropdown[0]).click()
            time.sleep(1)
            self.driver.find_element_by_xpath(franklin_select[0]).click()
            time.sleep(1)
            self.driver.find_element_by_xpath(franklin_link[0]).click()
            time.sleep(10)
            rename_file(index, EXTRACTED_DIR)


def rename_file(index, directory):
    os.chdir(directory)
    latest_file = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    filename = directory + '/' + index.lower() + xlsx_ext
    os.rename(latest_file[-1], filename)
