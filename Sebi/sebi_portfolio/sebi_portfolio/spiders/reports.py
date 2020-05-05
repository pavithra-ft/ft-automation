import scrapy
from ..items import DiscretionaryItem, NonDiscretionaryItem


class ReportSpider(scrapy.Spider):
    name = "report"
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
#################DISCRETIONARY SERVICES########################
        disc_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
                                  'table-striped table-bordered table-hover background '
                                  'statistics-table"]')
        if disc_table:
            disc_table = disc_table[0]
            for index, row in enumerate(disc_table.css('tbody > tr')):
                if index > 2:
                    items = DiscretionaryItem()
                    items['s_no'] = row.css('td:nth-child(1)::text').extract_first()
                    items['types_of_clients'] = row.css('td:nth-child(2)::text').extract_first()
                    items['no_of_investors'] = row.css('td:nth-child(3)::text').extract_first()
                    items['listed'] = row.css('td:nth-child(4)::text').extract_first()
                    items['unlisted'] = row.css('td:nth-child(5)::text').extract_first()
                    items['plain_debt'] = row.css('td:nth-child(6)::text').extract_first()
                    items['stru_debt'] = row.css('td:nth-child(7)::text').extract_first()
                    items['eq_derivative'] = row.css('td:nth-child(8)::text').extract_first()
                    items['mutual_funds'] = row.css('td:nth-child(9)::text').extract_first()
                    items['others'] = row.css('td:nth-child(10)::text').extract_first()
                    items['total'] = row.css('td:nth-child(11)::text').extract_first()
                    items['month'] = month
                    items['code'] = "DISC"
                    items['year'] = year
                    amc_name = response.css('div[class="org-strong"] strong::text').get()
                    items['amc_name'] = amc_name[27:]
                    yield items

# #################NON DISCRETIONARY SERVICES########################
        non_disc_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
                                      'table-striped table-bordered table-hover background '
                                      'statistics-table"]')
        if non_disc_table:
            non_disc_table = non_disc_table[2]
            for index, row in enumerate(non_disc_table.css('tbody > tr')):
                if index > 2:
                    nd_items = NonDiscretionaryItem()
                    nd_items['s_no'] = row.css('td:nth-child(1)::text').extract_first()
                    nd_items['types_of_clients'] = row.css('td:nth-child(2)::text').extract_first()
                    nd_items['no_of_investors'] = row.css('td:nth-child(3)::text').extract_first()
                    nd_items['listed'] = row.css('td:nth-child(4)::text').extract_first()
                    nd_items['unlisted'] = row.css('td:nth-child(5)::text').extract_first()
                    nd_items['plain_debt'] = row.css('td:nth-child(6)::text').extract_first()
                    nd_items['stru_debt'] = row.css('td:nth-child(7)::text').extract_first()
                    nd_items['eq_derivative'] = row.css('td:nth-child(8)::text').extract_first()
                    nd_items['mutual_funds'] = row.css('td:nth-child(9)::text').extract_first()
                    nd_items['others'] = row.css('td:nth-child(10)::text').extract_first()
                    nd_items['total'] = row.css('td:nth-child(11)::text').extract_first()
                    nd_items['month'] = month
                    nd_items['code'] = "NONDISC"
                    nd_items['year'] = year
                    amc_name = response.css('div[class="org-strong"] strong::text').get()
                    nd_items['amc_name'] = amc_name[27:]
                    yield nd_items
