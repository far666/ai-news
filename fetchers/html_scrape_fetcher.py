"""HTML 網頁爬蟲來源的 fetcher 實作。"""

import logging
import re
from datetime import datetime, timezone
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from fetchers.base import BaseFetcher
from models import Article
from utils.cleaner import clean_html

logger = logging.getLogger(__name__)


class HTMLScrapeFetcher(BaseFetcher):
    """從 HTML 列表頁抓取近期新聞項目。"""

    def fetch(self, start: datetime, end: datetime) -> list[Article]:
        """抓取頁面中的新聞列表，回傳發佈時間介於 [start, end] 之間的文章。"""
        try:
            response = httpx.get(self.url, timeout=10)
            if hasattr(response, "raise_for_status"):
                response.raise_for_status()
        except (httpx.HTTPError, AttributeError) as exc:
            logger.error("[%s] 請求失敗: %s", self.name, exc)
            return []

        soup = BeautifulSoup(response.text, "lxml")
        items = self._find_news_items(soup)
        if items is None:
            logger.error("[%s] 找不到新聞列表區塊，HTML 結構可能已改版: %s", self.name, self.url)
            return []

        articles = []
        for item in items:
            try:
                title = self._extract_title(item)
                url = self._extract_url(item)
                published_at = self._extract_published_at(item)
                logger.info("[%s] 解析新聞項目：標題=%s，連結=%s，發布時間=%s", self.name, title, url, published_at)
            except ValueError as exc:
                logger.warning("[%s] 解析新聞項目失敗: %s", self.name, exc)
                continue

            if published_at is None:
                logger.warning("[%s] 缺少發布時間，跳過：%s", self.name, title or url)
                continue

            if not (start <= published_at <= end):
                logger.info("[%s] 發布時間不在範圍, %s ~ %s 內，跳過：%s", self.name, start.isoformat(), end.isoformat(), title or url)
                continue

            articles.append(
                Article(
                    title=title,
                    url=url,
                    content=clean_html(title),
                    published_at=published_at,
                    source=self.name,
                )
            )

        logger.info("[%s] 解析到 %d 個新聞項目，篩選後 %d 篇", self.name, len(items), len(articles))
        return articles

    def _find_news_items(self, soup: BeautifulSoup):
        """嘗試在頁面中找到新聞列表項目。"""
        news_links = soup.select('a[href^="/news/"]')
        if not news_links:
            return None

        items = []
        for link in news_links:
            text = " ".join(link.get_text(" ", strip=True).split())
            if not text:
                continue
            if re.search(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b", text.lower()):
                items.append(link)
            elif any(keyword in text.lower() for keyword in ["announcements", "product", "case study", "economic research"]):
                items.append(link)

        if not items:
            return None

        return items

    @staticmethod
    def _extract_title(item) -> str:
        heading = item.find(["h1", "h2", "h3", "strong", "b"])
        if heading is not None:
            title = " ".join(heading.get_text(" ", strip=True).split())
            if title:
                return title

        text = " ".join(item.get_text(" ", strip=True).split())
        if text:
            return text
        raise ValueError("找不到標題")

    @staticmethod
    def _extract_url(item) -> str:
        anchor = item.find("a") or item
        href = anchor.get("href") if hasattr(anchor, "get") else None
        if not href:
            raise ValueError("找不到連結")
        return urljoin("https://www.anthropic.com", href)

    @staticmethod
    def _extract_published_at(item) -> datetime | None:
        for candidate in item.find_all(["time", "span", "p", "div"]):
            text = " ".join(candidate.get_text(" ", strip=True).split())
            if not text:
                continue
            if re.fullmatch(r"[A-Za-z]{3}\s+\d{1,2},\s*\d{4}", text):
                try:
                    return datetime.strptime(text, "%b %d, %Y").replace(tzinfo=timezone.utc)
                except ValueError:
                    pass
            if re.fullmatch(r"[A-Za-z]+\s+\d{1,2},\s*\d{4}", text):
                try:
                    return datetime.strptime(text, "%B %d, %Y").replace(tzinfo=timezone.utc)
                except ValueError:
                    pass

        return None
