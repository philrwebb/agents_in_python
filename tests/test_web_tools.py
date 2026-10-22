import asyncio
import json
from email.message import Message
from unittest.mock import MagicMock

import pytest

import harness
import tools


@pytest.fixture
def page(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    response = MagicMock()
    response.headers = Message()
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.read.return_value = b'Useful source text'
    response.geturl.return_value = 'https://example.com/final'
    opener = MagicMock()
    opener.return_value.__enter__.return_value = response
    monkeypatch.setattr(tools, 'urlopen', opener)
    return response


def test_page_text_and_truncation(page: MagicMock) -> None:
    result = json.loads(tools.browse_web('https://example.com', max_chars=6))
    assert result == {'url': 'https://example.com/final', 'text': 'Useful', 'truncated': True}
    page.read.assert_called_once_with(tools.MAX_PAGE_BYTES + 1)


@pytest.mark.parametrize('url', ['file:///etc/passwd', 'ftp://example.com', '', 'https://user:pass@example.com'])
def test_invalid_urls(url: str) -> None:
    assert 'error' in json.loads(tools.browse_web(url))


def test_size_and_content_limits(page: MagicMock) -> None:
    page.read.return_value = b'x' * (tools.MAX_PAGE_BYTES + 1)
    assert 'error' in json.loads(tools.browse_web('https://example.com'))
    page.headers.replace_header('Content-Type', 'application/pdf')
    assert 'error' in json.loads(tools.browse_web('https://example.com'))


def test_html_extraction(page: MagicMock) -> None:
    page.headers.replace_header('Content-Type', 'text/html')
    page.read.return_value = b'<html><body><article><h1>Source</h1><p>This is useful text from a remote article for the assistant to read.</p></article></body></html>'
    result = json.loads(tools.browse_web('https://example.com'))
    assert 'useful text' in result['text']
    assert '<p>' not in result['text']


def test_search_results(monkeypatch: pytest.MonkeyPatch) -> None:
    search = MagicMock()
    search.return_value.text.return_value = [{'title': 'Source', 'href': 'https://example.com', 'body': 'Summary'}]
    monkeypatch.setattr(tools, 'DDGS', search)
    assert json.loads(tools.search_web('question'))['results'][0]['url'] == 'https://example.com'
    search.return_value.text.assert_called_once_with('question', max_results=5)
    search.return_value.text.side_effect = RuntimeError('offline')
    assert 'error' in json.loads(tools.search_web('question'))


def test_invalid_arguments() -> None:
    assert 'error' in json.loads(tools.search_web(''))
    assert 'error' in json.loads(tools.search_web('question', True))
    assert 'error' in json.loads(tools.browse_web('https://example.com', 0))


def test_schemas_and_dispatch(monkeypatch: pytest.MonkeyPatch) -> None:
    schemas = {schema['function']['name']: schema['function'] for schema in harness.TOOL_SCHEMAS if schema['type'] == 'function'}
    for name, required in [('search_web', 'query'), ('browse_web', 'url')]:
        assert name in harness.LOCAL_TOOLS
        assert schemas[name]['parameters']['required'] == [required] # type: ignore
    monkeypatch.setitem(harness.LOCAL_TOOLS, 'search_web', lambda query: query)
    assert asyncio.run(harness.call_tool('search_web', {'query': 'question'})) == 'question'
    assert 'error' in json.loads(asyncio.run(harness.call_tool('browse_web', {})))


def test_abc_news_schema_and_dispatch(monkeypatch: pytest.MonkeyPatch) -> None:
    schema = next(schema['function'] for schema in harness.TOOL_SCHEMAS
                  if schema['type'] == 'function' and schema['function']['name'] == 'fetch_abc_news')
    assert 'abc.net.au' in schema['description']
    assert schema['parameters']['properties']['limit']['type'] == 'integer'
    fetch = MagicMock(return_value='[{"title": "Latest headline"}]')
    monkeypatch.setitem(harness.LOCAL_TOOLS, 'fetch_abc_news', fetch)
    assert json.loads(asyncio.run(harness.call_tool('fetch_abc_news', {'limit': 10})))[0]['title'] == 'Latest headline'
    fetch.assert_called_once_with(limit=10)
