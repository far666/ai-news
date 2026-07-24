"""實際測試 LINE 發送。"""

import os

from dotenv import load_dotenv

from output.line_sender import LineSender

load_dotenv()


if __name__ == "__main__":
    access_token = os.getenv("LINE_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")

    if not access_token:
        raise SystemExit("請先設定 LINE_ACCESS_TOKEN")

    sender = LineSender(access_token)
    sender.send_text("這是一則 LINE 實測訊息", user_id=user_id)
    print("已嘗試發送 LINE 訊息")
