import docker
import os
import pprint
import json 
import ast 
from message import Message


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
    m = Message(
         res['envelope']['source'],res['envelope']['syncMessage']['sentMessage']['message'],res['envelope']['syncMessage']['sentMessage']['groupInfo']['groupId']
         )
    #pprint.pprint(res)
    print(m.getSource())
    print(m.getGroupinfo())
    print(m.getMessage())


def run_signalcli(groupid,action):

    #case statement to configure actionmessage

    home = os.environ['HOME']
    client = docker.from_env()
    output = client.containers.run(
        signalcliimage, 
        "-o json -u " + registerednr + " send -g " + groupid + " -m " + actionmessage
        auto_remove=True,
        volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
        )

if __name__ == '__main__':
    init_program() 