"""內容清洗工具。

所有 fetcher 在回傳 Article 前，都必須用這裡的函式清洗過 content，
確保存進 Article.content 的是不含 HTML tag、沒有多餘空白的純文字。
"""

import re

from bs4 import BeautifulSoup


def clean_html(raw_html: str) -> str:
    """去除 HTML tag 並回傳乾淨純文字。

    使用 BeautifulSoup 解析 raw_html，取出純文字後再清除多餘空白。

    Args:
        raw_html: 原始 HTML 字串。

    Returns:
        不含 HTML tag 的純文字。
    """
    if not raw_html:
        return ""

    soup = BeautifulSoup(raw_html, "lxml")
    text = soup.get_text(separator=" ")
    return normalize_whitespace(text)


def normalize_whitespace(text: str) -> str:
    """去除多餘空白、換行，回傳整理過的純文字。

    Args:
        text: 待整理的文字。

    Returns:
        整理過後的純文字。
    """
    if not text:
        return ""

    return re.sub(r"\s+", " ", text).strip()
