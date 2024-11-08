import scrapy
from scrapy import Request
from pathlib import Path
import sys

# Add current directory to PYTHONPATH to avoid
# ModuleNotFoundError when running the script.
sys.path.append(str(Path(__file__).parent))
from items import NodeItem

class WikiSpider(scrapy.Spider):
    name = "wikispider"

    def __init__(self, domain_list: list=[], root_url: str="", filter_char: str=""):
        """
        self.start_urls: list[str] -> List of URLs to scrape.
        self.root_url: str -> The root URL of the domain.
        self.filter_char: str -> The character to filter out from the URLs.
        """
        self.start_urls = domain_list
        self.root_url = root_url
        self.filter_char = filter_char

    def parse(self, response):
        """
        Parse the page content and return an NodeItem() scrapy Item.

        response: TextResponse -> Holds the page content.
        """
        paths = []
        result_file = Path(f"link_urls.txt")
        
        # create separate items for each url scraped from the page.
        node = NodeItem()
        for url in response.css('a::attr(href)').getall():
            if url.startswith('/wiki/') and self.filter_char not in url:
                yield Request("".join([self.root_url, url]), callback=self.parse)
                # node['parent_node'] = response.url
                # node['node_url'] = self.root_url+url
                # node['node_children'] = []
                # yield node
