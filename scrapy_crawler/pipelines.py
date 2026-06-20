"""
Item pipelines enforce DATA ACCURACY and deduplication before export.
This is where "ensure data accuracy" from the brief actually gets implemented.
"""
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ValidationPipeline:
    """Drop items missing required fields; normalise types."""

    required = ("title", "url")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        for field in self.required:
            if not adapter.get(field):
                raise DropItem(f"Missing required field: {field}")

        # Coerce price to float when present (data-format handling).
        price = adapter.get("price")
        if price:
            try:
                adapter["price"] = float(price)
            except (TypeError, ValueError):
                spider.logger.warning("Unparseable price %r at %s", price, adapter["url"])
                adapter["price"] = None
        return item


class DedupePipeline:
    """Skip URLs already seen in this crawl."""

    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        url = ItemAdapter(item).get("url")
        if url in self.seen:
            raise DropItem(f"Duplicate item: {url}")
        self.seen.add(url)
        return item
