from datetime import datetime as dt

YEAR = dt.today().year
BINARY_LOCATION = {'binary_location': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'}
CHROME_DRIVER_PATH = r'C:\Users\pavithra\Downloads\chromedriver_win32\chromedriver.exe'
EXTRACTED_DIR = r'C:\Users\pavithra\Documents\fintuple-automation-projects\BseBhavCopy\dailybhavcopy\dailybhavcopy' \
                r'\csv_files'
ZIP_DIR = r'C:\Users\pavithra\Documents\fintuple-automation-projects\BseBhavCopy\dailybhavcopy\dailybhavcopy\zip_files'
HEADLESS_OPTIONS = {'headless': '--headless',
                    'window_size': '--window-size=1920x1080'}
DOWNLOAD_PREFERENCES = {'download.default_directory': EXTRACTED_DIR,
                        'download.prompt_for_download': False}


def enable_download(driver, directory):
    """

    :param driver: Selenium web driver
    :param directory: Directory to store the file

    This function allows the Selenium web driver to store the file in the given directory.
    """
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow',
                         'downloadPath': directory}}
    driver.execute("send_command", params)
