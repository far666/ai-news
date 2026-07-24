"""每日資料儲存。

負責把 main_fetch.py 當日抓到的 Article 存進 data/YYYY-MM-DD/ 資料夾，
每個來源存成一個檔案。
"""

import json
from datetime import date
from pathlib import Path

from models import Article

DATA_DIR = Path("data")


def save_articles(articles: list[Article], source_name: str, day: date) -> None:
    """把單一來源當日抓到的文章存檔。

    存檔路徑為 data/YYYY-MM-DD/{source_name}.json（或其他決定的格式）。

    Args:
        articles: 該來源抓到的文章清單。
        source_name: 來源名稱，對應 sources.yaml 的 name 欄位。
        day: 抓取日期，決定存進哪個 data/YYYY-MM-DD/ 資料夾。
    """
    day_dir = DATA_DIR / day.isoformat()
    day_dir.mkdir(parents=True, exist_ok=True)

    file_path = day_dir / f"{source_name}.json"
    payload = [json.loads(article.model_dump_json()) for article in articles]
    file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_articles(source_name: str, day: date) -> list[Article]:
    """讀取指定來源、指定日期已存檔的文章。

    給 main_analyze.py 彙整一週資料時使用。

    Args:
        source_name: 來源名稱。
        day: 要讀取的日期。

    Returns:
        該來源當天存檔的 Article 清單，若檔案不存在則回傳空清單。
    """
    file_path = DATA_DIR / day.isoformat() / f"{source_name}.json"
    if not file_path.exists():
        return []

    payload = json.loads(file_path.read_text(encoding="utf-8"))
    return [Article.model_validate(item) for item in payload]


def load_all_articles_for_day(day: date) -> list[Article]:
    """讀取指定日期資料夾內所有來源的文章。

    Args:
        day: 要讀取的日期。

    Returns:
        當天所有來源的 Article 清單。
    """
    day_dir = DATA_DIR / day.isoformat()
    if not day_dir.exists():
        return []

    articles = []
    for file_path in sorted(day_dir.glob("*.json")):
        payload = json.loads(file_path.read_text(encoding="utf-8"))
        articles.extend(Article.model_validate(item) for item in payload)
    return articles
