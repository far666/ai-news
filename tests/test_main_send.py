from pathlib import Path

from main_send import load_latest_report


def test_load_latest_report_prefers_latest_file(tmp_path):
    reports_dir = tmp_path / "weekly_reports"
    reports_dir.mkdir()
    (reports_dir / "2026-07-10_2026-07-16.md").write_text("old", encoding="utf-8")
    (reports_dir / "2026-07-17_2026-07-24.md").write_text("new", encoding="utf-8")

    report_path, content = load_latest_report(reports_dir)

    assert report_path == reports_dir / "2026-07-17_2026-07-24.md"
    assert content == "new"
