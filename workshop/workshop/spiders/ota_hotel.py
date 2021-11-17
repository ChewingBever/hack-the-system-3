import scrapy
from scrapy.linkextractors import LinkExtractor

server_location = 'http://35.233.25.116'


class DummyOtaHotelsSpider(scrapy.Spider):
    """ scrapy crawl ota_hotels -o hotels.json """
    name = "ota_hotel"

    # Skeleton implementation

    def start_requests(self):
        base_url = "http://35.233.25.116/sitemap/hotels/Amsterdam/"
        count = 13
        urls = [f"{base_url}?page={i}" for i in range(1, count + 1)]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_function)

    def parse_function(self, response):
        yield from response.follow_all([res.attrib["href"] for res in response.css("a.hotellink")], callback=self.parse_hotel_page)

    def parse_hotel_page(self, response):
        hotel_id = response.url.strip("/").split("/")[-1]
        card_div = response.css(".card-body")

        name_str = card_div.xpath("//h5/text()").get()
        texts = card_div.css(".text-muted::text").getall()
        address_str = " ".join(texts[:3])
        coord_str, rate_str = texts[3:]

        return {
            "id": hotel_id,
            "name": name_str,
            "address": address_str,
            "coord": coord_str,
            "rate": rate_str
        }
