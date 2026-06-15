"""Offline tests for the parsing logic (no network needed). Run: pytest -q"""
import scraper

SAMPLE_HTML = """
<div class="quote">
  <span class="text">&ldquo;The world is what we make it.&rdquo;</span>
  <small class="author">Ada Lovelace</small>
  <div class="tags"><a class="tag">inspiration</a><a class="tag">life</a></div>
</div>
<div class="quote">
  <span class="text">&ldquo;Code is poetry.&rdquo;</span>
  <small class="author">Anonymous</small>
  <div class="tags"><a class="tag">code</a></div>
</div>
<nav><ul class="pager"><li class="next"><a href="/page/2/">Next</a></li></ul></nav>
"""


def test_parse_quotes_extracts_fields():
    quotes = scraper.parse_quotes(SAMPLE_HTML)
    assert len(quotes) == 2
    assert quotes[0]["author"] == "Ada Lovelace"
    assert "inspiration" in quotes[0]["tags"] and "life" in quotes[0]["tags"]
    assert quotes[1]["author"] == "Anonymous"
    assert quotes[1]["tags"] == ["code"]


def test_next_page_url_resolves_absolute():
    nxt = scraper.next_page_url(SAMPLE_HTML, "https://quotes.toscrape.com/")
    assert nxt == "https://quotes.toscrape.com/page/2/"


def test_next_page_url_none_when_absent():
    assert scraper.next_page_url("<html><body></body></html>", "https://x/") is None
