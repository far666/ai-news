"""定義輸出管道的介面。

之後若要擴充 Email、Telegram 等其他輸出管道，
只需要繼承 BaseOutput 並實作 send()。
"""

from abc import ABC, abstractmethod


class BaseOutput(ABC):
    """所有輸出管道的基礎介面。"""

    @abstractmethod
    def send(self, content: str) -> None:
        """把摘要內容輸出出去。

        Args:
            content: 要輸出的摘要文字內容（例如 Claude 產生的週摘要）。
        """
        raise NotImplementedError
