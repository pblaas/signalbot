import random
import urllib3
import json
import pprint

""" Model for Messages """

class Message:

    def __init__(self,source,message,groupinfo,author,version):
        self._source = source
        self._message = message
        self._groupinfo = groupinfo
        self._author = author
        self._version = version

    def getGroupinfo(self):
        return self._groupinfo

    def getMessage(self):
        return self._message

    def getSource(self):
        return self._source

    def getVersion(self):
        return "SignalCLI bot version: " + self._version + " by " + self._author

    def getHelp(self):
        return """Available commands:
        !help
        !version
        !random
        !flip
        !chuck
        !gif
        """

    def getRandom(self):
        return random.randrange(1000)

    def getFlip(self):
        return random.choice(['Heads', 'Tails'])

    def getChuck(self):
        http = urllib3.PoolManager()
        r = http.request('GET', 'https://api.chucknorris.io/jokes/random')
        chuck = json.loads(r.data.decode('utf-8'))
        pprint.pprint(chuck)
        return chuck['value']

    def getGif(self):
        http = urllib3.PoolManager()
        r = http.request('GET', 'https://api.giphy.com/v1/gifs/random?api_key=elRcLdk25G3cllhDMki4ZIKLMxKqRPSW&tag=&rating=g')
        gif = json.loads(r.data.decode('utf-8'))
        #return (gif['data']['image_original_url'])
        url = "https://i.giphy.com/media/" + gif['data']['id'] + "/giphy.gif"
        r = http.request('GET', url, preload_content=False)

        with open("/config/giphy.gif", 'wb') as out:
            while True:
                data = r.read(chunk_size)
                if not data:
                    break
                out.write(data)
        r.release_conn()

        return("https://i.giphy.com/media/" + gif['data']['id'] + "/giphy.gif")