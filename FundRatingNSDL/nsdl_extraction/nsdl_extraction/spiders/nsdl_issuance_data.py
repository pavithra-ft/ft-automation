import time
import scrapy
import datetime
from ..config.urls import *
from selenium import webdriver
from ..config.web_elements import *
from ..config.selenium_chrome import *
from ..items import NsdlIssuanceDataItem
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


class NsdlIssuance(scrapy.Spider):
    name = 'issuance_crawler'
    allowed_domains = [allowed_domains[0]]
    start_urls = [start_url[0]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response, **kwargs):
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
                        month = driver.find_element_by_xpath(mas_securities_month.format(mrows, mcols))
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
                    issuance_table = driver.find_element_by_xpath(issuance_table_path[0])
                    for i_index, i_row in enumerate(issuance_table.find_elements_by_xpath(issuance_table_row[0])):
                        td_issuance_data = []
                        if i_index > 2:
                            for t_cell in i_row.find_elements_by_xpath(issuance_table_cell[0]):
                                td_issuance_data.append(t_cell.text)
                                time.sleep(1)

                        if len(td_issuance_data) > 3:
                            issuance_items = NsdlIssuanceDataItem()
                            reporting_date = datetime.datetime.strptime(driver.find_element_by_xpath(
                                reporting_date_path[0]).get_attribute('value'), '%d-%b-%Y').date()
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

                except Exception as error:
                    print('Exception raised :', error)
                driver.close()
