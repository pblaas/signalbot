""" Collection of Bot functions """

import os
import random
import pprint
import json
import urllib3
import shutil


def gethelp():
    """ return all available commands """
    return """Available commands:
    !help
    !version
    !random
    !flip
    !chuck
    !gif
    """

def getrandom():
    """ return a random number between 0 and 1000 """
    return random.randrange(1000)


def getflip():
    """ Flip a coin, Heads and Tails """
    return random.choice(['Heads', 'Tails'])


def getchuck():
    """ Get random jokes from chucknorris API """
    http = urllib3.PoolManager()
    req_return = http.request('GET', 'https://api.chucknorris.io/jokes/random')
    chuck = json.loads(req_return.data.decode('utf-8'))
    pprint.pprint(chuck)
    return chuck['value']


def getgif():
    """ Get random gif images from Giphy platform """
    home = os.environ['HOME']
    http = urllib3.PoolManager()
    req_gif = http.request('GET', 'https://api.giphy.com/v1/gifs/random?api_key=elRcLdk25G3cllhDMki4ZIKLMxKqRPSW&tag=funny&rating=pg-13')
    gif = json.loads(req_gif.data.decode('utf-8'))
    url = "https://i.giphy.com/media/" + gif['data']['id'] + "/giphy.gif"

    with open(home + "/signal/giphy.gif", 'wb') as out:
        r = http.request('GET', url, preload_content=False)
        shutil.copyfileobj(r, out)
    return "gif"


def getversion(version, author):
    """ return version information """
    return "SignalCLI bot version: " + version + " by " + author
