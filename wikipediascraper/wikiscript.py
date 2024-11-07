from wikipediascraper.spiders.wikispider import WikiSpider
from scrapy.crawler import CrawlerProcess

# crawl based of a script here.

process = CrawlerProcess(
    settings={
        # "FEEDS": {"items.json": {"format": "json"},},
        'USER_AGENT': 'scrapy',
        'log_level': 'INFO',
        'ITEM_PIPELINES': {'wikipediascraper.pipelines.WikipediascraperPipeline': 1},
    }
)

domains = ["https://en.wikipedia.org/wiki/Main_Page"]

process.crawl(WikiSpider, domain_list=domains)
process.start(stop_after_crawl=True)  # the script will block here until the crawling is finished