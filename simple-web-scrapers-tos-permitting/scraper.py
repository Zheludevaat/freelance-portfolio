"""Polite web scraper for quotes.toscrape.com.

quotes.toscrape.com is a public sandbox published specifically for scraping
practice, so this sample respects Terms of Service by design. The scraper:

  * sends a real User-Agent and a short delay between requests (politeness),
  * follows pagination until there are no more pages,
  * parses each quote's text, author, and tags,
  * exports the results to both CSV and JSON.

The HTML parsing is split into a pure `parse_quotes()` function so it can be
unit-tested without any network access.

Usage:
    pip install -r requirements.txt
    python scraper.py            # scrape all pages -> quotes.csv / quotes.json
    python scraper.py --max-pages 2
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
HEADERS = {"User-Agent": "portfolio-sample-scraper/1.0 (+contact: see README)"}


def parse_quotes(html: str) -> list[dict]:
    """Extract quotes from a page of HTML. Pure function - no network."""
    soup = BeautifulSoup(html, "html.parser")
    quotes = []
    for q in soup.select("div.quote"):
        text_el = q.select_one("span.text")
        author_el = q.select_one("small.author")
        quotes.append({
            "text": text_el.get_text(strip=True) if text_el else "",
            "author": author_el.get_text(strip=True) if author_el else "",
            "tags": [t.get_text(strip=True) for t in q.select("a.tag")],
        })
    return quotes


def next_page_url(html: str, current_url: str) -> Optional[str]:
    """Return the absolute URL of the next page, or None if there isn't one."""
    soup = BeautifulSoup(html, "html.parser")
    nxt = soup.select_one("li.next > a")
    return urljoin(current_url, nxt["href"]) if nxt else None


def scrape(max_pages: Optional[int] = None, delay: float = 1.0) -> list[dict]:
    """Scrape quotes across pages, politely."""
    url: Optional[str] = BASE_URL
    all_quotes: list[dict] = []
    pages = 0
    session = requests.Session()
    while url:
        resp = session.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        all_quotes.extend(parse_quotes(resp.text))
        pages += 1
        if max_pages is not None and pages >= max_pages:
            break
        url = next_page_url(resp.text, url)
        if url:
            time.sleep(delay)  # be polite between requests
    return all_quotes


def export(quotes: list[dict], csv_path: str = "quotes.csv",
           json_path: str = "quotes.json") -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "author", "tags"])
        for q in quotes:
            writer.writerow([q["text"], q["author"], "; ".join(q["tags"])])


def main() -> None:
    ap = argparse.ArgumentParser(description="Scrape quotes.toscrape.com")
    ap.add_argument("--max-pages", type=int, default=None,
                    help="limit number of pages (default: all)")
    ap.add_argument("--delay", type=float, default=1.0,
                    help="seconds to wait between requests")
    args = ap.parse_args()
    quotes = scrape(max_pages=args.max_pages, delay=args.delay)
    export(quotes)
    print(f"Scraped {len(quotes)} quotes -> quotes.csv, quotes.json")


if __name__ == "__main__":
    main()
