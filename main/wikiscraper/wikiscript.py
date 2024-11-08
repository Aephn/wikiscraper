# scrapy libraries
from spiders.wikispider import WikiSpider
from scrapy.crawler import CrawlerProcess

# validation libraries for input.
from urllib.parse import urlparse
import validators

"""
Main script managing crawler processes and user input.
Directly connects to JS/HTML/CSS Front-End.

Need to:
- Look into using multiple spiders for large BFS searches
- Look into ways to store the data in some way such that the 
    list of children for a given node can be developed.
"""

def url_input() -> list[str]:
    """Get the URL to scrape from the user."""
    while True:
        url = input("Give a URL to Scrape:")
        if validators.url(url):
            return [url]
        else:
            print("Invalid URL. Please try again.")
        
def depth_input() -> int:
    """Get the depth of the BFS crawl from the user."""
    MIN_DEPTH = 0
    MAX_DEPTH = 3

    while True:
        try:
            depth = int(input("Crawl Depth:"))
            if MIN_DEPTH <= depth and depth <= MAX_DEPTH:
               return depth
            else:
                print(f"Invalid Crawl Depth ({MIN_DEPTH}-{MAX_DEPTH}).")
        except ValueError:
            print("Please enter a valid number.")

def derive_url(start_url: str) -> str:
    """
    Derive the root URL from the start URL.
    Example: 'https://example.com/page' -> 'https://example.com'
    """
    parsed_url = urlparse(start_url)
    root_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return root_url

def begin_scrape() -> None:
    url = url_input()
    max_depth = depth_input()

    process = CrawlerProcess(
        settings={
            'USER_AGENT': 'scrapy',
            'ITEM_PIPELINES': {
                'pipelines.WikiscraperPipeline': 1
            },

            # define debug logging settings
            'LOG_ENABLED': True,
            'LOG_LEVEL': 'INFO',

            # define optimizations for the crawler
            'COOKES_ENABLED': False,
            'RETRY_ENABLED': False,

            # crawl with BFS instead of the native DFS.
            # defines behaviors for BFS.
            'DEPTH_LIMIT' : max_depth,
            'DEPTH_PRIORITY' : 1,
            "DEPTH_STATS_VERBOSE" : True,
            'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
            'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue',
            
            # Reactor settings
            'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
            'FEED_EXPORT_ENCODING': 'utf-8',

            # OUTDATED BFS IMPLEMENTATION
            # 'MAX_DEPTH' : 1, # specifes crawl depth.
            # 'SPIDER_MIDDLEWARES' : {
            #     'middlewares.BFSDepthMiddleware': 543
            # }
        }
    )

    # start the crawler process with configured settings.
    root_url = derive_url(url[0])
    process.crawl(WikiSpider, 
                  domain_list=url, 
                  filter_char=":", 
                  root_url=root_url,
                  filter_url_tag="/wiki/",
                  max_depth=max_depth)
    process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished

if __name__ == "__main__":
   begin_scrape()