"""獨立發送週報摘要的入口。"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from output.line_output import LineOutput

load_dotenv()

logger = logging.getLogger(__name__)

WEEKLY_REPORTS_DIR = Path("weekly_reports")


def load_latest_report(reports_dir: Path | None = None) -> tuple[Path, str]:
    """讀取最新產生的週報 markdown 檔。"""
    reports_dir = reports_dir or WEEKLY_REPORTS_DIR
    reports_dir.mkdir(parents=True, exist_ok=True)

    report_files = sorted(reports_dir.glob("*.md"))
    if not report_files:
        raise FileNotFoundError("沒有找到任何週報檔案")

    latest_file = max(report_files, key=lambda path: path.name)
    return latest_file, latest_file.read_text(encoding="utf-8")


def send_latest_report() -> None:
    """讀取最新週報並透過 Line 發送。"""
    report_path, content = load_latest_report()
    logger.info("準備發送週報：%s", report_path)

    if not os.getenv("LINE_ACCESS_TOKEN"):
        raise ValueError("LINE_ACCESS_TOKEN 必須先設定")

    LineOutput().send(content)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    send_latest_report()
