import os
import random
import pprint
import json
import urllib3
import shutil
import emoji
from random import randint

http = urllib3.PoolManager()
req_url = http.request('GET', 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
data = json.loads(req_url.data.decode('utf-8'))
selection = data[:10]
story_url = http.request('GET', 'https://hacker-news.firebaseio.com/v0/item/' + str(data[randint(0, 9)]) + '.json?print=pretty')
story_data = json.loads(story_url.data.decode('utf-8'))
return ("HN: [" + str(story_data['score']) + "] " + story_data['title'] + " -> " + story_data['url'])