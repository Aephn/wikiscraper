import scrapy
from pathlib import Path
import sys

# Add current directory to PYTHONPATH to avoid
# ModuleNotFoundError when running the script.
sys.path.append(str(Path(__file__).parent))
from wiki_items import NodeItem

class WikiSpider(scrapy.Spider):
    """
    response: TextResponse -> Holds the page content.
    """

    name = "wikispider"

    def __init__(self, domain_list: list = []):
        self.start_urls = domain_list
        self.filter_character = ':'

    def parse(self, response):
        paths = []
        result_file = Path(f"link_urls.txt")
        
        root_url = "https://en.wikipedia.org"

        # create separate items for each url scraped from the page.
        node = NodeItem()
        for url in response.css('a::attr(href)').getall():
            if url.startswith('/wiki/') and self.filter_character not in url:
                node['parent_node'] = response.url
                node['node_url'] = root_url+url
                node['node_children'] = []
                yield node
