from wikipediascraper.spiders.wikispider import WikiSpider
from scrapy.crawler import CrawlerProcess

# crawl based of a script here.

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    }
)

process.crawl(WikiSpider)
process.start()  # the script will block here until the crawling is finished``