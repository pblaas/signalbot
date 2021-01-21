"""Collection of Bot functions."""

import os
import random
# import pprint
import json
import urllib3
import shutil


class SwitchCase:
    """SwitchCase class to switch bot functions."""

    def __init__(self, version, author):
        """Initialize SwitchCase with version and author variables."""
        self._version = version
        self._author = author

    def switch(self, action):
        """Switch function to switch between available functions."""
        default = "Invalid option."
        return getattr(self, str(action)[1:], lambda: default)()

    def help(self):
        """Return all available commands."""
        return """
        cmnds
        ----
        !help
        !version
        !random
        !flip
        !chuck
        !gif
        """

    def test(self):
        """Simple test function."""
        return "@#*&ES&@#YF.. nooo you got me!"

    def version(self):
        """Return version information."""
        return "SignalCLI bot version: " + self._version + " by " + self._author

    def gif(self):
        """Get random gif images from Giphy platform."""
        home = os.environ['HOME']
        http = urllib3.PoolManager()
        req_gif = http.request('GET', 'https://api.giphy.com/v1/gifs/random?api_key=elRcLdk25G3cllhDMki4ZIKLMxKqRPSW&tag=funny&rating=pg-13')
        gif = json.loads(req_gif.data.decode('utf-8'))
        url = "https://i.giphy.com/media/" + gif['data']['id'] + "/giphy.gif"

        with open(home + "/signal/giphy.gif", 'wb') as out:
            r = http.request('GET', url, preload_content=False)
            shutil.copyfileobj(r, out)
        return "Gif"

    def chuck(self):
        """Get random jokes from chucknorris API."""
        http = urllib3.PoolManager()
        req_return = http.request('GET', 'https://api.chucknorris.io/jokes/random')
        chuck = json.loads(req_return.data.decode('utf-8'))
        # pprint.pprint(chuck)
        return chuck['value']

    def flip(self):
        """Flip a coin, Heads and Tails."""
        return random.choice(['Heads', 'Tails'])

    def random(self):
        """Return a random number between 0 and 1000."""
        return str(random.randrange(1000))
