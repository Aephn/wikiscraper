# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pathlib import Path
import logging

class WikiscraperPipeline(object):
    """
    Defines the behavior for processing items yielded by the spider.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        self.logger.info(f"Processing item: {item}")
        print(item)
