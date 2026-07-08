"""定義所有 fetcher 必須遵守的介面。

新增一種來源類型（例如網頁爬蟲、API）時，繼承 BaseFetcher 並實作 fetch()。
"""

from abc import ABC, abstractmethod

from models import Article


class BaseFetcher(ABC):
    """所有 fetcher 的基礎介面。

    每個 fetcher 對應 sources.yaml 中的一筆來源設定，
    負責從該來源抓取文章並回傳清洗過的 Article 清單。
    """

    def __init__(self, name: str, url: str):
        """初始化 fetcher。

        Args:
            name: 來源名稱，對應 sources.yaml 的 name 欄位。
            url: 來源網址。
        """
        self.name = name
        self.url = url

    @abstractmethod
    def fetch(self) -> list[Article]:
        """抓取該來源的文章。

        實作時務必在回傳前呼叫 utils/cleaner.py 清洗 content，
        確保回傳的 Article.content 是不含 HTML tag 的乾淨純文字。

        Returns:
            清洗過後的 Article 清單。
        """
        raise NotImplementedError
