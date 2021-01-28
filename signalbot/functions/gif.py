"""Gif module."""

import urllib3
import json
import os
import shutil


class Gif:
    """Defining base class for inheritence."""

    def gif(self):
        """Get random gif images from Giphy platform."""
        http = urllib3.PoolManager()
        req_gif = http.request('GET', 'https://api.giphy.com/v1/gifs/random?api_key=elRcLdk25G3cllhDMki4ZIKLMxKqRPSW&tag=funny&rating=pg-13')
        gif = json.loads(req_gif.data.decode('utf-8'))
        url = "https://i.giphy.com/media/" + gif['data']['id'] + "/giphy.gif"

        if self._signalexecutorlocal is False:
            home = os.environ['HOME']
            with open(home + "/signal/giphy.gif", 'wb') as out:
                r = http.request('GET', url, preload_content=False)
                shutil.copyfileobj(r, out)
        else:
            with open("/tmp/signal/giphy.gif", 'wb') as out:
                r = http.request('GET', url, preload_content=False)
                shutil.copyfileobj(r, out)
        return "Gif"
