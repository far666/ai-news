# 開發計畫

## 現況

**每日流程（main_fetch.py）：已完成**
- `fetchers/rss_fetcher.py`、`fetchers/base.py`：已實作，有測試（`tests/test_rss_fetcher.py`）
- `storage/daily_store.py`：`save_articles()` 已實作
- `main_fetch.py`：`run()` 已實作（讀 sources.yaml → 逐一 fetch → try/except 包錯 → 存檔 → log 總結）

**每週流程（main_analyze.py）：尚未實作，全是 stub（`raise NotImplementedError`）**
- `storage/daily_store.py`：`load_articles()`、`load_all_articles_for_day()`
- `analyzer.py`：`collect_week_articles()`、`build_prompt()`、`analyze()`
- `main_analyze.py`：`setup_logging()`、`get_week_range()`、`run()`
- `output/console_output.py`：`send()`

## 待完成項目（依相依順序）

1. **`storage/daily_store.py`**
   - `load_articles(source_name, day)`：讀 `data/YYYY-MM-DD/{source_name}.json`，檔案不存在回傳 `[]`
   - `load_all_articles_for_day(day)`：掃該日資料夾下所有 json 檔，彙整成一份 Article 清單
   - 驗證：補單元測試，覆蓋「檔案存在／不存在」「資料夾內多個來源」情境

2. **`analyzer.py`**
   - `collect_week_articles(monday, sunday)`：迴圈呼叫 `load_all_articles_for_day()` 收集週一到週日
   - `build_prompt(articles)`：組出送給 Claude 的 prompt（文章數量、格式待確認，見下方待確認事項）
   - `analyze(articles)`：呼叫 Anthropic API（用 `.env` 的 `ANTHROPIC_API_KEY`），回傳摘要文字
   - 驗證：`build_prompt` 可用固定輸入做 snapshot 測試；`analyze` 用 mock 掉 API call 測試

3. **`main_analyze.py`**
   - `setup_logging(day)`：仿照 `main_fetch.py` 的 logging 設定
   - `get_week_range(today)`：回傳 `(週一日期, 週日日期)`，注意是「今天所在週」還是「上一週」（待確認）
   - `run()`：串起 setup_logging → get_week_range → collect_week_articles → analyze → output
   - 驗證：`get_week_range` 用多個不同 weekday 的 `today` 做單元測試

4. **`output/console_output.py`**
   - `send(content)`：印到 console，並存成 markdown 檔（存放路徑待確認，例如 `output/` 或 `data/`）
   - 驗證：跑一次確認檔案有產生、內容正確

## 待確認事項（實作前需要跟你對齊）

- `get_week_range()` 抓的是「執行當下這週」還是「上一週」？（週分析通常是分析已結束的一週）
- 週摘要 markdown 檔案要存在哪裡？檔名格式？
- `analyzer.analyze()` 要用哪個 Claude model、prompt 大致要包含哪些欄位（標題/來源/內容全文或摘錄）？

## 驗收標準

- `pytest` 全數通過，新增功能都有對應測試
- `python main_analyze.py` 可在有 `data/` 歷史資料的情況下跑完，產出週摘要 markdown
- 單一來源或單一天資料缺失不會讓整個流程中斷
