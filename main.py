"""整合抓取、分析與發送的主流程入口。"""

import logging
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

import main_analyze
import main_fetch
import main_send

load_dotenv()

LOGS_DIR = "logs"

logger = logging.getLogger(__name__)


def setup_logging(day: date) -> None:
    """設定主要 log 檔。"""
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

def run() -> None:
    """依序執行抓取、分析與發送。"""
    setup_logging(date.today())
    logger.info("開始執行整體流程")

    today = date.today()
    start = datetime.combine(today - timedelta(days=7), time.min, tzinfo=timezone.utc)
    end = datetime.combine(today, time.max, tzinfo=timezone.utc)

    logger.info("步驟 1: 抓取最新新聞（%s ~ %s）", start.isoformat(), end.isoformat())
    main_fetch.run(start=start, end=end)

    logger.info("步驟 2: 生成週報摘要")
    main_analyze.run()

    logger.info("步驟 3: 發送最新週報")
    main_send.send_latest_report()

    logger.info("整體流程完成")


if __name__ == "__main__":
    run()
