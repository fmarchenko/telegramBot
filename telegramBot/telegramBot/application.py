#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Mar 10, 2016"

from flask import Flask, request, jsonify
from telegramBot.bot_commands import Commands

app = Flask(__name__)
CMD = Commands()

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
        app.logger.info("MESSAGE\t%s\t%s" % (message['chat']['id'], text))

        if text[0] == '/':
            try:
                command, args = text.split(" ", 1)
            except ValueError:
                command = text.strip()
                args = None
            response = CMD.get(command, not_found)(message, args)
            app.logger.info("REPLY\t%s\t%s" % (message['chat']['id'], response))

    return jsonify(update)