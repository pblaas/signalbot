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
from metadata import version, author

__author__ = author
__version__ = version
SIGNALCLIIMAGE = "pblaas/signalcli:latest"

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if 'REGISTEREDNR' not in os.environ:
    logging.error("Mandatory variable not set: REGISTEREDNR")
    exit(1)
else:
    REGISTEREDNR = os.environ.get('REGISTEREDNR')

if 'DEBUG' in os.environ:
    DEBUG = bool(strtobool(os.environ.get('DEBUG')))
else:
    DEBUG = False

if 'SIGNALEXECUTORLOCAL' in os.environ:
    SIGNALEXECUTORLOCAL = bool(strtobool(os.environ.get('SIGNALEXECUTORLOCAL')))
else:
    SIGNALEXECUTORLOCAL = True

if 'READY' in os.environ:
    READY = bool(strtobool(os.environ.get('READY')))
else:
    READY = False

if 'PRIVATECHAT' in os.environ:
    PRIVATECHAT = bool(strtobool(os.environ.get('PRIVATECHAT')))
else:
    PRIVATECHAT = False

if 'GROUPCHAT' in os.environ:
    GROUPCHAT = bool(strtobool(os.environ.get('GROUPCHAT')))
else:
    GROUPCHAT = True

if 'BLACKLIST' in os.environ:
    blacklist = os.environ.get('BLACKLIST').split(',')
else:
    blacklist = []

if 'WHITELIST' in os.environ:
    whitelist = os.environ.get('WHITELIST').split(',')
else:
    whitelist = []


def init_program():
    """Initialize start of program."""
    try:

        homedir = os.environ['HOME']
        if SIGNALEXECUTORLOCAL:
            out = subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-o", "json", "-u", REGISTEREDNR, "receive"], stdout=subprocess.PIPE, text=True)
            output = out.stdout
        else:
            dockerclient = docker.from_env()
            out = dockerclient.containers.run(
                SIGNALCLIIMAGE,
                "-o json -u " + REGISTEREDNR + " receive",
                auto_remove=True,
                volumes={homedir + '/signal': {'bind': '/config', 'mode': 'rw'}}
            )
            output = out.decode('utf-8')
        lines = []
        for line in output.split("\n"):
            lines.append(line)

        for index, value in enumerate(lines):
            if value:
                parse_message(value.replace(u"\u2018", "'").replace(u"\u2019", "'"))

    except docker.errors.NotFound:
        logging.error("Unable to retrieve container. Please verify container.")
    except docker.errors.APIError as e_error:
        logging.error("Docker API error due to: " + e_error)


def parse_message(value):
    """Create  message object from input."""
    res = json.loads(value)
    if DEBUG:
        pprint.pprint(res)

    # Messages send by the registered number itself.
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
                    if group_not_in_blacklist(messageobject, blacklist) and group_in_whitelist(messageobject, whitelist):
                        run_signalcli(messageobject)
                    else:
                        logging.info("Group" + messageobject.getgroupinfo() + " is in the blacklist OR not in whitelist.")
                else:
                    logging.info("NOOP due to ready mode set to false.")
            if PRIVATECHAT and "groupInfo" not in res['envelope']['syncMessage']['sentMessage']:
                messageobject = Message(
                    res['envelope']['source'],
                    res['envelope']['syncMessage']['sentMessage']['message'],
                    None,
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

    # Messages send by others.
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
                    if group_not_in_blacklist(messageobject, blacklist) and group_in_whitelist(messageobject, whitelist):
                        run_signalcli(messageobject)
                    else:
                        logging.info("Group" + messageobject.getgroupinfo() + " is in the blacklist OR not in whitelist.")
                else:
                    logging.info("NOOP due to ready mode set to false.")
            if PRIVATECHAT and "groupInfo" not in res['envelope']['dataMessage']:
                messageobject = Message(
                    res['envelope']['source'],
                    res['envelope']['dataMessage']['message'],
                    None,
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
    global client, home
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
        elif messageobject.getmessage() == "!xkcd" and actionmessage == "xkcd":
            if SIGNALEXECUTORLOCAL:
                subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-u", REGISTEREDNR, "send", "-g", messageobject.getgroupinfo(), "-m", "", "-a", "/tmp/signal/image.png"], stdout=subprocess.PIPE, text=True, shell=False)
            else:
                client.containers.run(
                    SIGNALCLIIMAGE,
                    "-u " + REGISTEREDNR + " send -g " + messageobject.getgroupinfo() + " -a /config/image.png",
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
            # if SIGNALEXECUTORLOCAL:
            #    subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-u", REGISTEREDNR, "send", "-g", messageobject.getgroupinfo(), "-m", actionmessage], stdout=subprocess.PIPE, text=True, check=True)
            # else:
            signal_cli_send(REGISTEREDNR, PRIVATECHAT, GROUPCHAT, SIGNALEXECUTORLOCAL, messageobject, actionmessage)
            # if PRIVATECHAT:
            #     client.containers.run(
            #         SIGNALCLIIMAGE,
            #         "-u " + REGISTEREDNR + " send  -m " + "\"" + actionmessage + "\"" + " " + messageobject.getsource(),
            #         auto_remove=True,
            #         volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
            #     )
            # else:
            #     client.containers.run(
            #         SIGNALCLIIMAGE,
            #         "-u " + REGISTEREDNR + " send -g " + messageobject.getgroupinfo() + " -m " + "\"" + actionmessage + "\"",
            #         auto_remove=True,
            #         volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
            #     )


def signal_cli_send(registerednr, privatechat, groupchat, signalexecutorlocal, messageobject, actionmessage):
    # check if messageobject contains groupinfo
    # check if PRIVATECHAT is True

    if messageobject.getgroupinfo() is None and privatechat:
        # this is a private one on one chat
        target_param = messageobject.getsource()

        if signalexecutorlocal:
            subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-u", REGISTEREDNR, "send",
                            target_param, "-m", actionmessage], stdout=subprocess.PIPE, text=True,
                           check=True)
        else:
            client.containers.run(
                SIGNALCLIIMAGE,
                "-u " + registerednr + " send -m " + "\"" + actionmessage + "\" " + target_param,
                auto_remove=True,
                volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
            )
    else:
        if groupchat:
            # this is a group chat
            target_param = "-g " + messageobject.getgroupinfo()

            if signalexecutorlocal:
                subprocess.run(["/signal/bin/signal-cli", "--config", "/config", "-u", REGISTEREDNR, "send",
                                target_param, "-m", actionmessage], stdout=subprocess.PIPE, text=True,
                               check=True)
            else:
                client.containers.run(
                    SIGNALCLIIMAGE,
                    "-u " + registerednr + " send -m " + "\"" + actionmessage + "\" " + target_param,
                    auto_remove=True,
                    volumes={home + '/signal': {'bind': '/config', 'mode': 'rw'}}
                )


def group_not_in_blacklist(messageobject, blist):
    for groupid in blist:
        if groupid == messageobject.getgroupinfo():
            return False
    return True


def group_in_whitelist(messageobject, wlist):
    if len(wlist) > 0:
        for groupid in wlist:
            if groupid == messageobject.getgroupinfo():
                return True
        return False
    else:
        return True


if __name__ == '__main__':

    logging.info("Signal bot " + __version__ + " started.")
    logging.info("Debug " + str(DEBUG))
    logging.info("Local Executor " + str(SIGNALEXECUTORLOCAL))
    logging.info("Ready " + str(READY))
    logging.info("Private chat " + str(PRIVATECHAT))
    logging.info("Group Chat " + str(GROUPCHAT))
    logging.info("Blacklists: " + str(blacklist))
    logging.info("Whitelits: " + str(whitelist))
    while True:
        init_program()
        time.sleep(2)
