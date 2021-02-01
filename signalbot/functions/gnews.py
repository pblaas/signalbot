"""Gnews module."""

import urllib3
import json
import os
import random


class Gnews:
    """Defining base class for inheritence."""

    def gnews(self):
        """Return news related content."""
        if len(self._messageobject.strip().split(" ")) > 1:
            gnewscase = SwitchCaseGnews(self._messageobject.strip().split(" ")[1])
        else:
            gnewscase = SwitchCaseGnews('science')

        gnewsreturn = gnewscase.query().replace('"', '')
        return gnewsreturn


class SwitchCaseGnews:
    """SwitchCaseGnews class to switch gnews bot subfunctions."""

    def __init__(self, query):
        """Initialize SwitchCase with version and author variables."""
        self._query = query

    def query(self):
        """Switch function to switch between available functions."""
        default = """gnews subcommands:
        yourquery
        """
        return getattr(self, 'fetch', lambda: default)()

    def fetch(self):
        """Get news from gnews API."""
        if "GNEWS_APIKEY" in os.environ:
            apikey = os.environ['GNEWS_APIKEY']
            reqinfo = self._query
            http = urllib3.PoolManager()
            req_return = http.request('GET', 'https://gnewsapi.net/api/search?q=' + reqinfo + '&country=nl&language=nl&api_token=' + apikey)
            all_news = json.loads(req_return.data.decode('utf-8'))
            total_articles = len(all_news['articles'])
            if total_articles > 0:
                random_article_number = random.randint(0, total_articles)
                return f"""Gnews: {all_news['articles'][random_article_number]['title']} -> {all_news['articles'][random_article_number]['article_url']}"""
            else:
                return "Gnews: No articles found."
        else:
            return "No Gnews API key found."
