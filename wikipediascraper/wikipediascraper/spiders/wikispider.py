import scrapy

class WikiSpider(scrapy.Spider):
    name = "wikispider"
    start_urls = {
        "https://en.wikipedia.org/wiki/Main_Page"
    }

    def parse(self, response):
        paths = []
        for url in response.css('a::attr(href)').getall():
            if url.startswith('/wiki/'):
                paths.append(url)

        print(paths)
        # response.css('a::attr(href)').getall()

        # yield response.follow(next_page, callback=self.parse)
        yield None
