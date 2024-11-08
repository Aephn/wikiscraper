# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class NodeItem(Item):
    """Define Node Item Characteristic"""
    parent_node = Field()
    node_url = Field()
    node_children = Field()
