"""Gif module."""

import urllib3
import json
import os
import shutil


class Gif:
    """Defining base class for inheritence."""

    def gif(self):
        """Get random gif images from Giphy platform."""

        # test if GIPHY_APIKEY exists before requesting source.
        if "GIPHY_APIKEY" in os.environ:
            apikey = os.environ['GIPHY_APIKEY']
            http = urllib3.PoolManager()
            req_gif = http.request('GET', 'https://api.giphy.com/v1/gifs/random?api_key=' + apikey + '&tag=funny&rating=pg-13')
            gif = json.loads(req_gif.data.decode('utf-8'))

            if len(gif['data']) > 0:
                url = "https://i.giphy.com/media/" + gif['data']['id'] + "/giphy.gif"
                with open("/tmp/signal/giphy.gif", 'wb') as out:
                    r = http.request('GET', url, preload_content=False)
                    shutil.copyfileobj(r, out)

                return "Gif"

            else:
                return "No valid repsonse for Giphy API."
        else:
            return "No Giphy API key found."
