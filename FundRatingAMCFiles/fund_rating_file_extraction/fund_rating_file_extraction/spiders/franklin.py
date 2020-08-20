import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select


def download_file(amc, directory):
    # main_url = 'https://www.advisorkhoj.com/mutual-funds-research/mutual-fund-portfolio/'
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': directory}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'C:\Users\pavithra\Downloads'
                                                                             r'\chromedriver_win32\chromedriver.exe')

    # driver.get(main_url + amc + '/' + year)
    driver.get(amc)
    selectOption = Select(driver.find_element_by_class_name("btn btn-default dropdown-toggle"))
    selectOption.select_by_visible_text("Monthly Portfolio Disclosure")


def rename_file(index, directory):
    os.chdir(directory)
    latest_file = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    filename = directory + '/' + index.lower() + '.xlsx'
    os.rename(latest_file[-1], filename)


if __name__ == '__main__':
    directory = r'C:\Users\pavithra\Documents\fintuple-automation-projects\AMC_Excel\amc_files_extraction' \
                r'\amc_files_extraction\extracted_data'
    year = '2020'
    url_dict = {'FRANKLIN': 'https://www.franklintempletonindia.com/investor/reports'}
    for index, amc in url_dict.items():
        download_file(amc, directory)
        # time.sleep(20)
        # rename_file(index, directory)
