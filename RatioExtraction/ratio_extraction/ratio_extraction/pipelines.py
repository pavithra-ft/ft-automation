# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter
from .settings import BASE_DIR
from .items import BseSectorItem


class RatioExtractionPipeline:
    filename = BASE_DIR + "/ExportedData/"

    def __init__(self):
        self.file = ""

    def open_spider(self, spider):
        self.filename = self.filename + '%s.json' % spider.name
        self.file = open(self.filename, 'wb')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, BseSectorItem):
            return self.handleBseSector(item, spider)

    def handleBseSector(self, item, spider):
        self.exporter.fields_to_export = ['index_code', 'sector_name', 'sector_exposure']
        self.exporter.export_item(item)
        return item
