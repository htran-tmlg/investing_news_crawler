# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class InvestingNewsAggregatorPipeline:
    def process_item(self, item, spider):
        # self.export_item(item)
        return item

    # def export_item(self, item):
    #     with open(os.path.join(BASE_DIR, 'test.jsonl'), 'wb') as f:
    #         exporter = JsonLinesItemExporter(f)
    #         exporter.start_exporting()
    #     print(item.title)

