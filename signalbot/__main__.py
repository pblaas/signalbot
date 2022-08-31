"""Signal bot based on Single-cli."""

import os
import pprint
import json
import time
import docker
import subprocess
import shlex
import logging
import sys
import pika
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

if 'AMQPSERVERHOST' not in os.environ:
    logging.error("Mandatory variable not set: AMQPSERVERHOST")
    exit(1)
else:
    amqpserverhost = os.environ.get('AMQPSERVERHOST')


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
                volumes={homedir + '/poller': {'bind': '/config', 'mode': 'rw'}}
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

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=amqpserverhost))
    channel = connection.channel()

    channel.queue_declare(queue='signalbot')
    channel.basic_publish(exchange='', routing_key='signalbot', body=json.dumps(res), properties=pika.BasicProperties(content_type='application/json'))
    connection.close()

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
