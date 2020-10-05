import time
import scrapy
import datetime
from ..config.urls import *
from selenium import webdriver
from ..config.web_elements import *
from ..items import NsdlSecurityItem
from ..config.selenium_chrome import *
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


class NsdlTradeSecurity(scrapy.Spider):
    name = 'trade_security_crawler'
    allowed_domains = [allowed_domains[0]]
    start_urls = [start_url[0]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response, **kwargs):
        """
        This function will parse through all the dates in the current month and extracts the Security ISIN and
        Security name from the NSDL website.

        Extracted data will go through a condition, if ISIN already present in MAS_SECURITIES table, it will drop off
        that particular data and if it doesn't exist in MAS_SECURITIES then it will push the data into the table.
        (This process is taken care by the Pipelines.py)

        :param response: Response from the URL
        :param kwargs: Keyword arguments
        """
        calendar_rows = [1, 2, 3, 4, 5, 6]
        calendar_cols = [1, 2, 3, 4, 5, 6, 7]
        for row in calendar_rows:
            for col in calendar_cols:
                options = Options()
                options.add_argument(HEADLESS_OPTIONS['headless'])
                options.add_argument(HEADLESS_OPTIONS['window_size'])
                options.add_argument(HEADLESS_OPTIONS['sandbox'])
                options.add_argument(HEADLESS_OPTIONS['dev_shm_usage'])
                options.add_argument(HEADLESS_OPTIONS['disable_gpu'])
                options.add_argument(HEADLESS_OPTIONS['network_service'])
                options.add_argument(HEADLESS_OPTIONS['display_compositor'])
                driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)

                driver.get(self.start_urls[0])
                criteria = Select(driver.find_element_by_xpath(criteria_path[0]))
                criteria.select_by_value(criteria_value[0])

                market = Select(driver.find_element_by_xpath(market_path[0]))
                market.select_by_value(market_value[0])

                current_date = datetime.datetime.today().date() - relativedelta(months=1)
                month_in_words = datetime.date(current_date.year, current_date.month, current_date.day).strftime('%B')

                date_picker = driver.find_element_by_id(date_picker_path[0])
                date_picker.click()
                time.sleep(1)

                month_year_title = driver.find_element_by_class_name(date_picker_mon_yr[0])
                month_year_title.click()
                time.sleep(1)

                year = driver.find_element_by_xpath(date_picker_year[0])
                year.clear()
                year.send_keys(current_date.year)
                time.sleep(1)

                month_rows = [1, 2, 3, 4]
                month_cols = [1, 2, 3]
                for mrows in month_rows:
                    for mcols in month_cols:
                        month = driver.find_element_by_xpath(mas_securities_month[0].format(mrows, mcols))
                        if month.text == month_in_words[0:3]:
                            month.click()
                            time.sleep(1)

                day = driver.find_element_by_xpath(date_locator_path[0].format(row, col))
                day.click()
                time.sleep(1)

                go_button = driver.find_element_by_xpath(go_button_path[0])
                go_button.click()
                time.sleep(3)

                try:
                    trade_table = driver.find_element_by_xpath(trade_table_path[0])
                    time.sleep(1)
                    for index, t_row in enumerate(trade_table.find_elements_by_xpath(trade_table_row[0])):
                        td_trade_data = []
                        if index > 2:
                            for t_cell in t_row.find_elements_by_xpath(trade_table_cell[0]):
                                td_trade_data.append(t_cell.text)

                        if td_trade_data:
                            security_items = NsdlSecurityItem()
                            security_items['security_isin'] = td_trade_data[1]
                            security_items['security_name'] = td_trade_data[2]
                            security_items['exchange_code'] = td_trade_data[0]
                            security_items['security_type'] = 'CORPBOND'
                            security_items['security_code'] = None
                            security_items['bse_security_symbol'] = None
                            security_items['nse_security_symbol'] = None
                            security_items['mse_security_symbol'] = None
                            security_items['industry'] = None
                            yield security_items
                except Exception as error:
                    print('Exception raised :', error)
                driver.close()
