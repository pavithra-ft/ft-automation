import os
import time
from selenium import webdriver


def download_file(amc, directory):
    chrome_options = webdriver.ChromeOptions()
    preferences = {"download.default_directory": directory,
                   "directory_upgrade": True,
                   "safebrowsing.enabled": True}
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=r'C:\Users\pavithra\Downloads\chromedriver_win32\chromedriver.exe')

    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': directory}}
    driver.execute("send_command", params)

    driver.get(amc)
    driver.find_element_by_xpath('//*[@id="select-data"]/div/ul/li/div/button/i').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="MonthlyPortfolioDisclosure"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="MonthlyPortfolioDisclosure10"]/div/ul/li[1]').click()
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
    url_dict = {'FRANKLIN': 'https://www.franklintempletonindia.com/investor/reports'}
    for index, amc in url_dict.items():
        download_file(amc, directory)
        rename_file(index, directory)
