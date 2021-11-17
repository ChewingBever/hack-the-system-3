import scrapy

server_location = 'http://35.233.25.116'


class DummyOtaHotelsSpider(scrapy.Spider):
    """ scrapy crawl ota_hotels -o hotels.json """
    name = "ota_hotels"

    # Skeleton implementation

    def start_requests(self):
        yield scrapy.Request(url='https://www.google.com/', callback=self.parse_function)

    def parse_function(self, response):
        yield {"Success": True}

