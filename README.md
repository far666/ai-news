# AI News

這個專案會定期抓取 AI 相關新聞來源，整理成每日與每週報告，並可選擇輸出到終端機或 Line。

## 目的

- 從多個新聞來源抓取 AI 相關文章
- 將文章儲存到日期分類的資料夾
- 每週整理成摘要報告
- 可選擇將週報發送到 Line

## 專案結構

- main.py：整合抓取、分析與發送的主流程
- main_fetch.py：每日抓取流程入口
- main_analyze.py：每週分析流程入口
- main_send.py：發送最新週報入口
- sources.yaml：新聞來源設定
- data/：每日抓取結果儲存資料夾
- weekly_reports/：產生的週報輸出
- logs/：執行日誌

## 需求

請先安裝 Python 依賴：

```bash
pip install -r requirements.txt
```

## 環境變數

這個專案需要以下環境變數：

- ANTHROPIC_API_KEY：Claude API 使用所需的金鑰
- LINE_ACCESS_TOKEN：若要發送 Line 訊息，需設定此環境變數
- LINE_USER_ID：選填，設定時只發給該使用者（push），未設定則群發給所有好友（broadcast）

你可以在專案根目錄建立 .env 檔，內容如下：

```env
ANTHROPIC_API_KEY=your_anthropic_key
LINE_ACCESS_TOKEN=your_line_access_token
LINE_USER_ID=your_line_user_id
```

## 如何執行

### 1. 每日抓取新聞

```bash
python main_fetch.py
```

預設抓取「前一天 00:00 UTC」到「現在」發布的文章，可用 `--start` / `--end`（ISO 8601）指定區間：

```bash
python main_fetch.py --start 2026-07-19T00:00:00+00:00 --end 2026-07-20T00:00:00+00:00
```

### 2. 每週分析週報

```bash
python main_analyze.py
```

### 3. 發送最新週報到 Line

```bash
python main_send.py
```

週報超過 LINE 單則 5000 字上限時會自動分段發送。

### 4. 執行完整流程

```bash
python main.py
```

## 注意事項

- 新增或修改新聞來源時，請更新 [sources.yaml](sources.yaml)
- 週報分析使用的 Claude model 設定在 [analyzer.py](analyzer.py) 的 `DEFAULT_MODEL`
- 生成的資料、週報與日誌會被忽略，不會直接提交到 Git
