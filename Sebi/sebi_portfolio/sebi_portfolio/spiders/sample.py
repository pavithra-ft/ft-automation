# import scrapy
# from ..items import AmcItem, DiscretionaryItem, NonDiscretionaryItem, DiscParticularsItem, \
#     AdvisoryItem, ComplaintsItem, NonDiscParticularsItem
#
#
# class MonthlyreportSpider(scrapy.Spider):
#     name = "test"
#     allowed_domains = ['https://www.sebi.gov.in']
#     formURL = "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes"
#
#     def start_requests(self):
#         urls = ["https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes"]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)
#
#     def parse(self, response):
#         for i in range(1, 13):
#             data = {'pmrId': "1000171371@@INP000004243@@BANYAN CAPITAL ADVISORS PRIVATE LIMITED",
#                     'year': "2019",
#                     'month': str(i)
#                     }
#             yield scrapy.FormRequest(self.formURL, formdata=data, callback=self.item_parser, dont_filter=True,cb_kwargs={"month":i})
#
#     def item_parser(self, response,month):
#
#         #################DISCRETIONARY SERVICES########################
#         disc_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
#                                   'table-striped table-bordered table-hover background '
#                                   'statistics-table"]')[0]
#         # code = response.css("member-wrapper section div:nth-child(4) strong::text").get()
#
#         for index, row in enumerate(disc_table.css('tbody > tr')):
#             if index > 2:
#                 items = DiscretionaryItem()
#                 items['s_no'] = row.css('td:nth-child(1)::text').extract_first()
#                 items['types_of_clients'] = row.css('td:nth-child(2)::text').extract_first()
#                 items['no_of_investors'] = row.css('td:nth-child(3)::text').extract_first()
#                 items['listed'] = row.css('td:nth-child(4)::text').extract_first()
#                 items['unlisted'] = row.css('td:nth-child(5)::text').extract_first()
#                 items['plain_debt'] = row.css('td:nth-child(6)::text').extract_first()
#                 items['stru_debt'] = row.css('td:nth-child(7)::text').extract_first()
#                 items['eq_derivative'] = row.css('td:nth-child(8)::text').extract_first()
#                 items['mutual_funds'] = row.css('td:nth-child(9)::text').extract_first()
#                 items['others'] = row.css('td:nth-child(10)::text').extract_first()
#                 items['total'] = row.css('td:nth-child(11)::text').extract_first()
#                 items['month'] = month
#                 items['code'] = "DISC"
#                 yield items