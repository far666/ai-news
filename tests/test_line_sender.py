from unittest.mock import Mock

import pytest

from output.line_sender import LineSender, split_text


@pytest.fixture
def sender():
    return LineSender(access_token="fake-token")


def test_send_text_single_message(monkeypatch, sender):
    post_mock = Mock(return_value=type("Resp", (), {"raise_for_status": lambda self: None})())
    monkeypatch.setattr("output.line_sender.httpx.post", post_mock)

    sender.send_text("hello", user_id="user-123")

    post_mock.assert_called_once()
    args, kwargs = post_mock.call_args
    assert args[0] == "https://api.line.me/v2/bot/message/push"
    assert kwargs["json"]["to"] == "user-123"
    assert kwargs["json"]["messages"][0]["text"] == "hello"


def test_send_text_broadcast(monkeypatch, sender):
    post_mock = Mock(return_value=type("Resp", (), {"raise_for_status": lambda self: None})())
    monkeypatch.setattr("output.line_sender.httpx.post", post_mock)

    sender.send_text("hello")

    post_mock.assert_called_once()
    args, kwargs = post_mock.call_args
    assert args[0] == "https://api.line.me/v2/bot/message/broadcast"
    assert "to" not in kwargs["json"]


def test_split_text_prefers_newline():
    text = "a" * 3000 + "\n" + "b" * 3000

    chunks = split_text(text, limit=5000)

    assert chunks == ["a" * 3000, "b" * 3000]


def test_split_text_hard_cut_without_newline():
    chunks = split_text("x" * 12000, limit=5000)

    assert [len(c) for c in chunks] == [5000, 5000, 2000]


def test_send_text_long_message_batches_requests(monkeypatch, sender):
    post_mock = Mock(return_value=type("Resp", (), {"raise_for_status": lambda self: None})())
    monkeypatch.setattr("output.line_sender.httpx.post", post_mock)

    sender.send_text("x" * 5000 * 6, user_id="user-123")

    assert post_mock.call_count == 2
    first, second = post_mock.call_args_list
    assert len(first.kwargs["json"]["messages"]) == 5
    assert len(second.kwargs["json"]["messages"]) == 1
    assert all(len(m["text"]) <= 5000 for m in first.kwargs["json"]["messages"])
