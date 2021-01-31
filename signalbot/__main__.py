"""Signal bot based on Single-cli."""

import os
import pprint
import json
import time
import docker
import subprocess
import logging
import sys
from distutils.util import strtobool
from message import Message
from botfunctions import SwitchCase


__author__ = "Patrick Blaas <patrick@kite4fun.nl>"
__version__ = "0.1.4"
SIGNALCLIIMAGE = "pblaas/signalcli:latest"

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if not os.environ.get('REGISTEREDNR'):
    raise Exception('Variable REGISTEREDNR is not exported.')

try:
    REGISTEREDNR = os.environ.get('REGISTEREDNR')
except Exception as e:
    raise e

if os.environ.get('DEBUG'):
    DEBUG = bool(strtobool(os.environ.get('DEBUG')))
else:
    DEBUG = False

if os.environ.get('SIGNALEXECUTORLOCAL'):
    SIGNALEXECUTORLOCAL = bool(strtobool(os.environ.get('SIGNALEXECUTORLOCAL')))
else:
    SIGNALEXECUTORLOCAL = True

if os.environ.get('READY'):
    READY = bool(strtobool(os.environ.get('READY')))
else:
    READY = False


def init_program():
    """Initialize start of program."""
    try:

        home = os.environ['HOME']
        if SIGNALEXECUTORLOCAL:
            out = subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-o", "json", "-u", REGISTEREDNR, "receive"], stdout=subprocess.PIPE, text=True)
            output = out.stdout
        else:
            client = docker.from_env()
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
        logging.error("Unable to retrieve container. Please verify container.")
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
                if READY:
                    run_signalcli(messageobject)
                else:
                    logging.info("NOOP due to ready mode set to false.")

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
                if READY:
                    run_signalcli(messageobject)
                else:
                    logging.info("NOOP due to ready mode set to false.")


def run_signalcli(messageobject):
    """Run SignalCLI and return messages."""
    if isinstance(messageobject.getmessage(), str) and messageobject.getmessage().startswith('!'):

        action = SwitchCase(__version__, __author__, SIGNALEXECUTORLOCAL, messageobject.getmessage())
        actionmessage = action.switch(messageobject.getmessage()).replace('"', '')

        if not SIGNALEXECUTORLOCAL:
            client = docker.from_env()
            home = os.environ['HOME']

        if messageobject.getmessage() == "!gif" and actionmessage == "Gif":
            if SIGNALEXECUTORLOCAL:
                subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-u", REGISTEREDNR, "send", "-g", messageobject.getgroupinfo(), "-m", "", "-a", "/tmp/signal/giphy.gif"], stdout=subprocess.PIPE, text=True, shell=False)
            else:
                client.containers.run(
                    SIGNALCLIIMAGE,
                    "-u " + REGISTEREDNR + " send -g " + messageobject.getgroupinfo() + " -a /config/giphy.gif",
                    auto_remove=True,
                    volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
                )
        elif messageobject.getmessage() == "!rand":
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
    logging.info("READY mode " + str(READY))
    while True:
        init_program()
        time.sleep(2)
