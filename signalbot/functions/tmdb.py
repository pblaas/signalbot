"""Tmdb module."""

import urllib3
import json
import os
import textwrap
from datetime import datetime
from pprint import pprint as pp


class Tmdb:
    """Defining base class for inheritence."""

    def tmdb(self):
        """Return news related content."""
        if len(self._messageobject.strip().split(" ")) > 1:
            category = self._messageobject.split()[1]
            message = self._messageobject.split(" ")[2:]
        else:
            category = "default"
            message = ""

        tmdbcase = SwitchCaseTmdb(category, message)
        tmdbreturn = tmdbcase.switch().replace('"', '')
        return tmdbreturn


class SwitchCaseTmdb:
    """SwitchCaseTmdb class to switch gnews bot subfunctions."""

    def __init__(self, category, message):
        m = "%20"
        self._category = category
        self._message = m.join(message)

    def switch(self):
        """Switch function to switch between available functions."""
        default = textwrap.dedent("""\
        tmdb subcommands:\n
        [movierelease | mr] {string}- release dates movies
        [tvshowrelease | tvr] {string}- release dates shows
        [newtvshow | ntv] -  release dates new shows
        [movie] {string}- movie info
        [tvshow] {string}- tvshow info""")
        return getattr(self, str(self._category), lambda: default)()

    @staticmethod
    def _queryapi(endpoint, searchstring):
        if "TMDB_APIKEY" in os.environ:
            apikey = os.environ['TMDB_APIKEY']
            today = datetime.now().strftime("%Y-%m-%d")
            if "search" in endpoint:
                additional_flags = "&query=" + searchstring
            elif "discover" in endpoint:
                additional_flags = "&sort_by=popularity.desc&timezone=America%2FNew_York&include_null_first_air_dates=false&first_air_date.gte=" + today
            http = urllib3.PoolManager()
            url = "https://api.themoviedb.org/3/" + endpoint + "?api_key=" + apikey + "&language=en-US&page=1&include_adult=false" + additional_flags
            req_return = http.request('GET', url)
            return req_return
        else:
            return "No tmdb API KEY found."

    def movierelease(self):
        """Get movie release info from tmdb API."""
        endpoint = "search/movie"
        searchstring = str(self._message)
        all_items = json.loads(self._queryapi(endpoint, searchstring).data.decode('utf-8'))
        all_item_results = len(all_items['results'])
        if all_item_results > 0:
            item_array = []
            for x in range(0, all_item_results):
                if x == 3:
                    break
                item_array.append(f"{all_items['results'][x]['release_date']} -> {all_items['results'][x]['original_title']}")

            new_line = "\n"
            item_return_string = new_line.join(item_array)
            pp(item_return_string)
            return f"""The Movie DB Movie Release Dates:\n\n{item_return_string}"""
        else:
            return "tmdb: no items found."

    mr = movierelease

    def movie(self):
        """Get movie info from tmdb API."""
        endpoint = "search/movie"
        searchstring = str(self._message)
        all_items = json.loads(self._queryapi(endpoint, searchstring).data.decode('utf-8'))
        all_item_results = len(all_items['results'])
        if all_item_results > 0:
            return textwrap.dedent(f"""\
            The Movie DB Movie Info:\n
            {all_items['results'][0]['original_title']}
            Overview: {all_items['results'][0]['overview']}
            Popularity: {all_items['results'][0]['popularity']}
            Vote avg: {all_items['results'][0]['vote_average']}
            Vote count: {all_items['results'][0]['vote_count']}""")
        else:
            return "tmdb: no items found."

    def tvshow(self):
        """Get tvshow info from tmdb API."""
        endpoint = "search/tv"
        searchstring = str(self._message)
        all_items = json.loads(self._queryapi(endpoint, searchstring).data.decode('utf-8'))
        all_item_results = len(all_items['results'])
        if all_item_results > 0:
            if all_items['results'][0]['first_air_date']:
                first_date_date = all_items['results'][0]['first_air_date']
            else:
                first_date_date = "Unknown."
            return textwrap.dedent(f"""\
            The Movie DB TVshow Info:\n
            {all_items['results'][0]['original_name']}
            Overview: {all_items['results'][0]['overview']}
            Popularity: {all_items['results'][0]['popularity']}
            Vote avg: {all_items['results'][0]['vote_average']}
            Vote count: {all_items['results'][0]['vote_count']}
            First aired: {first_date_date}""")
        else:
            return "tmdb: no items found."

    def tvshowrelease(self):
        """Get tvshow release date info from tmdb API."""
        endpoint = "search/tv"
        searchstring = str(self._message)
        all_items = json.loads(self._queryapi(endpoint, searchstring).data.decode('utf-8'))
        all_item_results = len(all_items['results'])
        pp(all_items)
        if all_item_results > 0:
            item_array = []
            for x in range(0, all_item_results):
                if x == 3:
                    break
                if all_items['results'][0]['first_air_date']:
                    first_date_date = all_items['results'][0]['first_air_date']
                else:
                    first_date_date = "Unknown."

                item_array.append(f"{first_date_date} -> {all_items['results'][x]['name']}")

            new_line = "\n"
            item_return_string = new_line.join(item_array)
            pp(item_return_string)
            return f"""The Movie DB tvshow Release Dates:\n\n{item_return_string}"""
        else:
            return "tmdb: no items found."

    tvr = tvshowrelease

    def newtvshow(self):
        """Get new tvshow release date info from tmdb API."""
        endpoint = "discover/tv"
        searchstring = ""
        all_items = json.loads(self._queryapi(endpoint, searchstring).data.decode('utf-8'))
        all_item_results = len(all_items['results'])
        if all_item_results > 0:
            item_array = []
            for x in range(0, all_item_results):
                if x == 5:
                    break
                item_array.append(f"{all_items['results'][x]['first_air_date']} -> {all_items['results'][x]['name']}")

            new_line = "\n"
            item_return_string = new_line.join(item_array)
            pp(item_return_string)
            return f"""The Movie DB New TVshow Release Dates:\n\n{item_return_string}"""
        else:
            return "tmdb: no items found."

    ntv = newtvshow
