# python
import urllib3
import json
import pprint
import shutil

http = urllib3.PoolManager()
req_gif = http.request('GET', 'https://api.giphy.com/v1/gifs/random?api_key=elRcLdk25G3cllhDMki4ZIKLMxKqRPSW&tag=&rating=g')
gif = json.loads(req_gif.data.decode('utf-8'))
pprint.pprint(gif)
url = "https://i.giphy.com/media/" + gif['data']['id'] + "/giphy.gif"


with open("giphy.gif", 'wb') as out:
     r = http.request('GET', url, preload_content=False)
     shutil.copyfileobj(r, out)
