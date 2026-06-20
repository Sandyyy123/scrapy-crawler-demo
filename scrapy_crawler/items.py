import scrapy


class ProductItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
