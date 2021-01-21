""" Message module """

import os
import random
import pprint
import json
import urllib3
import shutil


class Message:
    """ Message class to model data """
    def __init__(self, source, message, groupinfo, author, version):
        self._source = source
        self._message = message
        self._groupinfo = groupinfo
        self._author = author
        self._version = version

    def getgroupinfo(self):
        """ return groupID """
        return self._groupinfo

    def getmessage(self):
        """ return message string """
        return self._message

    def getsource(self):
        """ return initiator of the message """
        return self._source

    def getversion(self):
        """ return version information """
        return "SignalCLI bot version: " + self._version + " by " + self._author

    def gethelp(self):
        """ return all available commands """
        return """Available commands:
        !help
        !version
        !random
        !flip
        !chuck
        !gif
        """

    def getrandom(self):
        """ return a random number between 0 and 1000 """
        return random.randrange(1000)

    def getflip(self):
        """ Flip a coin, Heads and Tails """
        return random.choice(['Heads', 'Tails'])

    def getchuck(self):
        """ Get random jokes from chucknorris API """
        http = urllib3.PoolManager()
        req_return = http.request('GET', 'https://api.chucknorris.io/jokes/random')
        chuck = json.loads(req_return.data.decode('utf-8'))
        pprint.pprint(chuck)
        return chuck['value']

    def getgif(self):
        """ Get random gif images from Giphy platform """
        home = os.environ['HOME']
        http = urllib3.PoolManager()
        req_gif = http.request('GET', 'https://api.giphy.com/v1/gifs/random?api_key=elRcLdk25G3cllhDMki4ZIKLMxKqRPSW&tag=&rating=g')
        gif = json.loads(req_gif.data.decode('utf-8'))
        url = "https://i.giphy.com/media/" + gif['data']['id'] + "/giphy.gif"

        with open(home + "/signal/giphy.gif", 'wb') as out:
            r = http.request('GET', url, preload_content=False)
            shutil.copyfileobj(r, out)
        return "gif"
