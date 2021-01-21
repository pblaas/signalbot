""" Signal bot based on Single-cli """

import os
import pprint
import json
import time
import docker
from message import Message
from botfunctions import getversion, getchuck, getgif, gethelp, getrandom, getflip

__author__ = "Patrick Blaas <patrick@kite4fun.nl>"
__version__ = "0.0.2"
REGISTEREDNR = "+31630030905"
SIGNALCLIIMAGE = "pblaas/signalcli:latest"


def init_program():
    """ Initial start of program """
    try:
        home = os.environ['HOME']
        client = docker.from_env()
        output = client.containers.run(
            SIGNALCLIIMAGE,
            "-o json -u " + REGISTEREDNR + " receive",
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
    except docker.errors.APIError as e_error:
        print("Docker API error due to: " + e_error)


def parse_message(value):
    """ Creating message object from input """
    res = json.loads(value)
    pprint.pprint(res)
    if "syncMessage" in res['envelope']:
        if "sentMessage" in res['envelope']['syncMessage']:
            if "groupInfo" in res['envelope']['syncMessage']['sentMessage']:
                messageobject = Message(
                    res['envelope']['source'],
                    res['envelope']['syncMessage']['sentMessage']['message'],
                    res['envelope']['syncMessage']['sentMessage']['groupInfo']['groupId']
                    )
                pprint.pprint(res)
                print(messageobject.getsource())
                print(messageobject.getgroupinfo())
                print(messageobject.getmessage())
                run_signalcli(messageobject)

    if "dataMessage" in res['envelope']:
        if "message" in res['envelope']['dataMessage']:
            if "groupInfo" in res['envelope']['dataMessage']:
                messageobject = Message(
                    res['envelope']['source'],
                    res['envelope']['dataMessage']['message'],
                    res['envelope']['dataMessage']['groupInfo']['groupId']
                    )
                pprint.pprint(res)
                print(messageobject.getsource())
                print(messageobject.getgroupinfo())
                print(messageobject.getmessage())
                run_signalcli(messageobject)


def run_signalcli(messageobject):
    """ Run SignalCLI and return messages """
    def xyz(x_input):
        """ Switcher function used as case statement """
        switcher = {
            '!version': getversion(__version__, __author__),
            '!help': gethelp(),
            '!random': str(getrandom()),
            '!flip': getflip(),
            '!chuck': getchuck(),
            '!gif': getgif()
        }
        return switcher.get(x_input, "Oops! Invalid Option")

    if isinstance(messageobject.getmessage(), str) and messageobject.getmessage().startswith('!'):
        actionmessage = xyz(messageobject.getmessage())

        home = os.environ['HOME']
        client = docker.from_env()

        if messageobject.getmessage() == "!gif":
            client.containers.run(
                SIGNALCLIIMAGE,
                "-u " + REGISTEREDNR + " send -g " + messageobject.getgroupinfo() + " -m " + actionmessage + " -a /config/giphy.gif",
                auto_remove=True,
                volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
                )
        else:
            client.containers.run(
                SIGNALCLIIMAGE,
                "-u " + REGISTEREDNR + " send -g " + messageobject.getgroupinfo() + " -m " + "\"" + actionmessage + "\"",
                auto_remove=True,
                volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
                )


if __name__ == '__main__':

    print("Signal bot " + __version__ + " started.")
    while True:
        init_program()
        time.sleep(2)
