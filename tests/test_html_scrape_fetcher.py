from datetime import datetime, timezone

import pytest

from fetchers.html_scrape_fetcher import HTMLScrapeFetcher


class FakeResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code


@pytest.fixture
def fetcher():
    return HTMLScrapeFetcher(name="anthropic_news", url="https://www.anthropic.com/news")


def test_fetch_parses_recent_news_items(monkeypatch, fetcher):
    html = """
    <html><body>
      <main>
        <ul>
          <li>
            <a href="/news/claude-sonnet-5">
              <span class="date">Jul 22, 2026</span>
              <span class="tag">Product</span>
              <h2>Claude Sonnet 5</h2>
            </a>
          </li>
        </ul>
      </main>
    </body></html>
    """
    monkeypatch.setattr(
        "fetchers.html_scrape_fetcher.httpx.get",
        lambda *args, **kwargs: FakeResponse(html),
    )

    start = datetime(2026, 7, 21, tzinfo=timezone.utc)
    end = datetime(2026, 7, 24, tzinfo=timezone.utc)
    articles = fetcher.fetch(start=start, end=end)

    assert len(articles) == 1
    article = articles[0]
    assert article.title == "Claude Sonnet 5"
    assert article.url == "https://www.anthropic.com/news/claude-sonnet-5"
    assert article.content == "Claude Sonnet 5"
    assert article.source == "anthropic_news"
    assert article.published_at == datetime(2026, 7, 22, tzinfo=timezone.utc)


def test_fetch_returns_empty_when_no_recent_items(monkeypatch, fetcher):
    html = """
    <html><body>
      <main>
        <ul>
          <li><a href="/news/old-post"><span class="date">Jul 10, 2026</span><h2>Old post</h2></a></li>
        </ul>
      </main>
    </body></html>
    """
    monkeypatch.setattr(
        "fetchers.html_scrape_fetcher.httpx.get",
        lambda *args, **kwargs: FakeResponse(html),
    )

    start = datetime(2026, 7, 21, tzinfo=timezone.utc)
    end = datetime(2026, 7, 24, tzinfo=timezone.utc)
    articles = fetcher.fetch(start=start, end=end)

    assert articles == []


def test_fetch_logs_and_returns_empty_when_structure_missing(monkeypatch, fetcher, caplog):
    html = "<html><body><nav><a href='/'>Home</a></nav></body></html>"
    monkeypatch.setattr(
        "fetchers.html_scrape_fetcher.httpx.get",
        lambda *args, **kwargs: FakeResponse(html),
    )

    start = datetime(2026, 7, 21, tzinfo=timezone.utc)
    end = datetime(2026, 7, 24, tzinfo=timezone.utc)
    with caplog.at_level("ERROR"):
        articles = fetcher.fetch(start=start, end=end)

    assert articles == []
    assert "找不到新聞列表區塊" in caplog.text
