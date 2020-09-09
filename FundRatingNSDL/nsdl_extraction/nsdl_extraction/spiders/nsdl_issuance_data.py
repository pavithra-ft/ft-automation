import time
import scrapy
import datetime
from selenium import webdriver
from ..items import NsdlIssuanceDataItem
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class NsdlIssuance(scrapy.Spider):
    name = 'issuance_crawler'
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

                    issuance_table = self.driver.find_element_by_xpath('//*[@id="dvTradeData"]/table[2]/tbody')
                    for i_index, i_row in enumerate(issuance_table.find_elements_by_xpath('tr')):
                        td_issuance_data = []
                        if i_index > 2:
                            for t_cell in i_row.find_elements_by_xpath('td'):
                                td_issuance_data.append(t_cell.text)

                        if len(td_issuance_data) > 3:
                            print('####################' + self.driver.find_element_by_xpath(
                                '//*[@id="hdnFromDate"]').get_attribute('value'))

                            issuance_items = NsdlIssuanceDataItem()
                            reporting_date = datetime.datetime.strptime(self.driver.find_element_by_xpath(
                                '//*[@id="hdnFromDate"]').get_attribute('value'), '%d-%b-%Y').date()
                            issuance_items['reporting_date'] = datetime.date.strftime(reporting_date, '%Y-%m-%d')
                            issuance_items['security_isin'] = td_issuance_data[0]

                            if ',' in td_issuance_data[2]:
                                issuance_items['issue_size'] = float(td_issuance_data[2].replace(',', '')) * 10000000
                            else:
                                issuance_items['issue_size'] = float(td_issuance_data[2]) * 10000000

                            issuance_items['issue_price'] = float(td_issuance_data[3].replace(',', ''))

                            issue_allotment_date = datetime.datetime.strptime(td_issuance_data[4], '%d/%m/%Y').date()
                            issuance_items['issue_allotment_date'] = datetime.date.strftime(issue_allotment_date,
                                                                                            '%Y-%m-%d')

                            issuance_items['interest_payment_frequency'] = td_issuance_data[5]

                            if td_issuance_data[6] != '':
                                first_interest_payment_date = datetime.datetime.strptime(td_issuance_data[6],
                                                                                         '%d-%b-%Y').date()
                                issuance_items['first_interest_payment_date'] = datetime.date.strftime(
                                    first_interest_payment_date, '%Y-%m-%d')
                            else:
                                issuance_items['first_interest_payment_date'] = None

                            maturity_date = datetime.datetime.strptime(td_issuance_data[7], '%d-%b-%Y').date()
                            issuance_items['maturity_date'] = datetime.date.strftime(maturity_date, '%Y-%m-%d')

                            issuance_items['put_option_description'] = td_issuance_data[8]
                            issuance_items['call_option_description'] = td_issuance_data[9]
                            issuance_items['credit_rating_agency'] = td_issuance_data[10]
                            issuance_items['credit_rating'] = td_issuance_data[11]

                            if td_issuance_data[12] != '':
                                date_of_rating = datetime.datetime.strptime(td_issuance_data[12], '%d/%m/%Y').date()
                                issuance_items['date_of_rating'] = datetime.date.strftime(date_of_rating, '%Y-%m-%d')
                            else:
                                issuance_items['date_of_rating'] = None

                            yield issuance_items

                except NoSuchElementException:
                    pass
