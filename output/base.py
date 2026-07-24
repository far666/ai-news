"""定義輸出管道的介面。

之後若要擴充 Email、Telegram 等其他輸出管道，
只需要繼承 BaseOutput 並實作 send()。
"""

from abc import ABC, abstractmethod
from datetime import date


class BaseOutput(ABC):
    """所有輸出管道的基礎介面。"""

    @abstractmethod
    def send(self, content: str, monday: date | None = None, sunday: date | None = None) -> None:
        """把摘要內容輸出出去。

        Args:
            content: 要輸出的摘要文字內容（例如 Claude 產生的週摘要）。
            monday: 該週摘要對應的週一日期，若無則可為 None。
            sunday: 該週摘要對應的週日日期，若無則可為 None。
        """
        raise NotImplementedError
