# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from idna import unicode
from scrapy.exporters import CsvItemExporter
import datetime


class FbspIndiaPipeline(object):
    def __init__(self):
        self.file = ""

    def open_spider(self, spider):
        file = "file_%s_%s.csv" % (spider.name, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        self.file = open(file, 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
