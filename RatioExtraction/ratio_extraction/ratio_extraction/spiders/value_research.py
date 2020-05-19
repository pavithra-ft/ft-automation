import scrapy
from scrapy_splash import SplashRequest

from ..items import SecurityRatios


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
        table = response.css('div[class="dataTables_scroll"] div[class="dataTables_scrollBody"] table['
                             'class="vro-table row-border dataTable no-footer"]')[0]
        for index, row in enumerate(table.css('tbody > tr')):
            if index >= 0:
                items = SecurityRatios()
                items['security_name'] = row.css('td a::text').extract_first()
                items['market_cap'] = row.css('td:nth-child(3)::text').extract_first()
                items['price_to_earnings'] = row.css('td:nth-child(4)::text').extract_first()
                items['price_to_book'] = row.css('td:nth-child(5)::text').extract_first()
                items['dividend_yield'] = row.css('td:nth-child(6)::text').extract_first()
                items['earning_per_share'] = row.css('td:nth-child(7)::text').extract_first()
                yield items

        # pages_count = response.xpath('//*[@id="DataTables_Table_0_paginate"]/span/a/text()').get()
        # if pages_count:
        #     next_page = response.xpath('//*[@id="DataTables_Table_0_next"]').get()
        #     # pages_count = response.xpath('//*[@id="DataTables_Table_0_paginate"]/span/a/text()').get()
