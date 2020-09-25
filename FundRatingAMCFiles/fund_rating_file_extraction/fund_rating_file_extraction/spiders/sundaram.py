import scrapy
import requests
from ..config.urls import *
from ..config.file_extensions import *
from ..config.amc_dictionary import sundaram_dict
from ..config.web_elements import sundaram_path
from ..config.selenium_chrome import EXTRACTED_DIR, YEAR


class SundaramAdvisorKhoj(scrapy.Spider):
    name = "sundaram_crawler"
    allowed_domains = [allowed_domains[0]]
    start_url = [start_url[0]]

    def start_requests(self):
        """
        This function loops through all the AMC's in the given dictionary with the Query parameters of the URL.
        With the built up URL, the Scrapy Request will be sent.
        """
        for amc_key, amc_value in sundaram_dict.items():
            url = self.start_url[0] + amc_value + "/" + str(YEAR)
            yield scrapy.Request(url=url, callback=self.parser, meta={'amc_key': amc_key})

    def parser(self, response):
        """
        This function gets the Response from the given URL and passes the response to the specific download formats.

        :param response: Response received from the URL.
        """
        link = {}
        link.update({response.meta.get('amc_key'): response.css(sundaram_path[0]).getall()[0]})

        for amc, url_value in link.items():
            download_format = url_value.split('/')[-1].split('.')[1]
            if download_format == xlsb_format or download_format == xls_format or download_format == xlsx_format:
                save_xlsx(amc, url_value)


def save_xlsx(amc, url):
    """
    This function saves the downloaded XLSX files.

    :param amc: Name of the AMC
    :param url: URL of the AMC
    """
    data = requests.get(url)
    content = data.content
    filename = EXTRACTED_DIR + '/' + amc.lower() + xlsx_ext
    with open(filename, 'wb') as f:
        f.write(content)
