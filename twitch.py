"""Simple Twitch module."""

import json
import urllib3
import pprint

def twitch(string):
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
    pprint.pprint(data)


    helix_url = http.request(
        "GET", "https://api.twitch.tv/helix/games/top", 
        headers={
            "Authorization": "Bearer " + data['access_token'],
            "Client-Id": CLIENTID
        })
    #print(helix_url)
    helixdata = json.loads(helix_url.data.decode('utf-8'))
    # selection = data[:10]
    #pprint.pprint(helixdata)
    #print("String: " + string.split()[1])
    print(helixdata['data'][1]['name'])
twitch("twitch second third")