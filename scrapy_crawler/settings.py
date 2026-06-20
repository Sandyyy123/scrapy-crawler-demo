BOT_NAME = "scrapy_crawler"

SPIDER_MODULES = ["scrapy_crawler.spiders"]
NEWSPIDER_MODULE = "scrapy_crawler.spiders"

# Identify the crawler honestly and obey robots.txt by default.
USER_AGENT = "scrapy-crawler-demo (+https://github.com/Sandyyy123/scrapy-crawler-demo)"
ROBOTSTXT_OBEY = True

# Politeness: throttle automatically, cap concurrency per domain.
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4
DOWNLOAD_DELAY = 0.5
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Resume-able crawls and HTTP caching for fast re-runs during development.
HTTPCACHE_ENABLED = True
RETRY_ENABLED = True
RETRY_TIMES = 3

ITEM_PIPELINES = {
    "scrapy_crawler.pipelines.ValidationPipeline": 100,
    "scrapy_crawler.pipelines.DedupePipeline": 200,
}

FEED_EXPORT_ENCODING = "utf-8"
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
