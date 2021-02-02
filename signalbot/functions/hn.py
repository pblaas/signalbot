"""Hacker news module."""

import urllib3
import json
import emoji
from random import randint


class Hn:
    """Defining base class for inheritence."""

    def hn(self):
        """Return 1 of 10 latest hacker news items."""
        thumb = emoji.emojize(':newspaper:')
        http = urllib3.PoolManager()
        req_url = http.request('GET', 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
        data = json.loads(req_url.data.decode('utf-8'))
        if len(data) > 0:
            story_url = http.request('GET', 'https://hacker-news.firebaseio.com/v0/item/' + str(data[randint(0, 9)]) + '.json?print=pretty')
            story_data = json.loads(story_url.data.decode('utf-8'))
            if 'url' in story_data:
                return thumb + " Hacker News: [" + str(story_data['score']) + "] " + story_data['title'] + " -> " + story_data['url']
            else:
                return "Hacker News: Unable to retrieve news."
        else:
            return "Hacker News: unable to access api."
