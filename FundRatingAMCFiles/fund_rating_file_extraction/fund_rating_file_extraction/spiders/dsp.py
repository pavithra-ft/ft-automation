import glob
import os
import time
import zipfile
from selenium import webdriver


def download_file(amc, source_dir):
    main_url = 'https://www.advisorkhoj.com/mutual-funds-research/mutual-fund-portfolio/'
    chrome_options = webdriver.ChromeOptions()
    preferences = {"download.default_directory": source_dir,
                   "directory_upgrade": True,
                   "safebrowsing.enabled": True}
    # chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('prefs', preferences)
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=r'C:\Users\pavithra\Downloads\chromedriver_win32\chromedriver.exe')

    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': source_dir}}
    driver.execute("send_command", params)

    driver.get(main_url + amc + '/' + year)
    driver.find_element_by_xpath('//*[@id="wrapper"]/section[2]/div/div/div[2]/div[3]/div/div/div[2]/div/div/div/p[1]'
                                 '/a').click()
    time.sleep(15)


def rename_file(index, source_dir):
    files_path = source_dir + '/*.zip'
    latest_file = max(glob.iglob(files_path), key=os.path.getmtime)
    if os.path.isfile(source_dir + '/' + index.lower() + '.zip'):
        os.remove(source_dir + '/' + index.lower() + '.zip')
    os.rename(latest_file, source_dir + '/' + index.lower() + '.zip')


def extract_zip_files(index, source_dir, target_dir):
    filelist = []
    inner_dir = []
    with zipfile.ZipFile(source_dir + '/' + index.lower() + '.zip', 'r') as zipObj:
        listOfiles = zipObj.namelist()
        for elem in listOfiles:
            inner_dir.append(elem.split('/')[0])
            filelist.append(elem.split('/')[-1])
    filelist.pop(-1)
    for item in os.listdir(source_dir):
        if item == index.lower() + '.zip':
            file_path = os.path.join(source_dir, item)
            with zipfile.ZipFile(file_path) as zf:
                if len(filelist) > 1:
                    for target_file in filelist:
                        file_data = zf.read(inner_dir[0] + '/' + target_file)
                        target_name = item.split('.')[0] + '_' + target_file.split('.')[0].lower() + '.xlsx'
                        target_path = os.path.join(target_dir, target_name)
                        with open(target_path, "wb") as f:
                            f.write(file_data)
                else:
                    for target_file in filelist:
                        file_data = zf.read(inner_dir[0] + '/' + target_file)
                        target_name = item.split('.')[0] + '_' + target_file.split('.')[0].lower() + '.xlsx'
                        target_path = os.path.join(target_dir, target_name)
                        with open(target_path, "wb") as f:
                            f.write(file_data)


if __name__ == '__main__':
    source_dir = r'C:\Users\pavithra\Documents\fintuple-automation-projects\FundRatingAMCFiles' \
                 r'\fund_rating_file_extraction\fund_rating_file_extraction\zip_files'
    target_dir = r'C:\Users\pavithra\Documents\fintuple-automation-projects\FundRatingAMCFiles' \
                 r'\fund_rating_file_extraction\fund_rating_file_extraction\extracted_files'
    year = '2020'
    url_dict = {'DSP': 'DSP-Mutual-Fund'}
    for index, amc in url_dict.items():
        download_file(amc, source_dir)
        time.sleep(15)
        rename_file(index, source_dir)
        time.sleep(10)
        extract_zip_files(index, source_dir, target_dir)
