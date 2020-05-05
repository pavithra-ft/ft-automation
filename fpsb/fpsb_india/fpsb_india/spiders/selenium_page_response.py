import scrapy
from selenium import webdriver
from ..items import FpsbIndiaItem
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd


class ProductSpider(scrapy.Spider):
    name = "seleniumspider"
    allowed_domains = ['fpsb.co.in']
    start_urls = ['http://www.fpsb.co.in/scripts/CFPCertificantProfiles.aspx']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.driver = webdriver.Chrome(r'C:\Users\pavithra\Downloads\chromedriver_win32\chromedriver.exe')

    def parse(self, response):
        items = FpsbIndiaItem()
        self.driver.get(response.url)
        last_page_click = self.driver.find_element_by_xpath('//*[@id="DgCFPCertificant"]/tbody/tr[27]/td/font/b/a[10]')
        last_page_click.click()
        last_click = self.driver.find_element_by_xpath('//*[@id="DgCFPCertificant"]/tbody/tr[27]/td/font/b/a[11]')
        last_click.click()
        page_30 = self.driver.find_element_by_xpath('//*[@id="DgCFPCertificant"]/tbody/tr[27]/td/font/b/a[11]')
        page_30.click()
        page_40 = self.driver.find_element_by_xpath('//*[@id="DgCFPCertificant"]/tbody/tr[27]/td/font/b/a[11]')
        page_40.click()
        page_50 = self.driver.find_element_by_xpath('//*[@id="DgCFPCertificant"]/tbody/tr[27]/td/font/b/a[11]')
        page_50.click()
        next_page = self.driver.find_element_by_xpath('//*[@id="DgCFPCertificant"]/tbody/tr[27]/td/font/b/a[10]')
        next_page.click()
        no_of_views = len(self.driver.find_elements_by_link_text("View"))
        print("No of views in a page :", no_of_views)
        row = []
        page_view = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                     '20', '21', '22', '23', '24', '25', '26', '27']

        for page in page_view:
            id = "DgCFPCertificant__ctl{}_Linkbutton6".format(page)
            next = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, id)))
            next.click()
            try:
                items['name'] = self.driver.find_element_by_xpath('//*[@id="lblNamedb"]').text
                items['designation'] = self.driver.find_element_by_xpath('//*[@id="lblDesignationdb"]').text
                items['company'] = self.driver.find_element_by_xpath('//*[@id="lblCompanynamedb"]').text
                items['city'] = self.driver.find_element_by_xpath('//*[@id="lblcitydb"]').text
                items['address'] = self.driver.find_element_by_xpath('//*[@id="lblAddress"]').text
                items['address_city'] = self.driver.find_element_by_xpath('//*[@id="lblcityadd"]').text
                items['address_state'] = self.driver.find_element_by_xpath('//*[@id="lblstatedb"]').text
                items['address_pincode'] = self.driver.find_element_by_xpath('//*[@id="lblPincode"]').text
                # items['mobile'] = self.driver.find_element_by_xpath('//*[@id="lblMobile"]').text
                try:
                    mobile = self.driver.find_element_by_xpath('//*[@id="lblMobile"]')
                    items['mobile'] = mobile.text
                except:
                    items['mobile'] = ''
                items['resident_contact'] = self.driver.find_element_by_xpath('//*[@id="lblResidentContactNo"]').text
                items['business_contact'] = self.driver.find_element_by_xpath('//*[@id="lblBusinessContactNo"]').text
                # items['mailid1'] = self.driver.find_element_by_xpath('//*[@id="lblEmailid1"]').text
                try:
                    mailid1 = self.driver.find_element_by_xpath('//*[@id="lblEmailid1"]')
                    items['mailid1'] = mailid1.text
                except:
                    items['mailid1'] = ''
                # items['mailid2'] = self.driver.find_element_by_xpath('//*[@id="lblEmailid2"]').text
                try:
                    mailid2 = self.driver.find_element_by_xpath('//*[@id="lblEmailid2"]')
                    items['mailid2'] = mailid2.text
                except:
                    items['mailid2'] = ''
                items['employment_nature'] = self.driver.find_element_by_xpath('//*[@id="lblNatureofEmp"]').text
                items['fpsb_number'] = self.driver.find_element_by_xpath('//*[@id="lblFPSBNo"]').text
                # items['profile'] = self.driver.find_element_by_xpath('//*[@id="txtProfile"]/table/tbody/tr/td/div').text
                try:
                    profile = self.driver.find_element_by_xpath('//*[@id="txtProfile"]/table/tbody/tr/td/div')
                    items['profile'] = profile.text
                except:
                    items['profile'] = ''
                value = (items['name'], items['designation'], items['company'], items['city'], items['address'],
                         items['address_city'], items['address_state'], items['address_pincode'], items['mobile'],
                         items['resident_contact'], items['business_contact'], items['mailid1'], items['mailid2'],
                         items['employment_nature'], items['fpsb_number'], items['profile'])
                row.append(value)
                yield items
                self.driver.find_element_by_xpath('//*[@id="btnCancel"]').click()
            except Exception as err:
                print(err)
                break
        print(row)
        data = pd.DataFrame(row, columns=['name', 'designation', 'company', 'city', 'address', 'address_city',
                                          'address_state', 'address_pincode', 'mobile', 'resident_contact',
                                          'business_contact', 'mailid1', 'mailid2', 'employment_nature', 'fpsb_number',
                                          'profile'])
        data.to_csv('profile.csv', header=False, mode='a')
        self.driver.close()


