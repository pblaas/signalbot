# signal-cli


## Create intial config
```
mkdir $HOME/signal
docker run -v $HOME/signal:/config --rm -it pblaas/signal-cli:latest link
```


Paste entire tsdevice:/? string in https://www.nayuki.io/page/qr-code-generator-library and read with Signal APP to add connected device.

## Start messaging
After device is connected you can start sending messages:
```
docker run -v $HOME/signal:/config --rm -it pblaas/signal-cli:latest -u YOURREGISTEREDNR send RECEIVER -m "your message"
```


## show CLI help
```
docker run -v $HOME/signal:/config --rm -it pblaas/signal-cli:latest -h
```

## having some fun
```
echo `curl --silent https://api.chucknorris.io/jokes/random | jq '. | .value'` | docker run -v $HOME/signal:/config --rm -i signal:dev -u +31630030905 send --g "2SElh8hai/NQTSNaBOpHKBc0BbYE90l1iQyXAQzfeoE="
```

## bot ideas
* !jokes - show random joke
* !gifs  - show random gif
* !weather - show weather 
* !news - parse latest news from site x
* !me - return with random reply
* !version - show version
* !commands - show available commands
* !ai - return interesting AI facts?
* !hal - hal quotes from 2001 a space oddysee

