# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import JsonItemExporter
from .settings import BASE_DIR


class RatioExtractionPipeline:
    filename = BASE_DIR + r"/extracted_data/"

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
        self.exporter.export_item(item)
        return item
