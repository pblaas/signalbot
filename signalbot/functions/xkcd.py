"""Xkcd module."""

import urllib3
import json
import os
import shutil
import random


class Xkcd:
    """Defining base class for inheritence."""

    def xkcd(self):
        """Get random images from xkcd platform."""

        random_int = random.randint(1, 2421)
        http = urllib3.PoolManager()
        req_xkcd = http.request('GET', "https://xkcd.com/" + str(random_int) + "/info.0.json")
        xkcd_json = json.loads(req_xkcd.data.decode('utf-8'))

        if xkcd_json['title']:
            if self._signalexecutorlocal is False:
                home = os.environ['HOME']
                with open(home + "/signal/image.png", 'wb') as out:
                    r = http.request('GET', xkcd_json['img'], preload_content=False)
                    shutil.copyfileobj(r, out)
            else:
                with open("/tmp/signal/image.png", 'wb') as out:
                    r = http.request('GET', xkcd_json['img'], preload_content=False)
                    shutil.copyfileobj(r, out)

            return "xkcd"

        else:
            return "No valid repsonse from xkcd API."
