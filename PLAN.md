# 開發計畫

## 現況

**每日流程（main_fetch.py）：已完成**
- `fetchers/rss_fetcher.py`（type: rss）、`fetchers/html_scrape_fetcher.py`（type: html_scrape）、`fetchers/base.py`：已實作，有測試
- `storage/daily_store.py`：`save_articles()`、`load_articles()`、`load_all_articles_for_day()` 已實作
- `main_fetch.py`：`run()` 已實作（讀 sources.yaml → 逐一 fetch → try/except 包錯 → 存檔 → log 總結），支援 `--start` / `--end`

**每週流程（main_analyze.py）：已完成**
- `analyzer.py`：`collect_week_articles()`、`build_prompt()`、`analyze()`（呼叫 Claude API，model 見 `DEFAULT_MODEL`）
- `main_analyze.py`：`get_date_range()` 取「今天往前推 7 天」到「今天」，`run()` 串起分析流程
- `output/console_output.py`：印到 console，並存成 `weekly_reports/{開始日}_{結束日}.md`

**發送流程（main_send.py）：已完成**
- `output/line_output.py`、`output/line_sender.py`：透過 LINE Messaging API 發送最新週報
  - 有設 `LINE_USER_ID` 時單發（push），否則群發（broadcast）
  - 超過 5000 字自動分段，每次請求最多 5 段

**整合流程（main.py）**：依序執行抓取（7 天範圍）→ 分析 → 發送

## 已知限制

- `html_scrape` 來源目前只抓列表頁，`content` 只有標題，沒有文章內文；連結前綴寫死為 `https://www.anthropic.com`
- 同一篇文章可能被不同天的抓取重複存檔，週分析時不去重（預期行為）

## 驗收標準

- `pytest` 全數通過，新增功能都有對應測試
- 單一來源或單一天資料缺失不會讓整個流程中斷
