# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
# useful for handling different item types with a single interface
from itemadapter.adapter import ItemAdapter
from scrapy.exceptions import DropItem
class EmptyItemPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.keys():
            raise DropItem("Dropped item with no attributes: {item!r}")
        else:
            return item
class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        print('hi')
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['id'])
            return item

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
    
class NeuralPipeline:
    def process_item(self, item, spider):
        return item
