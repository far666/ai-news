"""RSS 來源的 fetcher 實作。

對應 sources.yaml 中 type: rss 的來源，使用 feedparser 解析 RSS feed。
"""

from datetime import datetime, timezone

import feedparser

from fetchers.base import BaseFetcher
from models import Article
from utils.cleaner import clean_html


class RSSFetcher(BaseFetcher):
    """從 RSS feed 抓取文章。"""

    def fetch(self) -> list[Article]:
        """解析 self.url 的 RSS feed 並回傳文章清單。

        Returns:
            清洗過後的 Article 清單。

        Raises:
            ValueError: RSS feed 解析失敗且沒有任何可用的 entry 時。
        """
        feed = feedparser.parse(self.url)

        if feed.bozo and not feed.entries:
            raise ValueError(f"無法解析 RSS feed: {self.url}") from feed.get("bozo_exception")

        articles = []
        for entry in feed.entries:
            raw_content = self._extract_raw_content(entry)
            articles.append(
                Article(
                    title=entry.get("title", ""),
                    url=entry.get("link", ""),
                    content=clean_html(raw_content),
                    published_at=self._parse_published_at(entry),
                    source=self.name,
                )
            )

        return articles

    @staticmethod
    def _extract_raw_content(entry: feedparser.FeedParserDict) -> str:
        """從 feed entry 取出原始（未清洗）內容，優先用 content，其次 summary。

        Args:
            entry: feedparser 解析出的單筆 entry。

        Returns:
            原始（可能含 HTML tag）的內容字串。
        """
        if entry.get("content"):
            return entry["content"][0].get("value", "")
        return entry.get("summary", "")

    @staticmethod
    def _parse_published_at(entry: feedparser.FeedParserDict) -> datetime:
        """從 entry 取出發布時間，找不到時 fallback 為目前時間（UTC）。

        Args:
            entry: feedparser 解析出的單筆 entry。

        Returns:
            文章發布時間（UTC）。
        """
        time_struct = entry.get("published_parsed") or entry.get("updated_parsed")
        if time_struct is None:
            return datetime.now(timezone.utc)
        return datetime(*time_struct[:6], tzinfo=timezone.utc)
