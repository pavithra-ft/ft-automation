import time
import scrapy
import datetime
from selenium import webdriver
from ..items import NsdlSecurityItem
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class NsdlTradeSecurity(scrapy.Spider):
    name = 'trade_security_crawler'
    allowed_domains = ['nsdl.co.in']
    start_urls = ['https://www.fpi.nsdl.co.in/web/Reports/traderepositoryreport.aspx']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.binary_locaion = '/usr/bin/google-chrome-stable'
        self.driver = webdriver.Chrome(r'C:\Users\pavithra\Downloads\chromedriver_win32\chromedriver.exe',
                                       chrome_options=self.options)

    def parse(self, response, **kwargs):
        self.driver.get(self.start_urls[0])
        calendar_rows = [1, 2, 3, 4, 5, 6]
        calendar_cols = [1, 2, 3, 4, 5, 6, 7]
        for row in calendar_rows:
            for col in calendar_cols:
                criteria = Select(self.driver.find_element_by_xpath('//*[@id="drp_EntityType"]'))
                criteria.select_by_value('For All')

                market = Select(self.driver.find_element_by_xpath('//*[@id="drp_view"]'))
                market.select_by_value('Secondary Market plus Primary Market')

                current_date = datetime.datetime.today().date() - relativedelta(months=1)
                month_in_words = datetime.date(current_date.year, current_date.month, current_date.day).strftime('%B')

                date_picker = self.driver.find_element_by_id('imgtxtFromDate')
                date_picker.click()
                time.sleep(0.5)

                month_year_title = self.driver.find_element_by_class_name('DynarchCalendar-title')
                month_year_title.click()
                time.sleep(0.5)

                year = self.driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div/div[3]/table/tbody/tr/td/'
                                                         'table[1]/tbody/tr[1]/td/input')
                year.clear()
                year.send_keys(current_date.year)
                time.sleep(0.5)

                month_rows = [1, 2, 3, 4]
                month_cols = [1, 2, 3]
                for mrows in month_rows:
                    for mcols in month_cols:
                        month = self.driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div/div['
                                                                  '3]/table/tbody/tr/td/table[2]/tbody/tr[{}]/td[{}]'.
                                                                  format(mrows, mcols))
                        if month.text == month_in_words[0:3]:
                            month.click()
                            time.sleep(2)

                date_locator = '/html/body/table/tbody/tr/td/div/div[2]/table/tbody/tr[{}]/td[{}]/' \
                               'div[@class="DynarchCalendar-day"]'.format(row, col)
                try:
                    day = self.driver.find_element_by_xpath(date_locator)
                    day.click()
                    time.sleep(1)

                    go_button = self.driver.find_element_by_xpath('//*[@id="btnSubmit"]')
                    go_button.click()
                    time.sleep(1)

                    table = self.driver.find_element_by_xpath('//*[@id="dvTradeData"]/table[1]/tbody')
                    for index, t_row in enumerate(table.find_elements_by_xpath('tr')):
                        td_data = []
                        if index > 2:
                            for t_cell in t_row.find_elements_by_xpath('td'):
                                td_data.append(t_cell.text)

                        if td_data:
                            security_items = NsdlSecurityItem()
                            security_items['security_isin'] = td_data[1]
                            security_items['security_name'] = td_data[2]
                            security_items['exchange_code'] = td_data[0]
                            security_items['security_type'] = 'CORPBOND'
                            security_items['security_code'] = None
                            security_items['bse_security_symbol'] = None
                            security_items['nse_security_symbol'] = None
                            security_items['mse_security_symbol'] = None
                            security_items['industry'] = None

                            yield security_items

                except NoSuchElementException:
                    pass
