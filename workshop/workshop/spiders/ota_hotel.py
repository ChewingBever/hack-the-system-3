import scrapy
from scrapy.linkextractors import LinkExtractor
import base64
import urllib.parse
import re

server_location = 'http://35.233.25.116'


class DummyOtaHotelsSpider(scrapy.Spider):
    """ scrapy crawl ota_hotels -o hotels.json """
    name = "ota_hotel"

    # Skeleton implementation

    def start_requests(self):
        # cities = ["Amsterdam", "Brussels", "Paris", "London"]
        cities = ["Berlin"]
        base_urls = [f"http://35.233.25.116/sitemap/hotels/{city}/" for city in cities]

        for base_url in base_urls:
            yield scrapy.Request(base_url, callback=self.parse_count)

    def parse_count(self, response):
        count = int(response.css(".pagination").re("Page 1 / ([0-9]+)")[0])

        for i in range(1, count + 1):
            yield scrapy.Request(f"{response.url.strip('/')}/?page={i}", cookies=response.request.cookies, callback=self.parse_list_page)

    def parse_list_page(self, response):
        for r in response.follow_all([res.attrib["href"] for res in response.css("a.hotellink")], callback=self.parse_hotel_page):
            path = r.url[len(server_location):]
            r.cookies = {"controlid": base64.b64encode(re.sub(r"[A-F0-9]{2}", lambda x: chr(int(x.group(0), 16)), urllib.parse.quote(path)).encode()).decode()}
            print(r.cookies)

            yield r

    def parse_hotel_page(self, response):
        hotel_id = response.url.strip("/").split("/")[-1]
        card_div = response.css(".card-body")

        name_str = card_div.xpath("//h5/text()").get()
        texts = card_div.css(".text-muted::text").getall()

        return {
            "id": hotel_id,
            "name": name_str,
            "texts": texts
        }
