# Polite Web Scraper (quotes.toscrape.com)

A small, well-behaved scraper that collects quotes, authors, and tags across
all pages of a site and exports them to CSV and JSON.

## Why this target

[quotes.toscrape.com](https://quotes.toscrape.com/) is a public sandbox
published specifically for scraping practice, so this sample respects Terms of
Service by design. For real client work I always check the target site's
`robots.txt` and terms first, throttle requests, and decline anything a site
prohibits.

## What it demonstrates

- Real `User-Agent` and a polite delay between requests
- Pagination handling (follows "Next" until the last page)
- Clean parsing with BeautifulSoup, split into a pure, testable function
- Export to both CSV and JSON
- Offline unit tests for the parsing logic

## Run it

```bash
pip install -r requirements.txt
python scraper.py                # all pages -> quotes.csv, quotes.json
python scraper.py --max-pages 2  # just the first two pages
```

## Tests

```bash
pytest -q
```

The tests run fully offline against an HTML fixture, so they need no network.
A small `sample_output.csv` shows the shape of the exported data.
