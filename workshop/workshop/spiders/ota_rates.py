import scrapy

server_location = 'http://35.233.25.116'


class DummyOtaRatesSpider(scrapy.Spider):
    """ scrapy crawl ota_hotels -o hotels.json """
    name = "ota_hotels"

    # Skeleton implementation

    def start_requests(self):
        base_url = "http://35.233.25.116/sitemap/hotels/Amsterdam/"
        count = 13
        urls = [f"{base_url}?page={i}" for i in range(1, count + 1)]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_function)

    def parse_function(self, response):
        yield {"Success": True}

