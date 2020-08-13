import time
import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ..items import ItimfItem


class ItiMf(scrapy.Spider):
    name = 'iti_mf_crawler'
    allowed_domains = ['itimf.com']
    start_urls = ['https://www.itimf.com/locate_advisor/west']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome(r'C:\Users\pavithra\Downloads\chromedriver_win32\chromedriver.exe')

    def parse(self, response, **kwargs):
        self.driver.get(self.start_urls[0])
        north_states = ["Haryana", "New Delhi", "Rajasthan", "Uttar Pradesh"]
        south_states = ["Andhra Pradesh", "Karnataka", "Kerala", "Tamil Nadu", "Telangana"]
        east_states = ["Bihar", "West Bengal"]
        west_states = ["Gujarat", "Madhya Pradesh", "Maharashtra"]
        for state in west_states:
            next_state = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.LINK_TEXT, state)))
            next_state.click()
            time.sleep(5)
            state_name = self.driver.find_element_by_xpath(
                '//*[@id="ContentPlaceHolder1_updpannel"]/div/div[2]/div/h2').text

            for agent in range(1, 900):
                try:
                    agent_details = self.driver.find_element_by_xpath(
                        '//*[@id="ContentPlaceHolder1_updpannel"]/div/div[2]/div/div[2]/div[{}]/p'.format(agent)).text
                    agent_data = agent_details.split('\n')
                    items = ItimfItem()
                    items['region'] = self.start_urls[0].split('/')[-1].capitalize()
                    items['state'] = state_name
                    items['agent_no'] = agent_data[0].replace('Agent No :', '')
                    items['agent_name'] = agent_data[1].replace('Agent Name :', '')
                    items['city'] = agent_data[2].replace('City :', '')
                    items['pin_code'] = agent_data[3].replace('Pin Code :', '')
                    items['mobile_no'] = agent_data[4].replace('Mobile No :', '')
                    items['email'] = agent_data[5].replace('Email :', '')
                    yield items

                except Exception as error:
                    print('-----------------------Reached end of the page------------------------',  error)
