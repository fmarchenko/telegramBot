#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Mar 10, 2016"

from telegramBot.queue_commands import MemoryQueueCommands


class Commands(object):
    _instance = None
    _commands = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Commands, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __iter__(self):
        return self._commands.__iter__()

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
        commands = filter(lambda x: key in x.synonyms or key == x.command, self._commands.keys())
        if commands:
                return self._commands.get(commands[0], default)
        return default or None


    @staticmethod
    def register_class(cls):
        cls_obj = cls()
        Commands().set(cls_obj, cls_obj.run)
        # Commands().set(cls, cls.run)
        return cls


def help_message(message, *args):
    response = {'chat_id': message['chat']['id']}
    result = [
        "Hey, %s!" % message['from'].get('first_name'),
        "I can accept only these commands:"
    ]
    for command in Commands():
        result.append(str(command))
    response['text'] = "\n".join(result)
    return response


class BaseBotCommand(object):
    command = ""  # Command key, start with "/". Example "/help"
    synonyms = ()  # Synonyms keys for command. Example message: /help (/h, /start) for ("/h", "/start")
    help = ""  # Description for command. Example message: /help - Hi! This is description for this command for "Hi! This is description for this command"

    def __str__(self):
        """
        Method for compile string message with command name, synonyms and description
        :return:
        """
        if self.synonyms:
            return "%s (%s)\t- %s" % (self.command, ", ".join(self.synonyms), self.help)
        return "%s\t- %s" % (self.command, self.help)

    def __repr__(self):
        return self.command

    def run(self, message, *args):
        """

        :param message:
        :param args:
        :return:
        """
        response = {'chat_id': message['chat']['id'], 'text': ""}
        return response


@Commands.register_class
class HelpCommand(BaseBotCommand):
    command = "/help"
    synonyms = ("/h", "/start")
    help = "It is this that command! ;-)"

    def run(self, message, *args):
        response = {'chat_id': message['chat']['id']}
        result = [
            "Hey, %s!" % message['from'].get('first_name'),
            "I can accept only these commands:"
        ]
        for command in Commands():
            result.append(str(command))
        response['text'] = "\n".join(result)
        return response


@Commands.register_class
class HiCommand(BaseBotCommand):
    command = "/hi"
    synonyms = ()
    help = "Test for waiting answer command"

    def run(self, message, *args):
        response = {'chat_id': message['chat']['id']}
        result = [
            "Hi! What is you name?"
        ]
        response['text'] = "\n".join(result)
        mq = MemoryQueueCommands()
        mq.push(message['chat']['id'], self.step2)
        return response

    def step2(self, message, *args):
        response = {'chat_id': message['chat']['id']}
        result = [
            "Hi! %s!" % message['text'],
            "Nice to meet you!"
        ]
        response['text'] = "\n".join(result)
        return response


def test():
    import json
    import os
    updates = {}
    with open(os.path.join(os.path.dirname(__file__), "fixturies/testUpdate.json"), "r") as f:
        updates = json.load(f)

    for message in updates.get("result", []):
        print help_message(message.get("message"))

if __name__ == '__main__':
    test()