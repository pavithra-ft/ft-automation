import requests
import scrapy
from scrapy_splash import SplashRequest

from ..settings import BASE_DIR


class ValueResearchSpider(scrapy.Spider):
    name = "value_research"
    allowed_domains = ['https://www.valueresearchonline.com']
    start_url = "https://www.valueresearchonline.com/stocks/selector/indices/46/bse-500-index"

    def start_requests(self):
        urls = ["https://www.valueresearchonline.com/stocks/selector/indices/46/bse-500-index/?custom-cols=mcap%2Cpe"
                "%2Cpb%2Cdy%2Ceps"]
        for url in urls:
            yield SplashRequest(url=url, callback=self.security_ratios_parser, dont_filter=True)

    def security_ratios_parser(self, response):
        excel_url = response.css('div[class="col-sm-6 text-right"] a::attr(href)').get()
        print(excel_url)
        print(self.allowed_domains[0] + excel_url)
        self.save_pdf(self.allowed_domains[0] + excel_url)

    def save_pdf(self, url):
        data = requests.get(url)
        content = data.content
        filename = BASE_DIR + "/security_ratio_files/" + 'security_ratio.xlsx'
        with open(filename, 'wb') as f:
            f.write(content)
