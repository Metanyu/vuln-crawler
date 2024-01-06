# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
# useful for handling different item types with a single interface
from itemadapter.adapter import ItemAdapter
from scrapy.exceptions import DropItem
class EmptyItemPipeline:
    def process_item(self, item, spider):
        if not item.keys():
            raise DropItem("Dropped item with no attributes: {item!r}")
        else:
            return item

class DuplicatesPipeline:
    def process_item(self, item, spider):
        path = os.path.join('data', item['breadcrumbItems'][1]['label'], item['id']) + '.json'
        if os.path.exists(path):
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            return item

class JsonWriterPipeline:
    def process_item(self, item, spider):
        path = os.path.join('data', item['breadcrumbItems'][1]['label'])
        if not os.path.exists(path):
            os.makedirs(path)
        # Open the file
        with open(os.path.join(path, item['id']) + '.json', 'w') as f:
        # Use json.dump to write data into the file
            json.dump(item, f, indent=4)
        return item
    
class NeuralPipeline:
    def process_item(self, item, spider):
        return item
