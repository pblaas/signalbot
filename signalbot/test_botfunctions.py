from botfunctions import SwitchCase
from functions.twitch import SwitchCaseTwitch
import pytest
import emoji
import re


@pytest.fixture
def switchcase():
    return SwitchCase('7.7.7', 'Patrick', True, '')


@pytest.fixture
def switchcasetwitch():
    return SwitchCaseTwitch()


def test_switch_get_function_invalid_option(switchcase):
    assert 'Invalid option.' == switchcase.switch('!invalid')


def test_switch_get_function_bored(switchcase):
    assert re.match(r'\w+\s\w+', switchcase.switch('!bored'))


def test_switch_get_function_chuck(switchcase):
    assert re.match(r'\w+\s\w+', switchcase.switch('!chuck'))


def test_switch_get_function_dog(switchcase):
    dog = emoji.emojize(':dog:')
    assert dog + " WOEF,  WAFFF! " + dog == switchcase.switch('!dog')


def test_switch_get_function_flip(switchcase):
    assert switchcase.switch('!flip') in ['Heads', 'Tails']


def test_switch_get_function_gif(switchcase):
    assert switchcase.switch('!gif') in ['Gif', 'No Giphy API key found.']


def test_switch_get_function_gnews(switchcase):
    assert re.match(r'Gnews:\s\w+\s\w+', switchcase.switch('!gnews'))


def test_switch_get_function_haiku(switchcase):
    assert re.match(r'\w+\s\w+,\s\w+\s\w+\s\w+,\s\w+\s\w+', switchcase.switch('!haiku'))


def test_switch_get_function_help(switchcase):
    assert 'cmnds' in switchcase.switch('!help')


def test_switch_get_function_hn(switchcase):
    assert 'Hacker News' in switchcase.switch('!hn')


def test_switch_get_function_me(switchcase):
    thumb = emoji.emojize(':eggplant:')
    assert thumb == switchcase.switch('!me')


def test_switch_get_function_rand(switchcase):
    assert re.match(r'\w+\s\w+', switchcase.switch('!rand'))


def test_switch_get_function_test(switchcase):
    assert '@#*&ES&@#YF.. nooo you got me!' == switchcase.switch('!test')


def test_switch_get_function_testemoji(switchcase):
    tv2 = emoji.emojize(':tv2:')
    movie_camera = emoji.emojize(':movie_camera:')
    apple2 = emoji.emojize(':apple2:')
    lemon = emoji.emojize(':lemon:')
    pineapple = emoji.emojize(':pineapple:')
    pear = emoji.emojize(':pear:')
    tomato = emoji.emojize(':tomato:')
    assert tv2 + " " + movie_camera + " " + apple2 + " " + lemon + " " + pineapple + " " + pear + " " + tomato == switchcase.switch('!testemoji')


def test_switch_get_function_trivia(switchcase):
    assert 'Trivia:' and 'Options:' in switchcase.switch('!trivia')


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


def test_switch_get_function_version(switchcase):
    assert 'SignalCLI bot version: 7.7.7 by Patrick' == switchcase.switch('!version')


def test_switch_get_function_winamp(switchcase):
    thumb = emoji.emojize(':llama:')
    assert 'It really whips the ' + thumb + ' ass.' == switchcase.switch('!winamp')
