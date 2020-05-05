import scrapy
from ..items import DiscParticularsItem, NonDiscParticularsItem


class ParticularsSpider(scrapy.Spider):
    name = "particulars"
    allowed_domains = ['https://www.sebi.gov.in']
    formURL = "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes"

    def start_requests(self):
        urls = ["https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for year in range(2013, 2021):
            for month in range(1, 13):
                data = {'pmrId': "1000171371@@INP000004243@@BANYAN CAPITAL ADVISORS PRIVATE LIMITED",
                        'year': str(year),
                        'month': str(month)
                        }
                yield scrapy.FormRequest(self.formURL, formdata=data, callback=self.item_parser, dont_filter=True,
                                         cb_kwargs={"month": month, "year": year})

    def item_parser(self, response, month, year):
        particulars_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
                                         'table-striped table-bordered table-hover background '
                                         'statistics-table"]')
        if particulars_table:
            particulars_table = particulars_table[1]
            for row in particulars_table.css('tbody > tr'):
                p_item = DiscParticularsItem()
                p_item['gross_sale'] = row.css('td:nth-child(1)::text').extract_first()
                p_item['gross_purchase'] = row.css('td:nth-child(2)::text').extract_first()
                p_item['pf_turnover_ratio'] = row.css('td:nth-child(3)::text').extract_first()
                p_item['performance_of_pf'] = row.css('td:nth-child(4)::text').extract_first()
                p_item['value_of_assets'] = row.css('td:nth-child(5)::text').extract_first()
                p_item['month'] = month
                p_item['code'] = "DISC"
                p_item['year'] = year
                amc_name = response.css('div[class="org-strong"] strong::text').get()
                p_item['amc_name'] = amc_name[27:]
                yield p_item

        part_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
                                  'table-striped table-bordered table-hover background '
                                  'statistics-table"]')
        if part_table:
            part_table = part_table[3]
            for row in part_table.css('tbody > tr'):
                part_item = NonDiscParticularsItem()
                part_item['gross_sale'] = row.css('td:nth-child(1)::text').extract_first()
                part_item['gross_purchase'] = row.css('td:nth-child(2)::text').extract_first()
                part_item['pf_turnover_ratio'] = row.css('td:nth-child(3)::text').extract_first()
                part_item['performance_of_pf'] = row.css('td:nth-child(4)::text').extract_first()
                part_item['value_of_assets'] = row.css('td:nth-child(5)::text').extract_first()
                part_item['month'] = month
                part_item['code'] = "NONDISC"
                part_item['year'] = year
                amc_name = response.css('div[class="org-strong"] strong::text').get()
                part_item = amc_name[27:]
                yield part_item
