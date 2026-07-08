"""資料模型定義。

所有 fetcher 回傳的文章都必須符合 Article 這個 pydantic model，
確保後續清洗、儲存、分析流程拿到的資料格式一致。
"""

from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    """代表一篇抓取到的文章。

    Attributes:
        title: 文章標題。
        url: 文章原始連結。
        content: 清洗過後的純文字內容（不含 HTML tag）。
        published_at: 文章發布時間。
        source: 來源名稱，對應 sources.yaml 中的 name 欄位。
    """

    title: str
    url: str
    content: str
    published_at: datetime
    source: str
