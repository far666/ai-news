"""輸出到 console 與 markdown 檔案的實作。

初版輸出管道，之後若要接 Email/Telegram 等，另外實作 BaseOutput 即可。
"""

from datetime import date
from pathlib import Path

from output.base import BaseOutput

# 週摘要 markdown 存放資料夾，內容為產生物，不進版控（見 .gitignore）。
WEEKLY_REPORTS_DIR = Path("weekly_reports")


class ConsoleOutput(BaseOutput):
    """把摘要內容印到 console，並存成一份 markdown 檔案。"""

    def send(self, content: str, monday: date | None = None, sunday: date | None = None) -> None:
        """印出摘要內容到 console，同時存成 markdown 檔案。

        Args:
            content: 要輸出的摘要文字內容。
            monday: 該週摘要對應的週一日期，若無則使用預設檔名。
            sunday: 該週摘要對應的週日日期，若無則使用預設檔名。
        """
        print(content)

        WEEKLY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        if monday is not None and sunday is not None:
            file_path = WEEKLY_REPORTS_DIR / f"{monday.isoformat()}_{sunday.isoformat()}.md"
        else:
            file_path = WEEKLY_REPORTS_DIR / "latest.md"
        file_path.write_text(content, encoding="utf-8")
