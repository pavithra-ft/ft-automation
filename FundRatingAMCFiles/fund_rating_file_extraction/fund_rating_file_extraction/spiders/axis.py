import os
import time
from selenium import webdriver


def download_file(amc, directory):
    main_url = 'https://www.advisorkhoj.com/mutual-funds-research/mutual-fund-portfolio/'
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': directory}
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=r'C:\Users\pavithra\Downloads\chromedriver_win32\chromedriver.exe')

    driver.get(main_url + amc + '/' + year)
    search_input = driver.find_element_by_xpath('//*[@id="wrapper"]/section[2]/div/div/div[2]/div[3]/div/div/div[2]/div'
                                                '/div/div/p[1]/a')
    search_input.click()
    time.sleep(10)


def rename_file(index, directory):
    os.chdir(directory)
    latest_file = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    filename = directory + '/' + index.lower() + '.xlsx'
    os.rename(latest_file[-1], filename)


if __name__ == '__main__':
    directory = r'C:\Users\pavithra\Documents\fintuple-automation-projects\FundRatingAMCFiles' \
                r'\fund_rating_file_extraction\fund_rating_file_extraction\extracted_files'
    year = '2020'
    url_dict = {'AXIS': 'Axis-Mutual-Fund'}
    for index, amc in url_dict.items():
        download_file(amc, directory)
        rename_file(index, directory)
