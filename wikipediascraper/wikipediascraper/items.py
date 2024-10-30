# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikipediascraperItem(scrapy.Item):
    # define individual nodes/links within the scraper
    parent_links = scrapy.Field()
    current_link = scrapy.Field()
    child_links = scrapy.Field()
