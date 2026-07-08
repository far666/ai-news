"""輸出到 console 與 markdown 檔案的實作。

初版輸出管道，之後若要接 Email/Telegram 等，另外實作 BaseOutput 即可。
"""

from output.base import BaseOutput


class ConsoleOutput(BaseOutput):
    """把摘要內容印到 console，並存成一份 markdown 檔案。"""

    def send(self, content: str) -> None:
        """印出摘要內容到 console，同時存成 markdown 檔案。

        Args:
            content: 要輸出的摘要文字內容。
        """
        raise NotImplementedError
