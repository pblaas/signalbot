from botfunctions import SwitchCase
from functions.twitch import SwitchCaseTwitch
import pytest
import re


@pytest.fixture
def switchcase():
    return SwitchCase('7.7.7', 'Patrick', True, '')


@pytest.fixture
def switchcasetwitch():
    return SwitchCaseTwitch()


def test_switch_get_function_twitch_without_option(switchcase):
    assert 'twitch subcommands' in switchcase.switch('!twitch')

    
def test_switch_get_function_twitch_get_access_token(switchcasetwitch):
    assert re.match(r'\w{30}', switchcasetwitch._getaccestoken())


def test_switch_get_function_twitch_get_topgames(switchcasetwitch):
    assert re.match(r'\s*Top games:', switchcasetwitch.topgames())


def test_switch_get_function_twitch_get_topstreams(switchcasetwitch):
    assert re.match(r'\s*Top Streams:', switchcasetwitch.topstreams())


def test_switch_get_function_twitch_get_pcreleases(switchcasetwitch):
    assert re.match(r'\s*New PC releases:', switchcasetwitch.pcreleases())


def test_switch_get_function_twitch_get_xboxxreleases(switchcasetwitch):
    assert 'Xbox series X releases' in switchcasetwitch.xboxxreleases()


def test_switch_get_function_twitch_get_ps5releases(switchcasetwitch):
    assert 'PS5 releases' in switchcasetwitch.ps5releases()


def test_switch_get_function_twitch_no_clientid(monkeypatch):
    """Unset the TWITCH_CLIENTID env var to assert the behavior."""
    t = SwitchCase("7.7.7", "author", True, "!twitch pcr")
    monkeypatch.delenv("TWITCH_CLIENTID", raising=False)
    assert t.switch("!twitch pcr") == "No Twitch clientid and Twitch clientsecret found."
