"""Simple test script."""
import urllib3
import json
import pprint
import shutil
import subprocess


__author__ = "Patrick Blaas <patrick@kite4fun.nl>"
__version__ = "0.0.4"
REGISTEREDNR = "+31630030905"
SIGNALCLIIMAGE = "pblaas/signalcli:latest"
DEBUG = True
SIGNALEXECUTORLOCAL = True

http = urllib3.PoolManager()
req_gif = http.request('GET', 'https://api.giphy.com/v1/gifs/random?api_key=elRcLdk25G3cllhDMki4ZIKLMxKqRPSW&tag=&rating=pg-13')
gif = json.loads(req_gif.data.decode('utf-8'))
pprint.pprint(gif)
url = "https://i.giphy.com/media/" + gif['data']['id'] + "/giphy.gif"


with open("/tmp/signal/giphy.gif", 'wb') as out:
    r = http.request('GET', url, preload_content=False)
    shutil.copyfileobj(r, out)

# --config /config -u +31630030905 send -g OcX1j1sAF3e8yGDuFxd/sC+XKJL8TbBTOhCREc4CNXI= -a /tmp/signal/giphy.gif
print("Start gif process:")
# out = subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-u", REGISTEREDNR, "send", "-g", messageobject.getgroupinfo(), "-a", "/tmp/signal/giphy.gif"], stdout=subprocess.PIPE, text=True, shell=True)
input = "--config /config -u " + REGISTEREDNR + " send -g " + " OcX1j1sAF3e8yGDuFxd/sC+XKJL8TbBTOhCREc4CNXI= " + " -a /tmp/signal/giphy.gif"
print(input)
out = subprocess.run(["/signal/bin/signal-cli", input], stdout=subprocess.PIPE, text=True, shell=True)
print(out.stdout)
