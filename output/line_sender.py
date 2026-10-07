"""LINE Messaging API 的底層發送服務。"""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# LINE 單則文字訊息上限 5000 字。
MAX_TEXT_LENGTH = 5000
# LINE 單次 push / broadcast 請求最多帶 5 則訊息。
MAX_MESSAGES_PER_REQUEST = 5


def split_text(message: str, limit: int = MAX_TEXT_LENGTH) -> list[str]:
    """把長訊息切成每段不超過 limit 字，盡量在換行處切開。"""
    chunks = []
    while len(message) > limit:
        cut = message.rfind("\n", 0, limit + 1)
        if cut <= 0:
            cut = limit
        chunks.append(message[:cut])
        message = message[cut:].lstrip("\n")
    if message:
        chunks.append(message)
    return chunks


class LineSender:
    """負責實際呼叫 LINE Messaging API。"""

    def __init__(self, access_token: str):
        self.access_token = access_token

    def send_text(self, message: str, *, user_id: str | None = None) -> None:
        """發送文字訊息，若 user_id 存在則單發，否則群發。

        超過 5000 字的訊息會分段，每次請求最多帶 5 段。
        """
        endpoint = "https://api.line.me/v2/bot/message/push"
        if not user_id:
            endpoint = "https://api.line.me/v2/bot/message/broadcast"

        chunks = split_text(message)
        for i in range(0, len(chunks), MAX_MESSAGES_PER_REQUEST):
            batch = chunks[i:i + MAX_MESSAGES_PER_REQUEST]
            payload: dict[str, Any] = {"messages": [{"type": "text", "text": text} for text in batch]}
            if user_id:
                payload["to"] = user_id

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
        logger.info("LINE 訊息送出成功，共 %d 段", len(chunks))
