# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class LeadsPipeline:
    def process_item(self, item, spider):
        with open('leads.json', 'r+') as f:
            file = f.read()
            obj = json.load(file)
            obj['list'].append(item)
            f.seek(0)
            f.write(json.dumps(obj))
            f.close()
        return item
