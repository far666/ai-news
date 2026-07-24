"""每日執行進入點。

只做「讀取 sources.yaml -> 逐一呼叫對應 fetcher 抓取 -> 清洗 -> 存檔」，
不呼叫 LLM。單一來源失敗要 try/except 包起來，記錄 log 並跳過，
不能讓整體流程中斷。
"""

import argparse
import logging
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

import yaml

from fetchers.html_scrape_fetcher import HTMLScrapeFetcher
from fetchers.rss_fetcher import RSSFetcher
from storage.daily_store import save_articles

FETCHER_REGISTRY = {
    "rss": RSSFetcher,
    "html_scrape": HTMLScrapeFetcher,
}

LOGS_DIR = Path("logs")

logger = logging.getLogger(__name__)


def setup_logging(day: date) -> None:
    """設定 logging，log 檔依日期命名存到 logs/ 資料夾。

    Args:
        day: 執行日期，決定 log 檔名。
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"{day.isoformat()}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def load_sources(config_path: str = "sources.yaml") -> list[dict]:
    """讀取 sources.yaml 設定檔。

    Args:
        config_path: 設定檔路徑。

    Returns:
        來源設定清單，每筆為 dict（包含 name / type / url）。
    """
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("sources", [])


def parse_args() -> argparse.Namespace:
    """解析命令列參數。

    --start / --end 為 ISO 8601 格式時間字串（例如 2026-07-19T00:00:00+00:00）。
    未指定時使用預設值：前一天 00:00（UTC）到當前時間。

    Returns:
        解析後的參數，start/end 欄位可能為 None（表示使用預設值）。
    """
    parser = argparse.ArgumentParser(description="每日抓取 AI 新聞來源")
    parser.add_argument("--start", type=datetime.fromisoformat, default=None, help="抓取區間起始時間（ISO 8601），預設為前一天 00:00 UTC")
    parser.add_argument("--end", type=datetime.fromisoformat, default=None, help="抓取區間結束時間（ISO 8601），預設為當前時間")
    return parser.parse_args()


def run(start: datetime | None = None, end: datetime | None = None) -> None:
    """執行每日抓取流程。

    流程：
        1. setup_logging()。
        2. load_sources() 讀取所有來源設定。
        3. 逐一依 type 找到對應 fetcher，呼叫 fetch()。
           單一來源失敗時用 try/except 包起來，記錄 log 後跳過，
           不中斷整體流程。
        4. 呼叫 storage/daily_store.save_articles() 存檔。
        5. 記錄本次執行總結（成功/失敗來源、抓到篇數）到 log。
    """
    today = date.today()
    setup_logging(today)

    sources = load_sources()

    args = parse_args()
    end = end or args.end or datetime.now(timezone.utc)
    start = start or args.start or datetime.combine(end.date() - timedelta(days=1), time.min, tzinfo=timezone.utc)

    succeeded = 0
    failed = 0
    total_articles = 0

    for source in sources:
        name = source["name"]
        source_type = source["type"]
        url = source["url"]

        fetcher_cls = FETCHER_REGISTRY.get(source_type)
        if fetcher_cls is None:
            logger.error("[%s] 不支援的來源類型: %s，跳過", name, source_type)
            failed += 1
            continue

        try:
            articles = fetcher_cls(name=name, url=url).fetch(start=start, end=end)
        except Exception:
            logger.exception("[%s] 抓取失敗，跳過", name)
            failed += 1
            continue

        succeeded += 1
        total_articles += len(articles)

        if not articles:
            logger.info("[%s] 本次抓到 0 篇，略過存檔", name)
            continue

        save_articles(articles, name, today)
        logger.info("[%s] 抓到 %d 篇，已存檔", name, len(articles))

    logger.info(
        "執行完畢：成功 %d 個來源、失敗 %d 個來源，共抓到 %d 篇文章",
        succeeded,
        failed,
        total_articles,
    )


if __name__ == "__main__":
    run()
