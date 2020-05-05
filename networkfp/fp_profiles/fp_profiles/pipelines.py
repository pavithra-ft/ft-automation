# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from idna import unicode
from scrapy.exporters import CsvItemExporter
import datetime


class FpProfilesPipeline(object):
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

    def process_item(self, item, spider):
        self.exporter.fields_to_export = ['amfi_arn', 'name', 'designation', 'company', 'city', 'mobile', 'mailid',
                                          'website', 'address']
        self.exporter.export_item(item)
        return item
