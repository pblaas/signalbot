"""Twitch module."""

import urllib3
import json
import os
import emoji
from datetime import datetime, date


class Twitch():
    """Defining base class for inheritence."""

    def twitch(self):
        """Return game related content."""
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
        default = """twitch subcommands:
        topgames || tg
        topstreams || ts
        pcreleases || pcr
        """
        return getattr(self, str(action), lambda: default)()

    def _getaccestoken(self):
        """Retrieve access token."""
        clientid = os.environ['TWITCH_CLIENTID']
        clientsecret = os.environ['TWITCH_CLIENTSECRET']
        http = urllib3.PoolManager()
        data = {'client_id': clientid, 'client_secret': clientsecret, 'grant_type': "client_credentials"}
        req_url = http.request(
            "POST", "https://id.twitch.tv/oauth2/token",
            body=json.dumps(data),
            headers={'Content-Type': 'application/json'})
        data = json.loads(req_url.data.decode('utf-8'))
        return data['access_token']

    def topgames(self):
        """Switch function to show top 3 most popular streams."""
        clientid = os.environ['TWITCH_CLIENTID']
        clientsecret = os.environ['TWITCH_CLIENTSECRET']
        http = urllib3.PoolManager()
        data = {'client_id': clientid, 'client_secret': clientsecret, 'grant_type': "client_credentials"}
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
                "Client-Id": clientid
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
        clientid = os.environ['TWITCH_CLIENTID']
        clientsecret = os.environ['TWITCH_CLIENTSECRET']
        http = urllib3.PoolManager()
        data = {'client_id': clientid, 'client_secret': clientsecret, 'grant_type': "client_credentials"}
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
                "Client-Id": clientid
            })
        # print(helix_url)
        helixdata = json.loads(helix_url.data.decode('utf-8'))
        # selection = data[:10]
        movie_camera = emoji.emojize(':movie_camera:')
        return f"""
        Top Streams:
        {movie_camera} {helixdata['data'][0]['viewer_count']} viewing {helixdata['data'][0]['user_name']} game: {helixdata['data'][0]['game_name']}
        {movie_camera} {helixdata['data'][1]['viewer_count']} viewing {helixdata['data'][1]['user_name']} game: {helixdata['data'][1]['game_name']}
        {movie_camera} {helixdata['data'][2]['viewer_count']} viewing {helixdata['data'][2]['user_name']} game: {helixdata['data'][2]['game_name']}
        """

    # Adding alias to topstreams
    ts = topstreams

    def pcreleases(self):
        """Twitch example function."""
        clientid = os.environ['TWITCH_CLIENTID']
        clientsecret = os.environ['TWITCH_CLIENTSECRET']

        now = datetime.now()
        timestamp = str(datetime.timestamp(now)).split(".")[0]

        http = urllib3.PoolManager()
        data = {'client_id': clientid, 'client_secret': clientsecret, 'grant_type': "client_credentials"}
        req_url = http.request(
            "POST", "https://id.twitch.tv/oauth2/token",
            body=json.dumps(data),
            headers={'Content-Type': 'application/json'})
        data = json.loads(req_url.data.decode('utf-8'))
        # contains access token:
        # data['access-token']
        # pprint.pprint(data)

        helix_url = http.request(
            "POST", "https://api.igdb.com/v4/release_dates",
            headers={
                "Accept": "application/json",
                "Authorization": "Bearer " + data['access_token'],
                "Client-Id": clientid
            },
            # body="fields category,checksum,created_at,date,game,human,m,platform,region,updated_at,y;where y = 2021;where m = 1;"
            body="fields game; where game.platforms = 6 & date > " + timestamp + "; sort date asc; limit 3;"
        )
        # print(helix_url)
        helixdata = json.loads(helix_url.data.decode('utf-8'))
        # selection = data[:10]
        # pprint.pprint(helixdata)
        # print("String: " + string.split()[1])
        # print(helixdata['data'][1]['name'])

        # all_answers = trivia_data['results'][0]['incorrect_answers']
        # all_answers.insert(0, trivia_data['results'][0]['correct_answer'])
        # random.shuffle(all_answers)

        all_games = []
        for x in range(len(helixdata)):
            # print(helixdata[x]['game'])
            all_games.append(str(helixdata[x]['game']))

        string = ","
        games = string.join(all_games)
        # print(games)
        helix_url = http.request(
            "POST", "https://api.igdb.com/v4/games",
            headers={
                "Accept": "application/json",
                "Authorization": "Bearer " + data['access_token'],
                "Client-Id": clientid
            },
            # body="fields category,checksum,created_at,date,game,human,m,platform,region,updated_at,y;where y = 2021;where m = 1;"
            body="fields *; where id = (" + games + "); sort date asc; limit 3;"
        )

        helixdata = json.loads(helix_url.data.decode('utf-8'))
        # selection = data[:10]
        # pprint.pprint(helixdata)
        return f""" New PC releases:
        {helixdata[0]['name']} | Release: {date.fromtimestamp(helixdata[0]['first_release_date'])}
        {helixdata[1]['name']} | Release: {date.fromtimestamp(helixdata[1]['first_release_date'])}
        {helixdata[2]['name']} | Release: {date.fromtimestamp(helixdata[2]['first_release_date'])}
        """
    # Aliases for pcreleases
    pcr = pcreleases
