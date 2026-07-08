"""每日執行進入點。

只做「讀取 sources.yaml -> 逐一呼叫對應 fetcher 抓取 -> 清洗 -> 存檔」，
不呼叫 LLM。單一來源失敗要 try/except 包起來，記錄 log 並跳過，
不能讓整體流程中斷。
"""

import logging
from datetime import date

FETCHER_REGISTRY = {
    # type 名稱 -> fetcher class，例如 "rss": RSSFetcher
}


def setup_logging(day: date) -> None:
    """設定 logging，log 檔依日期命名存到 logs/ 資料夾。

    Args:
        day: 執行日期，決定 log 檔名。
    """
    raise NotImplementedError


def load_sources(config_path: str = "sources.yaml") -> list[dict]:
    """讀取 sources.yaml 設定檔。

    Args:
        config_path: 設定檔路徑。

    Returns:
        來源設定清單，每筆為 dict（包含 name / type / url）。
    """
    raise NotImplementedError


def run() -> None:
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
    raise NotImplementedError


if __name__ == "__main__":
    run()
