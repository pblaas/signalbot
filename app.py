"""Signal bot based on Single-cli."""

import os
import pprint
import json
import time
import docker
from message import Message
from botfunctions import SwitchCase

__author__ = "Patrick Blaas <patrick@kite4fun.nl>"
__version__ = "0.0.3"
REGISTEREDNR = "+31630030905"
SIGNALCLIIMAGE = "pblaas/signalcli:latest"
DEBUG = True


def init_program():
    """Initialize start of program."""
    try:
        home = os.environ['HOME']
        client = docker.from_env()
        output = client.containers.run(
            SIGNALCLIIMAGE,
            "-o json -u " + REGISTEREDNR + " receive",
            auto_remove=True,
            volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
        )
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
    """Create  message object from input."""
    res = json.loads(value)
    if DEBUG:
        pprint.pprint(res)
    if "syncMessage" in res['envelope']:
        if "sentMessage" in res['envelope']['syncMessage']:
            if "groupInfo" in res['envelope']['syncMessage']['sentMessage']:
                messageobject = Message(
                    res['envelope']['source'],
                    res['envelope']['syncMessage']['sentMessage']['message'],
                    res['envelope']['syncMessage']['sentMessage']['groupInfo']['groupId']
                )
                if DEBUG:
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
                if DEBUG:
                    pprint.pprint(res)
                    print(messageobject.getsource())
                    print(messageobject.getgroupinfo())
                    print(messageobject.getmessage())
                run_signalcli(messageobject)


def run_signalcli(messageobject):
    """Run SignalCLI and return messages."""
    if isinstance(messageobject.getmessage(), str) and messageobject.getmessage().startswith('!'):

        action = SwitchCase(__version__, __author__)
        actionmessage = action.switch(messageobject.getmessage()).replace('"', '')

        home = os.environ['HOME']
        client = docker.from_env()

        if messageobject.getmessage() == "!gif":
            client.containers.run(
                SIGNALCLIIMAGE,
                "-u " + REGISTEREDNR + " send -g " + messageobject.getgroupinfo() + " -a /config/giphy.gif",
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
    print("Debug is " + str(DEBUG))
    while True:
        init_program()
        time.sleep(1)
