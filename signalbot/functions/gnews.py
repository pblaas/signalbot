"""Gnews module."""

import urllib3
import json
import random


class Gnews():
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
        APITOKEN = '3zhnLmjmyvvmVYHF1gB8m8z2WdjDtGjPyqvUOdXMeOxTkkNYnB84on9YGMzQ'
        reqinfo = self._query
        http = urllib3.PoolManager()
        req_return = http.request('GET', 'https://gnewsapi.net/api/search?q=' + reqinfo + '&country=nl&language=nl&api_token=' + APITOKEN)
        all_news = json.loads(req_return.data.decode('utf-8'))
        total_articles = len(all_news['articles'])
        random_article_number = random.randint(0, total_articles)
        return(f"""
        {all_news['articles'][random_article_number]['title']} -> {all_news['articles'][random_article_number]['article_url']}
        """)
        # return al['value']
