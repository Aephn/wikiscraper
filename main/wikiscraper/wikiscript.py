from spiders.wikispider import WikiSpider
from scrapy.crawler import CrawlerProcess

import validators

"""
Main script managing crawler processes and user input.
Directly connects to JS/HTML/CSS Front-End.

Need to:
- Add a BFS implementation of scraping
- Look into using multiple spiders for large BFS searches
"""

def url_input() -> list[str]:
    """Get the URL to scrape from the user."""
    url = input("Give a URL to Scrape:")
    return [url]

def depth_input() -> int:
    """Get the depth of the BFS crawl from the user."""
    while True:
        try:
            depth = int(input("Crawl Depth:"))
            return depth
        except ValueError:
            print("Please enter a valid number.")

def derive_url(start_url) -> str:
    """
    Derive the root url from the start url. Inefficient,
    but only needs to process the urls once.
    """
    root_url = start_url.split('/')[:3]
    root_url[1] = '//'
    root_url = ''.join(root_url)
    return root_url


if __name__ == "__main__":
    # define settings amnd pipeline for crawler
    url = url_input()
    max_depth = depth_input()


    process = CrawlerProcess(
        settings={
            'USER_AGENT': 'scrapy',
            'log_level': 'WARNING',
            'ITEM_PIPELINES': {
                'pipelines.WikiscraperPipeline': 1
            },

            # define optimizations for the crawler
            'COOKES_ENABLED': False,
            'RETRY_ENABLED': False,

            # crawl with BFS instead of the native DFS.
            'DEPTH_LIMIT' : max_depth,
            'DEPTH_PRIORITY' : 1,
            # "DEPTH_STATS_VERBOSE" : True,
            'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
            'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue',
            
            # OUTDATED BFS IMPLEMENTATION
            # 'MAX_DEPTH' : 1, # specifes crawl depth.
            # 'SPIDER_MIDDLEWARES' : {
            #     'middlewares.BFSDepthMiddleware': 543
            # }
        }
    )

    process.crawl(WikiSpider, domain_list=url, filter_char=":", root_url=derive_url(url[0]))
    process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished