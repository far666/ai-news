"""每週執行進入點。

明確計算「週一到週日」的固定日期範圍（不使用「最近 7 個資料夾」這種
相對邏輯，避免漏跑某天時範圍跑掉），讀取對應資料夾內容，
彙整後呼叫 Claude API 做摘要分析，最後透過輸出層輸出結果。
"""

import logging
from datetime import date


def setup_logging(day: date) -> None:
    """設定 logging，log 檔依日期命名存到 logs/ 資料夾。

    Args:
        day: 執行日期，決定 log 檔名。
    """
    raise NotImplementedError


def get_week_range(today: date) -> tuple[date, date]:
    """計算 today 所在週的週一與週日日期。

    Args:
        today: 基準日期。

    Returns:
        (週一日期, 週日日期) 的 tuple。
    """
    raise NotImplementedError


def run() -> None:
    """執行每週分析流程。

    流程：
        1. setup_logging()。
        2. get_week_range() 算出本週週一到週日的日期範圍。
        3. 呼叫 analyzer.collect_week_articles() 讀取該範圍內所有文章。
        4. 呼叫 analyzer.analyze() 呼叫 Claude API 做摘要分析。
        5. 透過 output 層（例如 ConsoleOutput）輸出摘要結果。
    """
    raise NotImplementedError


if __name__ == "__main__":
    run()
