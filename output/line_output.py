"""將週報摘要透過 LINE Messaging API 發送。"""

import logging
import os
from datetime import date

from dotenv import load_dotenv

from output.base import BaseOutput
from output.line_sender import LineSender

load_dotenv()

logger = logging.getLogger(__name__)


class LineOutput(BaseOutput):
    """使用 LINE Messaging API 發送週報摘要。"""

    def __init__(self, user_id: str | None = None, access_token: str | None = None):
        self.user_id = user_id or os.getenv("LINE_USER_ID")
        self.access_token = access_token or os.getenv("LINE_ACCESS_TOKEN")
        self.sender = LineSender(self.access_token) if self.access_token else None

    def send(self, content: str, monday: date | None = None, sunday: date | None = None) -> None:
        """把摘要送到指定的 LINE user；若未指定 user_id，則使用群發。"""
        if not self.access_token:
            raise ValueError("LINE_ACCESS_TOKEN 必須先設定")

        if monday is not None and sunday is not None:
            header = f"週報摘要 ({monday.isoformat()} ~ {sunday.isoformat()})"
        else:
            header = "週報摘要"
        message = f"{header}\n\n{content}"

        if self.user_id:
            logger.info("LINE 單發訊息給 %s", self.user_id)
            self.sender.send_text(message, user_id=self.user_id)
        else:
            logger.info("LINE 群發訊息")
            self.sender.send_text(message)
