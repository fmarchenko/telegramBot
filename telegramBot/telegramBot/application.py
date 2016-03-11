#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Mar 10, 2016"

from flask import Flask, request, jsonify
from telegramBot.bot_commands import Commands
from telegramBot.commands import send_reply
from telegramBot.queue_commands import MemoryQueueCommands
import settings

app = Flask(__name__)
CMD = Commands()
mq = MemoryQueueCommands()

def not_found(message, args):
    app.logger.error("Handler for message\t%s\tnot found!" % message)
    return ""

@app.route("/", methods=("GET", "POST"))
def index_handler():
    app.logger.debug("Got request:\n%s" % request.get_data())
    update = request.get_json()
    message = update['message']
    text = message.get('text')

    if text:
        response = {}
        app.logger.info("MESSAGE\t%s\t%s" % (message['chat']['id'], text))

        if text[0] == '/':
            # Clear queue for this chat
            mq.pop(message['chat']['id'])
            try:
                command, args = text.split(" ", 1)
            except ValueError:
                command = text.strip()
                args = None
            response = CMD.get(command, not_found)(message, *args.split() if args else ())
            app.logger.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
            send_reply(response)
        else:
            chat_id, cmd = mq.pop(message['chat']['id'])
            if cmd:
                response = cmd(message)
                app.logger.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                send_reply(response)

    return jsonify(response)