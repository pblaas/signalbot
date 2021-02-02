"""Simple Twitch module."""

import json
import urllib3
# import pprint
from datetime import datetime, date


def twitch():
    """Twitch example function."""
    CLIENTID = "xu5vir3u0bdxub6q8r3qq50o9t0cik"
    CLIENTSECRET = "ocqwwmooe78inxki55ugbnld1uz9rl"

    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).split(".")[0]

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
        "POST", "https://api.igdb.com/v4/release_dates",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer " + data['access_token'],
            "Client-Id": CLIENTID
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
            "Client-Id": CLIENTID
        },
        # body="fields category,checksum,created_at,date,game,human,m,platform,region,updated_at,y;where y = 2021;where m = 1;"
        body="fields *; where id = (" + games + "); sort date asc; limit 3;"
    )

    helixdata = json.loads(helix_url.data.decode('utf-8'))
    # selection = data[:10]
    # pprint.pprint(helixdata)
    print(f""" New PC releases:
    {helixdata[0]['name']} | Release: {date.fromtimestamp(helixdata[0]['first_release_date'])}
    {helixdata[1]['name']} | Release: {date.fromtimestamp(helixdata[1]['first_release_date'])}
    {helixdata[2]['name']} | Release: {date.fromtimestamp(helixdata[2]['first_release_date'])}
    """)


twitch()
