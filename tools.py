import json
import subprocess
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

from pathlib import Path
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
