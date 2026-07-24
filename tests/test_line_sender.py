from unittest.mock import Mock

import pytest

from output.line_sender import LineSender


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
