#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Mar 11, 2016"

from copy import deepcopy


class BaseQueueCommands(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BaseQueueCommands, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def push(self, key, func):
        """
        Function for pop function to queue with key
        :param key: Key of function on queue
        :type key: (int, str)
        :param func: Function for execute
        :type func: object
        :return: Boolean result
        :rtype: bool
        """
        pass

    def pop(self, key):
        """
        Function for pop function with key from queue
        :param key: Key of function on queue
        :type key: (int, str)
        :return: Index and Function for execute
        :rtype: tuple
        """
        pass


class MemoryQueueCommands(BaseQueueCommands):
    _queue = []
    _queue_commands = {}

    def push(self, key, func):
        try:
            self._queue.append(key)
            self._queue_commands[len(self._queue)-1] = func
            return True
        except:
            raise
            return False

    def pop(self, key):
        try:
            idx = self._queue.index(key)
            func = deepcopy(self._queue_commands[idx])
            del(self._queue[idx])
            del(self._queue_commands[idx])
            return idx, func
        except ValueError:
            return None, None
        except:
            raise


def test():
    mq = MemoryQueueCommands()
    print mq.push(1, 10)
    print mq._queue, '\t', mq._queue_commands
    print mq.push(3, 30)
    print mq._queue, '\t', mq._queue_commands
    print mq.push(2, 20)
    print mq._queue, '\t', mq._queue_commands
    print mq.push(3, lambda x: 31)
    print mq._queue, '\t', mq._queue_commands
    print mq.pop(3)
    print mq._queue, '\t', mq._queue_commands
    print mq.pop(4)
    print mq._queue, '\t', mq._queue_commands
    print mq.pop(3)
    print mq._queue, '\t', mq._queue_commands

if __name__ == '__main__':
    test()