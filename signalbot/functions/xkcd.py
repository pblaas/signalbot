"""Xkcd module."""

import urllib3
import json
import shutil
import random


class Xkcd:
    """Defining base class for inheritence."""

    def xkcd(self):
        """Get random images from xkcd platform."""

        # Retrieve the latest issue number.
        http = urllib3.PoolManager()
        req_xkcd_latest = http.request('GET', "https://xkcd.com/" + "/info.0.json")
        xkcd_json_latest = json.loads(req_xkcd_latest.data.decode('utf-8'))

        # Retrieve a random issue from min and max issue number range.
        random_int = random.randint(1, xkcd_json_latest['num'])
        req_xkcd = http.request('GET', "https://xkcd.com/" + str(random_int) + "/info.0.json")
        xkcd_json = json.loads(req_xkcd.data.decode('utf-8'))

        if xkcd_json['title']:
            with open("/tmp/signal/image.png", 'wb') as out:
                r = http.request('GET', xkcd_json['img'], preload_content=False)
                shutil.copyfileobj(r, out)
            return "xkcd"

        else:
            return "No valid repsonse from xkcd API."
