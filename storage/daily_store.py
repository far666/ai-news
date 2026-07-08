"""每日資料儲存。

負責把 main_fetch.py 當日抓到的 Article 存進 data/YYYY-MM-DD/ 資料夾，
每個來源存成一個檔案。
"""

from datetime import date

from models import Article


def save_articles(articles: list[Article], source_name: str, day: date) -> None:
    """把單一來源當日抓到的文章存檔。

    存檔路徑為 data/YYYY-MM-DD/{source_name}.json（或其他決定的格式）。

    Args:
        articles: 該來源抓到的文章清單。
        source_name: 來源名稱，對應 sources.yaml 的 name 欄位。
        day: 抓取日期，決定存進哪個 data/YYYY-MM-DD/ 資料夾。
    """
    raise NotImplementedError


def load_articles(source_name: str, day: date) -> list[Article]:
    """讀取指定來源、指定日期已存檔的文章。

    給 main_analyze.py 彙整一週資料時使用。

    Args:
        source_name: 來源名稱。
        day: 要讀取的日期。

    Returns:
        該來源當天存檔的 Article 清單，若檔案不存在則回傳空清單。
    """
    raise NotImplementedError


def load_all_articles_for_day(day: date) -> list[Article]:
    """讀取指定日期資料夾內所有來源的文章。

    Args:
        day: 要讀取的日期。

    Returns:
        當天所有來源的 Article 清單。
    """
    raise NotImplementedError
