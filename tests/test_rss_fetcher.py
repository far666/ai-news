"""fetchers/rss_fetcher.py 的測試。"""

from datetime import datetime, timezone

import pytest

from fetchers.rss_fetcher import RSSFetcher


class FakeFeed(dict):
    """模擬 feedparser.parse() 的回傳值。"""

    def __init__(self, entries, bozo=False):
        super().__init__()
        self.entries = entries
        self.bozo = bozo


def make_entry(
    title="title",
    link="https://example.com/a",
    summary="<p>summary</p>",
    content=None,
    published=(2026, 1, 2, 0, 0, 0),
    updated=None,
):
    entry = {"title": title, "link": link, "summary": summary}
    if content is not None:
        entry["content"] = [{"value": content}]
    if published is not None:
        entry["published_parsed"] = published
    if updated is not None:
        entry["updated_parsed"] = updated
    return entry


@pytest.fixture
def fetcher():
    return RSSFetcher(name="openai_blog", url="https://example.com/rss.xml")


def test_fetch_keeps_entries_within_range(monkeypatch, fetcher):
    in_range = make_entry(title="in range", published=(2026, 1, 2, 0, 0, 0))
    before_range = make_entry(title="too old", published=(2026, 1, 1, 0, 0, 0))
    after_range = make_entry(title="too new", published=(2026, 1, 4, 0, 0, 0))
    monkeypatch.setattr(
        "fetchers.rss_fetcher.feedparser.parse",
        lambda url: FakeFeed([in_range, before_range, after_range]),
    )

    start = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    end = datetime(2026, 1, 3, 0, 0, 0, tzinfo=timezone.utc)
    articles = fetcher.fetch(start=start, end=end)

    assert [a.title for a in articles] == ["in range"]


def test_fetch_range_boundaries_are_inclusive(monkeypatch, fetcher):
    start = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    end = datetime(2026, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
    at_start = make_entry(title="at start", published=(2026, 1, 1, 0, 0, 0))
    at_end = make_entry(title="at end", published=(2026, 1, 2, 0, 0, 0))
    monkeypatch.setattr(
        "fetchers.rss_fetcher.feedparser.parse",
        lambda url: FakeFeed([at_start, at_end]),
    )

    articles = fetcher.fetch(start=start, end=end)

    assert {a.title for a in articles} == {"at start", "at end"}


def test_fetch_skips_entry_missing_published_at(monkeypatch, fetcher, caplog):
    missing = make_entry(title="missing date", published=None, updated=None)
    ok = make_entry(title="has date", published=(2026, 1, 2, 0, 0, 0))
    monkeypatch.setattr(
        "fetchers.rss_fetcher.feedparser.parse",
        lambda url: FakeFeed([missing, ok]),
    )

    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 3, tzinfo=timezone.utc)
    with caplog.at_level("WARNING"):
        articles = fetcher.fetch(start=start, end=end)

    assert [a.title for a in articles] == ["has date"]
    assert "缺少發布時間" in caplog.text


def test_fetch_cleans_html_content(monkeypatch, fetcher):
    entry = make_entry(summary="<p>Hello   <b>World</b></p>")
    monkeypatch.setattr(
        "fetchers.rss_fetcher.feedparser.parse", lambda url: FakeFeed([entry])
    )

    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 3, tzinfo=timezone.utc)
    articles = fetcher.fetch(start=start, end=end)

    assert articles[0].content == "Hello World"


def test_fetch_prefers_content_over_summary(monkeypatch, fetcher):
    entry = make_entry(summary="<p>summary text</p>", content="<p>full content</p>")
    monkeypatch.setattr(
        "fetchers.rss_fetcher.feedparser.parse", lambda url: FakeFeed([entry])
    )

    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 3, tzinfo=timezone.utc)
    articles = fetcher.fetch(start=start, end=end)

    assert articles[0].content == "full content"


def test_fetch_raises_when_feed_unparseable(monkeypatch, fetcher):
    monkeypatch.setattr(
        "fetchers.rss_fetcher.feedparser.parse", lambda url: FakeFeed([], bozo=True)
    )

    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 3, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        fetcher.fetch(start=start, end=end)
