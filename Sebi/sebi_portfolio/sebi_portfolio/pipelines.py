# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from idna import unicode
from scrapy.exporters import CsvItemExporter
import datetime
from .items import DiscretionaryItem, DiscParticularsItem, NonDiscretionaryItem, NonDiscParticularsItem
import pandas as pd


class SebiPortfolioPipeline(object):
    def __init__(self):
        self.file = ""

    def open_spider(self, spider):
        self.filename = r"file_%s_%s.csv" % (spider.name, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.file = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        data = pd.read_csv(self.filename)
        data = data.pivot_table(index=['month', 'year', 'types_of_clients',  'amc_name', 'code'],
                                values=['no_of_investors', 'listed', 'unlisted', 'plain_debt', 'stru_debt',
                                        'eq_derivative', 'mutual_funds', 'others', 'total'])
        data.pivot_table.sort_index(axis='values')
        data.to_csv(self.filename)

    def process_item(self, item, spider):
        if isinstance(item, DiscretionaryItem):
            return self.handleDiscretionary(item, spider)
        if isinstance(item, DiscParticularsItem):
            return self.handleDiscParticulars(item, spider)
        if isinstance(item, NonDiscretionaryItem):
            return self.handleNonDiscretionary(item, spider)
        if isinstance(item, NonDiscParticularsItem):
            return self.handleNonDiscParticulars(item, spider)

    def handleDiscretionary(self, item, spider):
        self.exporter.fields_to_export = ['amc_name', 'year', 'month', 'code', 'types_of_clients', 'no_of_investors',
                                          'listed', 'unlisted', 'plain_debt', 'stru_debt', 'eq_derivative',
                                          'mutual_funds', 'others', 'total']
        self.exporter.export_item(item)
        return item

    def handleDiscParticulars(self, item, spider):
        self.exporter.fields_to_export = ['amc_name', 'year', 'month', 'code', 'gross_sale', 'gross_purchase',
                                          'pf_turnover_ratio', 'performance_of_pf', 'value_of_assets']
        self.exporter.export_item(item)
        return item

    def handleNonDiscretionary(self, item, spider):
        self.exporter.fields_to_export = ['amc_name', 'year', 'month', 'code', 'types_of_clients', 'no_of_investors',
                                          'listed', 'unlisted', 'plain_debt', 'stru_debt', 'eq_derivative',
                                          'mutual_funds', 'others', 'total']
        self.exporter.export_item(item)
        return item

    def handleNonDiscParticulars(self, item, spider):
        self.exporter.fields_to_export = ['amc_name', 'year', 'month', 'code', 'gross_sale', 'gross_purchase',
                                          'pf_turnover_ratio', 'performance_of_pf', 'value_of_assets']
        self.exporter.export_item(item)
        return item
