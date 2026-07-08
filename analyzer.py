"""週摘要分析。

讀取一週（週一到週日）份的 data/YYYY-MM-DD/ 資料夾內容，
組成 prompt 呼叫 Claude API 做摘要分析。
"""

from datetime import date

from models import Article


def collect_week_articles(monday: date, sunday: date) -> list[Article]:
    """讀取週一到週日範圍內所有資料夾的文章。

    Args:
        monday: 該週的週一日期。
        sunday: 該週的週日日期。

    Returns:
        該週範圍內所有來源的 Article 清單。
    """
    raise NotImplementedError


def build_prompt(articles: list[Article]) -> str:
    """把文章清單組成要送給 Claude API 的 prompt。

    Args:
        articles: 該週收集到的文章清單。

    Returns:
        組好的 prompt 字串。
    """
    raise NotImplementedError


def analyze(articles: list[Article]) -> str:
    """呼叫 Claude API 對文章清單做摘要分析。

    Args:
        articles: 該週收集到的文章清單。

    Returns:
        Claude API 回傳的摘要文字內容。
    """
    raise NotImplementedError
