"""Signal bot based on Single-cli."""

import os
import pprint
import json
import time
import docker
import subprocess
import logging
import sys
from message import Message
from botfunctions import SwitchCase


__author__ = "Patrick Blaas <patrick@kite4fun.nl>"
__version__ = "0.0.11"
REGISTEREDNR = "+31630030905"
SIGNALCLIIMAGE = "pblaas/signalcli:latest"
DEBUG = True
SIGNALEXECUTORLOCAL = False
PASSIVE = True

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def init_program():
    """Initialize start of program."""
    try:
        home = os.environ['HOME']
        if SIGNALEXECUTORLOCAL is False:
            client = docker.from_env()
        if SIGNALEXECUTORLOCAL:
            out = subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-o", "json", "-u", REGISTEREDNR, "receive"], stdout=subprocess.PIPE, text=True)
            output = out.stdout
        else:
            out = client.containers.run(
                SIGNALCLIIMAGE,
                "-o json -u " + REGISTEREDNR + " receive",
                auto_remove=True,
                volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
            )
            output = out.decode('utf8')
        lines = []
        for line in output.split("\n"):
            lines.append(line)

        for index, value in enumerate(lines):
            if value:
                parse_message(value)

    except docker.errors.NotFound:
        logging.error("Unable to retreive container. Please verify container.")
    except docker.errors.APIError as e_error:
        logging.error("Docker API error due to: " + e_error)


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
                    res['envelope']['syncMessage']['sentMessage']['groupInfo']['groupId'],
                    res['envelope']['syncMessage']['sentMessage']['timestamp']
                )
                if DEBUG:
                    logging.info(pprint.pprint(res))
                    logging.info(messageobject.getsource())
                    logging.info(messageobject.getgroupinfo())
                    logging.info(messageobject.getmessage())
                if PASSIVE is False:
                    run_signalcli(messageobject)
                else:
                    logging.info("Passive mode active.")

    if "dataMessage" in res['envelope']:
        if "message" in res['envelope']['dataMessage']:
            if "groupInfo" in res['envelope']['dataMessage']:
                messageobject = Message(
                    res['envelope']['source'],
                    res['envelope']['dataMessage']['message'],
                    res['envelope']['dataMessage']['groupInfo']['groupId'],
                    res['envelope']['dataMessage']['timestamp']
                )
                if DEBUG:
                    logging.info(pprint.pprint(res))
                    logging.info(messageobject.getsource())
                    logging.info(messageobject.getgroupinfo())
                    logging.info(messageobject.getmessage())
                if PASSIVE is False:
                    run_signalcli(messageobject)
                else:
                    logging.info("Passive mode active.")


def run_signalcli(messageobject):
    """Run SignalCLI and return messages."""
    if isinstance(messageobject.getmessage(), str) and messageobject.getmessage().startswith('!'):

        action = SwitchCase(__version__, __author__, SIGNALEXECUTORLOCAL, messageobject.getmessage())
        actionmessage = action.switch(messageobject.getmessage()).replace('"', '')

        if SIGNALEXECUTORLOCAL is False:
            client = docker.from_env()
            home = os.environ['HOME']

        if messageobject.getmessage() == "!gif":
            if SIGNALEXECUTORLOCAL:
                subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-u", REGISTEREDNR, "send", "-g", messageobject.getgroupinfo(), "-m", "", "-a", "/tmp/signal/giphy.gif"], stdout=subprocess.PIPE, text=True, shell=False)
            else:
                client.containers.run(
                    SIGNALCLIIMAGE,
                    "-u " + REGISTEREDNR + " send -g " + messageobject.getgroupinfo() + " -a /config/giphy.gif",
                    auto_remove=True,
                    volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
                )
        elif messageobject.getmessage() == "!random":
            if SIGNALEXECUTORLOCAL:
                subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "updateGroup", "-g", messageobject.getgroupinfo(), "-n", actionmessage], stdout=subprocess.PIPE, text=True, check=True)
            else:
                client.containers.run(
                    SIGNALCLIIMAGE,
                    "updateGroup -g " + messageobject.getgroupinfo() + " -n " + "\"" + actionmessage + "\"",
                    auto_remove=True,
                    volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
                )
        elif messageobject.getmessage() == "!me":
            if SIGNALEXECUTORLOCAL:
                subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-u", REGISTEREDNR, "sendReaction", "-g", messageobject.getgroupinfo(), "-a", messageobject.getsource(), "-t", messageobject.gettimestamp(), "-e", actionmessage], stdout=subprocess.PIPE, text=True, check=True)
            else:
                client.containers.run(
                    SIGNALCLIIMAGE,
                    "-u " + REGISTEREDNR + " sendReaction -g " + messageobject.getgroupinfo() + " -a " + messageobject.getsource() + " -t " + messageobject.gettimestamp() + " -e " + actionmessage,
                    auto_remove=True,
                    volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
                )
        else:
            if SIGNALEXECUTORLOCAL:
                subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-u", REGISTEREDNR, "send", "-g", messageobject.getgroupinfo(), "-m", actionmessage], stdout=subprocess.PIPE, text=True, check=True)
            else:
                client.containers.run(
                    SIGNALCLIIMAGE,
                    "-u " + REGISTEREDNR + " send -g " + messageobject.getgroupinfo() + " -m " + "\"" + actionmessage + "\"",
                    auto_remove=True,
                    volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
                )


if __name__ == '__main__':

    logging.info("Signal bot " + __version__ + " started.")
    logging.info("Debug is " + str(DEBUG))
    logging.info("Local Signal executor " + str(SIGNALEXECUTORLOCAL))
    logging.info("Passive mode  " + str(PASSIVE))
    while True:
        init_program()
        time.sleep(2)
