# import scrapy
# from ..items import DiscretionaryItem, NonDiscretionaryItem, DiscParticularsItem, NonDiscParticularsItem
#
#
# class MonthlyreportSpider(scrapy.Spider):
#     name = "monthly_report"
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
#                     'month': i
#                     }
#             yield scrapy.FormRequest(self.formURL, formdata=data, callback=self.item_parser, dont_filter=True)
#
#     def item_parser(self, response):
#         # print(response.body)
#         # items_sebi = AmcItem()
#         # items_sebi['amc_name'] = response.css('div[class="org-strong"] strong::text').get()
#         # amc = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
#                                 'table-striped table-bordered table-hover background '
#                                 # 'statistics-table"] thead tr th:nth-child(4)::text').get()
#         # items_sebi['amc_month'] = month
#         # items_sebi['amc_year'] = amc[48:]
#         # yield items_sebi
#
#         #################DISCRETIONARY SERVICES########################
#         disc_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
#                                   'table-striped table-bordered table-hover background '
#                                   'statistics-table"]')[0]
#         for row in disc_table.css('tbody > tr'):
#             items = DiscretionaryItem()
#             items['s_no'] = row.css('td:nth-child(1)::text').extract_first()
#             items['types_of_clients'] = row.css('td:nth-child(2)::text').extract_first()
#             items['no_of_investors'] = row.css('td:nth-child(3)::text').extract_first()
#             items['listed'] = row.css('td:nth-child(4)::text').extract_first()
#             items['unlisted'] = row.css('td:nth-child(5)::text').extract_first()
#             items['plain_debt'] = row.css('td:nth-child(6)::text').extract_first()
#             items['stru_debt'] = row.css('td:nth-child(7)::text').extract_first()
#             items['eq_derivative'] = row.css('td:nth-child(8)::text').extract_first()
#             items['mutual_funds'] = row.css('td:nth-child(9)::text').extract_first()
#             items['others'] = row.css('td:nth-child(10)::text').extract_first()
#             items['total'] = row.css('td:nth-child(11)::text').extract_first()
#             yield items
#
#         # #################PARTICULARS########################
#         particulars_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
#                                          'table-striped table-bordered table-hover background '
#                                          'statistics-table"]')[1]
#         for header in particulars_table.css('thead > tr'):
#             p_item = DiscParticularsItem()
#             p_item['gross_sale'] = header.css('th:nth-child(1)::text').extract_first()
#             p_item['gross_purchase'] = header.css('th:nth-child(2)::text').extract_first()
#             p_item['pf_turnover_ratio'] = header.css('th:nth-child(3)::text').extract_first()
#             p_item['performance_of_pf'] = header.css('th:nth-child(4)::text').extract_first()
#             p_item['value_of_assets'] = header.css('th:nth-child(5)::text').extract_first()
#             yield p_item
#
#         for row in particulars_table.css('tbody > tr'):
#             p_item = DiscParticularsItem()
#             p_item['gross_sale'] = row.css('td:nth-child(1)::text').extract_first()
#             p_item['gross_purchase'] = row.css('td:nth-child(2)::text').extract_first()
#             p_item['pf_turnover_ratio'] = row.css('td:nth-child(3)::text').extract_first()
#             p_item['performance_of_pf'] = row.css('td:nth-child(4)::text').extract_first()
#             p_item['value_of_assets'] = row.css('td:nth-child(5)::text').extract_first()
#             yield p_item
#
#         # #################NON DISCRETIONARY SERVICES########################
#         non_disc_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
#                                       'table-striped table-bordered table-hover background '
#                                       'statistics-table"]')[2]
#         for row in non_disc_table.css('tbody > tr'):
#             nd_items = NonDiscretionaryItem()
#             nd_items['s_no'] = row.css('td:nth-child(1)::text').extract_first()
#             nd_items['types_of_clients'] = row.css('td:nth-child(2)::text').extract_first()
#             nd_items['no_of_investors'] = row.css('td:nth-child(3)::text').extract_first()
#             nd_items['listed'] = row.css('td:nth-child(4)::text').extract_first()
#             nd_items['unlisted'] = row.css('td:nth-child(5)::text').extract_first()
#             nd_items['plain_debt'] = row.css('td:nth-child(6)::text').extract_first()
#             nd_items['stru_debt'] = row.css('td:nth-child(7)::text').extract_first()
#             nd_items['eq_derivative'] = row.css('td:nth-child(8)::text').extract_first()
#             nd_items['mutual_funds'] = row.css('td:nth-child(9)::text').extract_first()
#             nd_items['others'] = row.css('td:nth-child(10)::text').extract_first()
#             nd_items['total'] = row.css('td:nth-child(11)::text').extract_first()
#             yield nd_items
#
#         # #################PARTICULARS########################
#         part_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
#                                   'table-striped table-bordered table-hover background '
#                                   'statistics-table"]')[3]
#         for header in part_table.css('thead > tr'):
#             part_item = NonDiscParticularsItem()
#             part_item['gross_sale'] = header.css('th:nth-child(1)::text').extract_first()
#             part_item['gross_purchase'] = header.css('th:nth-child(2)::text').extract_first()
#             part_item['pf_turnover_ratio'] = header.css('th:nth-child(3)::text').extract_first()
#             part_item['performance_of_pf'] = header.css('th:nth-child(4)::text').extract_first()
#             part_item['value_of_assets'] = header.css('th:nth-child(5)::text').extract_first()
#             yield part_item
#
#         for row in part_table.css('tbody > tr'):
#             part_item = NonDiscParticularsItem()
#             part_item['gross_sale'] = row.css('td:nth-child(1)::text').extract_first()
#             part_item['gross_purchase'] = row.css('td:nth-child(2)::text').extract_first()
#             part_item['pf_turnover_ratio'] = row.css('td:nth-child(3)::text').extract_first()
#             part_item['performance_of_pf'] = row.css('td:nth-child(4)::text').extract_first()
#             part_item['value_of_assets'] = row.css('td:nth-child(5)::text').extract_first()
#             yield part_item
#
#         # #################ADVISORY SERVICES########################
#         advisory_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
#                                       'table-striped table-bordered table-hover background '
#                                       'statistics-table"]')[4]
#         for header in advisory_table.css('thead > tr'):
#             advisory_item = AdvisoryItem()
#             advisory_item['s_no'] = header.css('th:nth-child(1)::text').extract_first()
#             advisory_item['advisory_business'] = header.css('th:nth-child(2)::text').extract_first()
#             advisory_item['total'] = header.css('th:nth-child(3)::text').extract_first()
#             yield advisory_item
#
#         for row in advisory_table.css('tbody > tr'):
#             advisory_item = AdvisoryItem()
#             advisory_item['s_no'] = row.css('td:nth-child(1)::text').extract_first()
#             advisory_item['advisory_business'] = row.css('td:nth-child(2)::text').extract_first()
#             advisory_item['total'] = row.css('td:nth-child(3)::text').extract_first()
#             yield advisory_item
#
#         # #################COMPLAINTS########################
#         complaints_table = response.css('div[class="portlet purple"] div[class="org-table-1"] table[class="table '
#                                         'table-striped table-bordered table-hover background '
#                                         'statistics-table"]')[5]
#         for header in complaints_table.css('thead > tr'):
#             com_item = ComplaintsItem()
#             com_item['s_no'] = header.css('th:nth-child(1)::text').extract_first()
#             com_item['type_of_clients'] = header.css('th:nth-child(2)::text').extract_first()
#             com_item['pending_beginning'] = header.css('th:nth-child(3)::text').extract_first()
#             com_item['received'] = header.css('th:nth-child(4)::text').extract_first()
#             com_item['resolved'] = header.css('th:nth-child(5)::text').extract_first()
#             com_item['pending_ending'] = header.css('th:nth-child(6)::text').extract_first()
#             yield com_item
#
#         for row in complaints_table.css('tbody > tr'):
#             com_item = ComplaintsItem()
#             com_item['s_no'] = row.css('td:nth-child(1)::text').extract_first()
#             com_item['type_of_clients'] = row.css('td:nth-child(2)::text').extract_first()
#             com_item['pending_beginning'] = row.css('td:nth-child(3)::text').extract_first()
#             com_item['received'] = row.css('td:nth-child(4)::text').extract_first()
#             com_item['resolved'] = row.css('td:nth-child(5)::text').extract_first()
#             com_item['pending_ending'] = row.css('td:nth-child(6)::text').extract_first()
#             yield com_item
