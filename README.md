> **⚠️ Proprietary — All Rights Reserved.** © 2026 Sandeep Grover. This repository is licensed to Sandeep Grover and may **not** be used, run, copied, modified, distributed, or used to train models without prior written permission. Public visibility does not grant a license. See [LICENSE](LICENSE).

---

# scrapy-crawler-demo

A small, production-shaped **Scrapy** project showing how I build website scrapers:
robust extraction, pagination, data validation, deduplication, and clean exports.

This is a demo for a website-scraping engagement. The target site
(`books.toscrape.com`) is a sandbox built specifically for scraper practice, so the
crawl is fully legal and reproducible.

## Architecture

```
                +------------------+
  start_urls -> |  ProductsSpider  |  CSS/XPath extraction + pagination
                +--------+---------+
                         | yields Request(detail) / Item
                         v
                +------------------+
                |   ItemLoader     |  typed, cleaned fields
                +--------+---------+
                         v
        +----------------+----------------+
        | ValidationPipeline (accuracy)   |  drop incomplete, coerce types
        +----------------+----------------+
                         v
        +----------------+----------------+
        | DedupePipeline (no duplicates)  |
        +----------------+----------------+
                         v
                  out/products.json  (or CSV / JSONL / DB)
```

## What it demonstrates

- **CSS + XPath + ItemLoaders** — clean, typed extraction instead of brittle regex
- **Pagination following** — crawls every catalogue page via the `next` link
- **AutoThrottle + robots.txt** — polite, ban-resistant crawling out of the box
- **Validation pipeline** — enforces required fields and coerces `price` to float
  (this is the "ensure data accuracy" requirement made concrete)
- **Dedup pipeline** — guarantees one row per URL
- **Multiple export formats** — JSON / JSONL / CSV with one flag
- **Resumable + cached** — HTTP cache and retries for fast iteration

## Setup

```bash
pip install -r requirements.txt
scrapy crawl products -O out/products.json     # JSON array
scrapy crawl products -O out/products.csv      # CSV
scrapy crawl products -O out/products.jsonl    # one JSON object per line
```

## Extending this to a real target

For a client site I add, as needed:
- **Playwright/Selenium middleware** for JavaScript-rendered pages
- **Rotating proxies + headers** for anti-bot sites
- **DB pipeline** (PostgreSQL/SQLite) instead of flat files
- **Scheduling** (cron / Scrapyd) for ongoing/recurring crawls
- **Delta crawling** so re-runs only fetch what changed

Built by Dr. Sandeep Grover.
