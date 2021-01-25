"""Collection of Bot functions."""

import os
import random
# import pprint
import html
import json
import urllib3
import shutil
import emoji
from random import randint
from haikunator import Haikunator


class SwitchCase:
    """SwitchCase class to switch bot functions."""

    def __init__(self, version, author, signalexecutorlocal, messageobject):
        """Initialize SwitchCase with version and author variables."""
        self._version = version
        self._author = author
        self._signalexecutorlocal = signalexecutorlocal
        self._messageobject = messageobject

    def switch(self, action):
        """Switch function to switch between available functions."""
        default = "Invalid option."
        return getattr(self, str(action)[1:].split()[0], lambda: default)()

    def help(self):
        """Return all available commands."""
        return """
        cmnds
        ----
        !help
        !version
        !random
        !flip
        !chuck
        !gif
        !haiku
        !names
        !me
        !hn
        !twitch
        !bored
        !trivia
        """

    def test(self):
        """Simple test function."""
        return "@#*&ES&@#YF.. nooo you got me!"

    def version(self):
        """Return version information."""
        return "SignalCLI bot version: " + self._version + " by " + self._author

    def gif(self):
        """Get random gif images from Giphy platform."""
        http = urllib3.PoolManager()
        req_gif = http.request('GET', 'https://api.giphy.com/v1/gifs/random?api_key=elRcLdk25G3cllhDMki4ZIKLMxKqRPSW&tag=funny&rating=pg-13')
        gif = json.loads(req_gif.data.decode('utf-8'))
        url = "https://i.giphy.com/media/" + gif['data']['id'] + "/giphy.gif"

        if self._signalexecutorlocal is False:
            home = os.environ['HOME']
            with open(home + "/signal/giphy.gif", 'wb') as out:
                r = http.request('GET', url, preload_content=False)
                shutil.copyfileobj(r, out)
        else:
            with open("/tmp/signal/giphy.gif", 'wb') as out:
                r = http.request('GET', url, preload_content=False)
                shutil.copyfileobj(r, out)
        return "Gif"

    def chuck(self):
        """Get random jokes from chucknorris API."""
        http = urllib3.PoolManager()
        req_return = http.request('GET', 'https://api.chucknorris.io/jokes/random')
        chuck = json.loads(req_return.data.decode('utf-8'))
        # pprint.pprint(chuck)
        return chuck['value']

    def flip(self):
        """Flip a coin, Heads and Tails."""
        return random.choice(['Heads', 'Tails'])

    def random(self):
        """Return a random number between 0 and 1000."""
        haikunator = Haikunator()
        return haikunator.haikunate(token_length=0, delimiter=' ')

    def haiku(self):
        """Return a random generator Haiku."""
        wordList1 = ["Enchanting", "Amazing", "Colourful", "Delightful", "Delicate"]
        wordList2 = ["visions", "distance", "conscience", "process", "chaos"]
        wordList3 = ["superstitious", "contrasting", "graceful", "inviting", "contradicting", "overwhelming"]
        wordList4 = ["true", "dark", "cold", "warm", "great"]
        wordList5 = ["scenery", "season", "colours", "lights", "Spring", "Winter", "Summer", "Autumn"]
        wordList6 = ["undeniable", "beautiful", "irreplaceable", "unbelievable", "irrevocable"]
        wordList7 = ["inspiration", "imagination", "wisdom", "thoughts"]

        wordIndex1 = randint(0, len(wordList1) - 1)
        wordIndex2 = randint(0, len(wordList2) - 1)
        wordIndex3 = randint(0, len(wordList3) - 1)
        wordIndex4 = randint(0, len(wordList4) - 1)
        wordIndex5 = randint(0, len(wordList5) - 1)
        wordIndex6 = randint(0, len(wordList6) - 1)
        wordIndex7 = randint(0, len(wordList7) - 1)

        haiku = wordList1[wordIndex1] + " " + wordList2[wordIndex2] + ",\n"
        haiku = haiku + wordList3[wordIndex3] + " " + wordList4[wordIndex4] + " " + wordList5[wordIndex5] + ",\n"
        haiku = haiku + wordList6[wordIndex6] + " " + wordList7[wordIndex7] + "."

        return haiku

    names = random

    def me(self):
        """Return random Emoij."""
        thumb = emoji.emojize(':eggplant:')
        return thumb

    def hn(self):
        """Return 1 of 10 latest hacker news items."""
        thumb = emoji.emojize(':newspaper:')
        http = urllib3.PoolManager()
        req_url = http.request('GET', 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
        data = json.loads(req_url.data.decode('utf-8'))
        story_url = http.request('GET', 'https://hacker-news.firebaseio.com/v0/item/' + str(data[randint(0, 9)]) + '.json?print=pretty')
        story_data = json.loads(story_url.data.decode('utf-8'))
        return (thumb + " Hacker News: [" + str(story_data['score']) + "] " + story_data['title'] + " -> " + story_data['url'])

    def winamp(self):
        """Return random Emoij."""
        thumb = emoji.emojize(':llama:')
        return "It really whips the " + thumb + " ass."

    def dog(self):
        """Return random Emoij."""
        dog = emoji.emojize(':dog:')
        return dog + " WOEF,  WAFFF! " + dog

    def testemoji(self):
        """Return random Emoij."""
        tv2 = emoji.emojize(':tv2:')
        movie_camera = emoji.emojize(':movie_camera:')
        apple2 = emoji.emojize(':apple2:')
        lemon = emoji.emojize(':lemon:')
        pineapple = emoji.emojize(':pineapple:')
        pear = emoji.emojize(':pear:')
        tomato = emoji.emojize(':tomato:')

        return tv2 + " " + movie_camera + " " + apple2 + " " + lemon + " " + pineapple + " " + pear + " " + tomato

    def bored(self):
        """Get random jokes from chucknorris API."""
        http = urllib3.PoolManager()
        req_return = http.request('GET', 'https://www.boredapi.com/api/activity?type=recreational')
        activity_data = json.loads(req_return.data.decode('utf-8'))
        # pprint.pprint(chuck)
        return activity_data['activity']

    def trivia():
        """Get random jokes from chucknorris API."""
        http = urllib3.PoolManager()
        req_return = http.request('GET', 'https://opentdb.com/api.php?amount=1')
        trivia_data = json.loads(req_return.data.decode('utf-8'))
        all_answers = trivia_data['results'][0]['incorrect_answers']
        all_answers.insert(0, trivia_data['results'][0]['correct_answer'])
        random.shuffle(all_answers)
        str = ","
        shuffled_string = str.join(all_answers)
        return f"""Trivia:
        {html.unescape(trivia_data['results'][0]['question'])}
        Options: {shuffled_string}
        """

    def twitch(self):
        """Return game related content."""
        print("Messages Object: " + self._messageobject)
        twitchcase = SwitchCaseTwitch()
        if len(self._messageobject.strip().split(" ")) > 1:
            message = self._messageobject.split()[1]
        else:
            message = "default"

        twitchfunctionreturn = twitchcase.switch(message).replace('"', '')
        return twitchfunctionreturn


class SwitchCaseTwitch:
    """SwitchCaseTwitch class to switch Twitch bot subfunctions."""

    def switch(self, action):
        """Switch function to switch between available functions."""
        default = "Not a twitch function."
        return getattr(self, str(action), lambda: default)()

    def topgames(self):
        """Switch function to show top 3 most popular streams."""
        CLIENTID = "xu5vir3u0bdxub6q8r3qq50o9t0cik"
        CLIENTSECRET = "ocqwwmooe78inxki55ugbnld1uz9rl"
        http = urllib3.PoolManager()
        data = {'client_id': CLIENTID, 'client_secret': CLIENTSECRET, 'grant_type': "client_credentials"}
        req_url = http.request(
            "POST", "https://id.twitch.tv/oauth2/token",
            body=json.dumps(data),
            headers={'Content-Type': 'application/json'})
        data = json.loads(req_url.data.decode('utf-8'))
        # contains access token:
        # data['access-token']
        # pprint.pprint(data)

        helix_url = http.request(
            "GET", "https://api.twitch.tv/helix/games/top",
            headers={
                "Authorization": "Bearer " + data['access_token'],
                "Client-Id": CLIENTID
            })
        # print(helix_url)
        helixdata = json.loads(helix_url.data.decode('utf-8'))
        # selection = data[:10]
        return f"""
        Top games:
        1: {helixdata['data'][0]['name']}
        2: {helixdata['data'][1]['name']}
        3: {helixdata['data'][2]['name']}
        4: {helixdata['data'][3]['name']}
        5: {helixdata['data'][4]['name']}
        """

    # Adding alias to topgames
    tg = topgames

    def topstreams(self):
        """Switch function to show top 3 most popular streams."""
        CLIENTID = "xu5vir3u0bdxub6q8r3qq50o9t0cik"
        CLIENTSECRET = "ocqwwmooe78inxki55ugbnld1uz9rl"
        http = urllib3.PoolManager()
        data = {'client_id': CLIENTID, 'client_secret': CLIENTSECRET, 'grant_type': "client_credentials"}
        req_url = http.request(
            "POST", "https://id.twitch.tv/oauth2/token",
            body=json.dumps(data),
            headers={'Content-Type': 'application/json'})
        data = json.loads(req_url.data.decode('utf-8'))
        # contains access token:
        # data['access-token']
        # pprint.pprint(data)

        helix_url = http.request(
            "GET", "https://api.twitch.tv/helix/streams",
            headers={
                "Authorization": "Bearer " + data['access_token'],
                "Client-Id": CLIENTID
            })
        # print(helix_url)
        helixdata = json.loads(helix_url.data.decode('utf-8'))
        # selection = data[:10]
        movie_camera = emoji.emojize(':movie_camera:')
        return f"""
        Top Streams:
        1: {movie_camera}: {helixdata['data'][0]['viewer_count']} {helixdata['data'][0]['user_name']} game: {helixdata['data'][0]['game_name']}
        2: {movie_camera}: {helixdata['data'][1]['viewer_count']} {helixdata['data'][1]['user_name']} game: {helixdata['data'][1]['game_name']}
        3: {movie_camera}: {helixdata['data'][2]['viewer_count']} {helixdata['data'][2]['user_name']} game: {helixdata['data'][2]['game_name']}
        """

    # Adding alias to topstreams
    ts = topstreams
