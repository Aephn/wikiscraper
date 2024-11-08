import scrapy
from scrapy import Request
from pathlib import Path

import validators

# Add current directory to PYTHONPATH to avoid
# ModuleNotFoundError when running the script.
import sys
sys.path.append(str(Path(__file__).parent))
from items import NodeItem

class WikiSpider(scrapy.Spider):
    name = "wikispider"

    def __init__(self, domain_list: list=[], root_url: str="", 
                 filter_char: str="", filter_url_tag: str = "",
                 max_depth: int=0):
        """
        Initialize the spider with start URLs, root URL, filter character, and max depth.

        :param domain_list: List of URLs to scrape.
        :param root_url: The root URL of the domain.
        :param filter_char: The character to filter out from the URLs.
        :param max_depth: Maximum depth to crawl.
        """
        self.start_urls = domain_list
        self.root_url = root_url

        self.filter_url_tag = filter_url_tag
        self.filter_char = filter_char

        # Set the maximum depth of the BFS crawl.
        self.max_depth = max_depth

    def url_filter(self, url: str) -> bool:
        """
        Defines how the URL on the page will be filtered.
        Given a URL, return True if the URL shouldn't be filtered out.
        Else, return False.

        :param url: The URL to filter.
        """
        return url.startswith(self.filter_url_tag) and self.filter_char not in url
    
    def relative_url_filter(self, url: str) -> str:
        """
        Complete URL if url is relative.
        check if the url is relative, and if it is, complete the URL.
        
        :param url: The URL to check.
        """
        if not validators.url(url):
            return "".join([self.root_url, url])
        else:
            return url

    def parse(self, response):
        """
        Parse the page content and return an NodeItem() scrapy Item.

        :param response: The response object.
        """
        
        # get current depth of the response. 0 if not set.
        current_depth = response.meta.get('depth', 0)

        # skip scraping pages if the current depth is greater than the max depth.
        if current_depth >= self.max_depth:
            return None
        
        # create separate items for each url scraped from the page.
        node = NodeItem()
        for url in response.css('a::attr(href)').getall():
            if self.url_filter(url):
                
                full_url = self.relative_url_filter(url)
                yield Request(full_url, callback=self.parse)
                
                # yield a scrapy NodeItem() object. (PASSES TO pipelines.py)
                node['parent_node'] = response.url
                node['node_url'] = self.root_url+url
                node['node_children'] = []   # NOTE: need to figure how to append children links to the list.
                yield node
