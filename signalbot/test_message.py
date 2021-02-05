from message import Message
import pytest


@pytest.fixture
def message():
    return Message("+316", "testmessage", "groupid4", 112233)


def test_lookup_message(message):
    assert "testmessage" == message.getmessage()


def test_lookup_timestamp(message):
    assert "112233" == message.gettimestamp()


def test_lookup_source(message):
    assert "+316" == message.getsource()


def test_lookup_groupinfo(message):
    assert "groupid4" == message.getgroupinfo()
