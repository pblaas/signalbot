import docker
import os
import pprint
import json 
import ast 
from message import Message
import time


# run the docker command with paramters
#docker run -v $HOME/signal:/config --rm -it pblaas/signal-cli:latest -o json -u YOURREGISTEREDNR receive

__author__ = "Patrick Blaas <patrick@kite4fun.nl>"
__version__ = "0.0.1"
registerednr="+31630030905"
signalcliimage="pblaas/signalcli:latest"

# show env vars
#pprint.pprint(dict(os.environ, width = 1))

def init_program():
  
    try:
        home = os.environ['HOME']
        client = docker.from_env()
        output = client.containers.run(
            signalcliimage, 
            "-o json -u " + registerednr + " receive",
            auto_remove=True,
            volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
            )
        # print(output)
        lines = []
        for line in output.decode('utf8').split("\n"):
            lines.append(line)
            
        for index, value in enumerate(lines):
            if value:
                parse_message(value)
               

    except docker.errors.NotFound: 
        print("Unable to retreive container. Please verify container.")
    except docker.errors.APIError as e:
        print("Docker API error due to: " + e)


def parse_message(value):
    res = json.loads(value)
    pprint.pprint(res)
    if "syncMessage" in res['envelope']:
        if "sentMessage" in res['envelope']['syncMessage']:
            if "groupInfo" in res['envelope']['syncMessage']['sentMessage']:
                m = Message(
                    res['envelope']['source'],
                    res['envelope']['syncMessage']['sentMessage']['message'],
                    res['envelope']['syncMessage']['sentMessage']['groupInfo']['groupId'],
                    __author__,
                    __version__
                    )
                pprint.pprint(res)
                print(m.getSource())
                print(m.getGroupinfo())
                print(m.getMessage())
                #print(m.getVersion())
                run_signalcli(m)

    if "dataMessage" in res['envelope']:
        if "message" in res['envelope']['dataMessage']:
            if "groupInfo" in res['envelope']['dataMessage']:
                m = Message(
                    res['envelope']['source'],
                    res['envelope']['dataMessage']['message'],
                    res['envelope']['dataMessage']['groupInfo']['groupId'],
                    __author__,
                    __version__
                    )
                pprint.pprint(res)
                print(m.getSource())
                print(m.getGroupinfo())
                print(m.getMessage())
                #print(m.getVersion())
                run_signalcli(m)


def run_signalcli(m):

    #case statement to configure actionmessage

    def xyz(x):
        switcher = {
            '!version': m.getVersion(),
            '!help': m.getHelp(),
            '!random' : str(m.getRandom()),
            '!flip': m.getFlip(),
            '!chuck': m.getChuck(),
            '!gif': m.getGif()
        }
        return switcher.get(x,"Oops! Invalid Option")

    if isinstance(m.getMessage(),str) and m.getMessage().startswith('!'):
        actionmessage=xyz(m.getMessage())

        home = os.environ['HOME']
        client = docker.from_env()
        client.containers.run(
            signalcliimage, 
            "-u " + registerednr + " send -g " + m.getGroupinfo() + " -m " + "\"" + actionmessage + "\"",
            auto_remove=True,
            volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
            )

if __name__ == '__main__':

    while True: 
        init_program() 
        time.sleep( 2 )