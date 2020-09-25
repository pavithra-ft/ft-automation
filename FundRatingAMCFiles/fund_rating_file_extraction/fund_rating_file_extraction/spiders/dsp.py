import os
import glob
import time
import scrapy
import zipfile
from ..config.urls import *
from selenium import webdriver
from ..config.selenium_chrome import *
from ..config.web_elements import dsp_path
from ..config.amc_dictionary import dsp_dict
from selenium.webdriver.chrome.options import Options
from ..config.file_extensions import zip_ext, xlsx_ext


class DspAdvisorKhoj(scrapy.Spider):
    name = 'dsp_crawler'
    allowed_domains = [allowed_domains[0]]
    start_urls = [start_url[0]]

    def __init__(self, **kwargs):
        """
        This constructor sets up the required settings for the Headless Selenium Chrome browser.

        :param kwargs: Keyword arguments
        """
        super().__init__(**kwargs)
        self.options = Options()
        self.options.add_experimental_option('prefs', DOWNLOAD_PREFERENCES)
        self.options.add_argument(HEADLESS_OPTIONS['headless'])
        self.options.add_argument(HEADLESS_OPTIONS['window_size'])
        self.driver = webdriver.Chrome(desired_capabilities=BINARY_LOCATION, chrome_options=self.options,
                                       executable_path=CHROME_DRIVER_PATH)

    def parse(self, response, **kwargs):
        """
        This function will loop through the Dictionary and gets the Response from the URL.

        :param response: Response of the URL
        :param kwargs: Keyword arguments
        """
        for index, amc in dsp_dict.items():
            enable_download(self.driver, ZIP_DIR)
            self.driver.get(self.start_urls[0] + amc + '/' + str(YEAR))
            self.driver.find_element_by_xpath(dsp_path[0]).click()
            time.sleep(5)
            rename_file(index, ZIP_DIR)
            time.sleep(10)
            extract_zip_files(index, ZIP_DIR, EXTRACTED_DIR)


def rename_file(index, source_dir):
    """
    This function renames the downloaded zip file with AMC name.

    :param index: Name of the AMC
    :param source_dir: Directory where the file is downloaded and stored
    """
    files_path = source_dir + '/*' + zip_ext
    latest_file = max(glob.iglob(files_path), key=os.path.getmtime)
    if os.path.isfile(source_dir + '/' + index.lower() + zip_ext):
        os.remove(source_dir + '/' + index.lower() + zip_ext)
    os.rename(latest_file, source_dir + '/' + index.lower() + zip_ext)


def extract_zip_files(index, source_dir, target_dir):
    """
    This function will extract the files inside the downloaded Zip file and stores it in the Target Directory.

    :param index: Name of the AMC
    :param source_dir: Directory where the file is downloaded and stored
    :param target_dir: Directory to store the file after extracting it from the Zip file
    """
    filelist = []
    inner_dir = []
    with zipfile.ZipFile(source_dir + '/' + index.lower() + zip_ext, 'r') as zipObj:
        listOfiles = zipObj.namelist()
        for elem in listOfiles:
            inner_dir.append(elem.split('/')[0])
            filelist.append(elem.split('/')[-1])
    filelist.pop(-1)
    for item in os.listdir(source_dir):
        if item == index.lower() + zip_ext:
            file_path = os.path.join(source_dir, item)
            with zipfile.ZipFile(file_path) as zf:
                for target_file in filelist:
                    if 'Open' in target_file:
                        file_data = zf.read(inner_dir[0] + '/' + target_file)
                        target_name = item.split('.')[0] + '_' + target_file.split('.')[0].lower() + xlsx_ext
                        target_path = os.path.join(target_dir, target_name)
                        with open(target_path, "wb") as f:
                            f.write(file_data)
