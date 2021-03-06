"""
This file holds the Selenium settings and Options for Headless Selenium Chrome browser.
"""

CHROME_DRIVER_PATH = r'C:\Users\pavithra\automation_software\FundRating\chromedriver_win32\chromedriver.exe'

HEADLESS_OPTIONS = {'headless': '--headless',
                    'window_size': '--window-size=1920x1080',
                    'sandbox': '--no-sandbox',
                    'dev_shm_usage': '--disable-dev-shm-usage',
                    'disable_gpu': '--disable-gpu',
                    'network_service': '--disable-features=NetworkService',
                    'display_compositor': '--disable-features=VizDisplayCompositor'}
