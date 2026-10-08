import json
from urllib.request import Request, urlopen

import feedparser  # type: ignore[import-untyped]
import trafilatura

# Target ABC RSS URL (e.g., Just In / Top News)
RSS_URL = "https://www.abc.net.au/news/feed/51120/rss.xml"


def fetch_article_text(url):
    """Download a linked page and extract its main article as plain text."""
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=20) as response:
        html = response.read()

    # Remove HTML markup, navigation, and other surrounding page content.
    return trafilatura.extract(html, include_comments=False) or ""


def fetch_abc_news(limit=5):
    """Return the latest ABC feed entries without downloading article pages."""
    # Parse the feed directly from the network URL
    feed = feedparser.parse(RSS_URL)

    # Check if the feed retrieved successfully
    if feed.bozo:
        raise RuntimeError(
            "Could not retrieve or parse the ABC RSS feed."
        ) from feed.get("bozo_exception")

    entries = [
        {
            "title": entry.get("title", "No Title"),
            "link": entry.get("link", ""),
            "published": entry.get("published", "No Date"),
            "summary": entry.get("summary", "No Summary Available"),
        }
        for entry in feed.entries[:limit]
    ]
    return json.dumps(entries, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print(fetch_abc_news(limit=10))
