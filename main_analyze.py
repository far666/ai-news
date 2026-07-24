"""每週執行進入點。

計算「今天往前推 7 天」到「今天」的日期範圍，讀取對應資料夾內容，
彙整後呼叫 Claude API 做摘要分析，最後透過輸出層輸出結果。
"""

import logging
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

import analyzer
from output.console_output import ConsoleOutput

load_dotenv()

LOGS_DIR = "logs"

logger = logging.getLogger(__name__)


def setup_logging(day: date) -> None:
    """設定 logging，log 檔依日期命名存到 logs/ 資料夾。

    Args:
        day: 執行日期，決定 log 檔名。
    """
    Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)
    log_file = Path(LOGS_DIR) / f"{day.isoformat()}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def get_date_range(today: date, days: int = 7) -> tuple[date, date]:
    """計算「today 往前推 days 天」到 today 的日期範圍。

    Args:
        today: 執行當下的日期。
        days: 要往前推的天數，預設 7。

    Returns:
        (開始日期, 結束日期) 的 tuple。
    """
    start = today - timedelta(days=days)
    return start, today


def run() -> None:
    """執行每週分析流程。

    流程：
        1. setup_logging()。
        2. get_date_range() 算出往前推 7 天到今天的日期範圍。
        3. 呼叫 analyzer.collect_week_articles() 讀取該範圍內所有文章。
        4. 呼叫 analyzer.analyze() 呼叫 Claude API 做摘要分析。
        5. 透過 output 層（例如 ConsoleOutput / LineOutput）輸出摘要結果。
    """
    today = date.today()
    setup_logging(today)

    start, end = get_date_range(today)
    logger.info("開始分析週報：%s ~ %s", start.isoformat(), end.isoformat())

    articles = analyzer.collect_week_articles(start, end)
    logger.info("共收集到 %d 篇文章", len(articles))

    if len(articles) == 0:
        logger.info("沒有文章可以分析")
    else:
        summary = analyzer.analyze(articles)
        ConsoleOutput().send(summary, start, end)
        logger.info("週報分析完成，已寫入檔案")

if __name__ == "__main__":
    run()
