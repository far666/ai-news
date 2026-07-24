"""LINE Messaging API 的底層發送服務。"""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class LineSender:
    """負責實際呼叫 LINE Messaging API。"""

    def __init__(self, access_token: str):
        self.access_token = access_token

    def send_text(self, message: str, *, user_id: str | None = None) -> None:
        """發送文字訊息，若 user_id 存在則單發，否則群發。"""
        endpoint = "https://api.line.me/v2/bot/message/push"
        payload: dict[str, Any] = {"messages": [{"type": "text", "text": message}]}

        if user_id:
            payload["to"] = user_id
        else:
            endpoint = "https://api.line.me/v2/bot/message/broadcast"

        response = httpx.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        logger.info("LINE 訊息送出成功")
