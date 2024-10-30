import scrapy
import re

import scrapy.exporters

class WikiSpider(scrapy.Spider):
    name = "wikispider"
    start_urls = {
        # "https://en.wikipedia.org/wiki/Main_Page"
        "https://omori.fandom.com/wiki/OMORI_WIKI"
    }

    def parse(self, response):
        """
        Method built into Scrapy to scrape all elements on the webpage
        given specified parameters given by response.css
        """
        paths = set()   # use set to exclude duplicate values, NOT ordered.

        # https://en.wikipedia.org
        wikipedia_url = 'https://omori.fandom.com'   # add url back on

        for url in response.css('a::attr(href)').getall():
            if url.startswith('/wiki/') and (':' not in url):   # get only internal links
                paths.add(wikipedia_url+url)
                                   
        for path in paths:
            print(path)

        # needs to be in the same method?
        for path in paths:   # might explode lol
            # yield scrapy.Request(path, self.parse)
            yield self.trysmth(path)

    def trysmth(self, path):
        print("TRYING TO SCRAPE WITH FUNCTION")
        return scrapy.Request(path, self.parse)   # this is the issue


    def pair_parentlink():
        """create a tuple of parent link and child link(s)"""
        pass
    
    def export_all():
        """Export all parent pairs to a JSON file"""
        # https://docs.scrapy.org/en/2.11/topics/exporters.html#scrapy.exporters.JsonItemExporter
        scrapy.exporters.JsonItemExporter()
        pass

    # def test(self, paths):
    #     for path in paths:   # might explode lol
    #         yield scrapy.Request(path, self.parse)