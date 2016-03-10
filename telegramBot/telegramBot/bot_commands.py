#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Mar 10, 2016"


class Commands(object):
    _instance = None
    _commands = {}
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Commands, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def register(name):
        def dec(func):
            cmd = Commands()
            cmd.set(name, func)
            return func
        return dec

    def set(self, key, value):
        self._commands[key] = value

    def get(self, key, default):
        return self._commands.get(key, default)


@Commands.register("/help")
def help_message(message, args):
    response = {'chat_id': message['chat']['id']}
    result = [
        "Hey, %s!" % message['from'].get('first_name'),
        "\rI can accept only these commands:"
    ]

    for command in Commands:
        result.append(command)
    response['text'] = "\n\t".join(result)
    return response