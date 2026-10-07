"""週摘要分析。

讀取「今天往前推 7 天」到「今天」的 data/YYYY-MM-DD/ 資料夾內容，
組成 prompt 呼叫 Claude API 做摘要分析。
"""

from datetime import date, timedelta

import anthropic

from models import Article
from storage.daily_store import load_all_articles_for_day

# 預設 model，之後要換就改這裡（或呼叫 analyze() 時傳 model 參數覆蓋）。
DEFAULT_MODEL = "claude-sonnet-5-5"

# 基本 prompt 模板，之後要調整分析角度、輸出格式就改這裡
# （或呼叫 build_prompt() 時傳 prompt_template 參數覆蓋）。
DEFAULT_PROMPT_TEMPLATE = """你是一個 AI 產業新聞編輯，請閱讀以下本週蒐集到的文章，整理成一份繁體中文的週報摘要。

文章列表：
{articles_text}

請輸出：
1. 本週重點趨勢（3-5 點）
2. 值得關注的個別新聞摘要
"""


def collect_week_articles(start: date, end: date) -> list[Article]:
    """讀取指定日期範圍內所有資料夾的文章。

    Args:
        start: 範圍開始日期。
        end: 範圍結束日期。

    Returns:
        該範圍內所有來源的 Article 清單。
    """
    articles = []
    day = start
    while day <= end:
        articles.extend(load_all_articles_for_day(day))
        day += timedelta(days=1)
    return articles


def build_prompt(articles: list[Article], prompt_template: str = DEFAULT_PROMPT_TEMPLATE) -> str:
    """把文章清單組成要送給 Claude API 的 prompt。

    Args:
        articles: 該週收集到的文章清單。
        prompt_template: prompt 模板，需含 {articles_text} 佔位字串。

    Returns:
        組好的 prompt 字串。
    """
    articles_text = "\n\n".join(
        f"- [{article.source}] {article.title} ({article.url})\n{article.content}"
        for article in articles
    )
    return prompt_template.format(articles_text=articles_text)


def analyze(articles: list[Article], model: str = DEFAULT_MODEL) -> str:
    """呼叫 Claude API 對文章清單做摘要分析。

    Args:
        articles: 該週收集到的文章清單。
        model: 要使用的 Claude model，預設 DEFAULT_MODEL。

    Returns:
        Claude API 回傳的摘要文字內容。
    """
    prompt = build_prompt(articles)

    client = anthropic.Anthropic()
    # fallbacks="default"：若被安全分類器拒答，API 會自動改用其他 model 重跑。
    message = client.beta.messages.create(
        model=model,
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{"role": "user", "content": prompt}],
    )
    for block in message.content:
        if block.type == "text":
            return block.text
    raise ValueError("Claude API 回應中沒有文字內容")
