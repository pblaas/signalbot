from botfunctions import SwitchCase
import pytest
import emoji
import re


@pytest.fixture
def switchcase():
    return SwitchCase('7.7.7', 'Patrick', True, '')


def test_switch_get_function_invalid_option(switchcase):
    assert 'Invalid option.' == switchcase.switch('!invalid')


def test_switch_get_function_flip(switchcase):
    assert 'Heads' or 'Tails2' == switchcase.switch('!flip')


def test_switch_get_function_winamp(switchcase):
    thumb = emoji.emojize(':llama:')
    assert 'It really whips the ' + thumb + ' ass.' == switchcase.switch('!winamp')


def test_switch_get_function_version(switchcase):
    assert 'SignalCLI bot version: 7.7.7 by Patrick' == switchcase.switch('!version')


def test_switch_get_function_twitch(switchcase):
    assert 'twitch subcommands' in switchcase.switch('!twitch')


def test_switch_get_function_trivia(switchcase):
    assert 'Trivia:' and 'Options:' in switchcase.switch('!trivia')


def test_switch_get_function_rand(switchcase):
    assert re.match(r'\w+\s\w+', switchcase.switch('!rand'))


def test_switch_get_function_me(switchcase):
    thumb = emoji.emojize(':eggplant:')
    assert thumb == switchcase.switch('!me')


def test_switch_get_function_hn(switchcase):
    assert 'Hacker News' in switchcase.switch('!hn')


def test_switch_get_function_help(switchcase):
    assert 'cmnds' in switchcase.switch('!help')


def test_switch_get_function_haiku(switchcase):
    assert re.match(r'\w+\s\w+,\s\w+\s\w+\s\w+,\s\w+\s\w+', switchcase.switch('!haiku'))


@pytest.mark.skip("WIP")
def test_switch_get_function_gnews(switchcase):
    assert '' == switchcase.switch('!gnews')


@pytest.mark.skip("Not implemented in switchcase")
def test_switch_get_function_testemoji(switchcase):
    tv2 = emoji.emojize(':tv2:')
    movie_camera = emoji.emojize(':movie_camera:')
    apple2 = emoji.emojize(':apple2:')
    lemon = emoji.emojize(':lemon:')
    pineapple = emoji.emojize(':pineapple:')
    pear = emoji.emojize(':pear:')
    tomato = emoji.emojize(':tomato:')
    assert tv2 + " " + movie_camera + " " + apple2 + " " + lemon + " " + pineapple + " " + pear + " " + tomato == switchcase.switch('!testemoji')


@pytest.mark.skip("Not implemented in switchcase")
def test_switch_get_function_test(switchcase):
    assert '@#*&ES&@#YF.. nooo you got me!' == switchcase.switch('!test')
