import json
import logging
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from ddgs import DDGS
import feedparser  # type: ignore[import-untyped]
import trafilatura

logger = logging.getLogger(__name__)
MAX_PAGE_BYTES = 2_000_000


def search_web(query: str, max_results: int = 5) -> str:
    """Find web sources, returning titles, URLs and snippets as JSON."""
    if not isinstance(query, str) or not query.strip() or len(query) > 1000:
        return json.dumps({"error": "query must contain 1 to 1000 characters"})
    if type(max_results) is not int or not 1 <= max_results <= 10:
        return json.dumps({"error": "max_results must be an integer from 1 to 10"})
    try:
        results = DDGS(timeout=5).text(query.strip(), max_results=max_results)
        return json.dumps({"results": [
            {"title": item.get("title", ""), "url": item.get("href", ""),
             "snippet": item.get("body", "")}
            for item in results[:max_results]
        ]}, ensure_ascii=False)
    except Exception:
        logger.exception("Web search failed")
        return json.dumps({"error": "Web search failed; try again or provide a URL"})


def browse_web(url: str, max_chars: int = 12000) -> str:
    """Read text from a public HTML or plain-text web page."""
    if type(max_chars) is not int or not 1 <= max_chars <= 50000:
        return json.dumps({"error": "max_chars must be an integer from 1 to 50000"})
    try:
        if not isinstance(url, str):
            raise ValueError("url must be an HTTP or HTTPS URL")
        parsed = urlsplit(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("url must be an HTTP or HTTPS URL")
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("URL credentials are not supported")
        request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html,text/plain"})
        with urlopen(request, timeout=5) as response:
            content_type = response.headers.get_content_type()
            if content_type not in {"text/html", "application/xhtml+xml", "text/plain"}:
                raise ValueError("Only HTML and plain-text pages are supported")
            data = response.read(MAX_PAGE_BYTES + 1)
            if len(data) > MAX_PAGE_BYTES:
                raise ValueError("Page exceeds the 2 MB download limit")
            source_url = response.geturl()
            charset = response.headers.get_content_charset() or "utf-8"
        if content_type == "text/plain":
            page_text = data.decode(charset, errors="replace")
        else:
            page_text = trafilatura.extract(data, include_comments=False) or ""
        if not page_text.strip():
            raise ValueError("No readable text found; the page may require JavaScript or a login")
        return json.dumps({"url": source_url, "text": page_text[:max_chars],
                           "truncated": len(page_text) > max_chars}, ensure_ascii=False)
    except ValueError as exc:
        return json.dumps({"error": str(exc)})
    except Exception:
        logger.exception("Web page retrieval failed")
        return json.dumps({"error": "Could not retrieve the page; it may be unavailable or block automated access"})

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

ROOT = Path(__file__).parent
WORKSPACE = ROOT / "workspace"
MEMORY_FILE = ROOT / "memory.md"

def list_files() -> str:
    return "\n".join(p.name for p in WORKSPACE.iterdir()) or "(empty)"


def read_file(filename: str) -> str:
    path = WORKSPACE / filename
    return (
        path.read_text(encoding="utf-8") if path.is_file() else f"error: no {filename}"
    )


def write_file(filename: str, content: str) -> str:
    (WORKSPACE / filename).write_text(content, encoding="utf-8")
    return f"wrote {filename}"


def run_shell_script(
    filename: str, args: list[str] | None = None, timeout: int = 60
) -> str:
    """Run a trusted Bash script; relative paths are based on WORKSPACE."""
    if not isinstance(filename, str) or not filename:
        return "error: filename must be a non-empty string"
    if args is not None and (
        not isinstance(args, list) or not all(isinstance(arg, str) for arg in args)
    ):
        return "error: args must be a list of strings"
    if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout < 1:
        return "error: timeout must be a positive integer"

    try:
        path = (WORKSPACE / filename).resolve()
        if not path.is_file():
            return f"error: no script {filename}"
        result = subprocess.run(
            ["bash", "--", str(path), *(args or [])],
            cwd=WORKSPACE,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"error: script exceeded the {timeout}-second timeout"
    except (OSError, ValueError) as exc:
        return f"error: could not run script: {exc}"

    return json.dumps(
        {"exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr},
        ensure_ascii=False,
    )


if __name__ == "__main__":
    print(fetch_abc_news(limit=10))


def load_memory() -> str:
    if MEMORY_FILE.is_file():
        return MEMORY_FILE.read_text(encoding="utf-8")
    return "(nothing saved yet)"


def save_memory(fact: str) -> str:
    with MEMORY_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- {fact}\n")
    return f"saved: {fact}"
