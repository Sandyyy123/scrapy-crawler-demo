"""
Example product spider demonstrating production Scrapy patterns:
- CSS + XPath extraction with ItemLoaders for clean, typed output
- Pagination following with depth control
- Per-request metadata threading
- Graceful handling of missing fields (data accuracy first)

Run:
    scrapy crawl products -O out/products.json
"""
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join

from scrapy_crawler.items import ProductItem


def clean_price(value: str) -> str:
    return value.replace("$", "").replace(",", "").strip()


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    custom_settings = {
        # Be a good citizen: throttle, obey robots, identify ourselves.
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2.0,
        "DOWNLOAD_DELAY": 0.5,
        "ROBOTSTXT_OBEY": True,
    }

    def parse(self, response):
        for card in response.css("article.product_pod"):
            detail_url = card.css("h3 a::attr(href)").get()
            yield response.follow(
                detail_url,
                callback=self.parse_product,
                meta={"list_price": card.css("p.price_color::text").get()},
            )

        # Follow pagination until there is no "next" link.
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        loader = ItemLoader(item=ProductItem(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.add_css("title", "div.product_main h1::text")
        loader.add_value("price", clean_price(response.meta["list_price"]))
        loader.add_css(
            "availability",
            "p.availability::text",
            MapCompose(str.strip),
            Join(),
        )
        loader.add_css("rating", "p.star-rating::attr(class)",
                       MapCompose(lambda c: c.replace("star-rating", "").strip()))
        loader.add_value("url", response.url)
        loader.add_css(
            "description",
            "#product_description ~ p::text",
        )
        yield loader.load_item()
