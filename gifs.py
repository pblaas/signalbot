# python
import urllib3
import json
import pprint

http = urllib3.PoolManager()
r = http.request('GET', 'https://api.giphy.com/v1/gifs/random?api_key=elRcLdk25G3cllhDMki4ZIKLMxKqRPSW&tag=&rating=g')
gif = json.loads(r.data.decode('utf-8'))
#pprint.pprint(gif)
print(gif['data']['image_original_url'])