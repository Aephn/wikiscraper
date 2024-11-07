import scrapy

class WikiSpider(scrapy.Spider):
    name = "wikispider"
    def __init__(self, domain_list: list = []):
        self.start_urls = domain_list

    def parse(self, response):
        paths = []
        for url in response.css('a::attr(href)').getall():
            if url.startswith('/wiki/') and ':' not in url:
                paths.append(url)

        print(paths)

        # yield response.follow(next_page, callback=self.parse)
        yield None
