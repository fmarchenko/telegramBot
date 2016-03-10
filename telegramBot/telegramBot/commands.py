#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Mar 10, 2016"

import requests
import time
import logging
import json

from . import settings, models

from django.core.management import call_command
from requests.exceptions import ConnectionError
from IPython import embed

def migrate():
    call_command('makemigrations', 'telegramBot')
    # call_command('sqlmigrate', 'loader', "0001_initial")
    call_command('migrate')


def shell():
    embed()


def puller():
    try:
        last, create = models.LastUpdate.objects.get_or_create(pk=1, update_id=0)
        while True:
            try:
                r = requests.get(settings.settings.API_URL + 'getUpdates' + '?offset=%d' % (last.update_id + 1))
                if r.status_code == 200:
                    for message in r.json()["result"]:
                        last.update_id = int(message["update_id"])
                        requests.post("http://%s:%d/" % (settings.BOT_HOST, settings.BOT_PORT),
                                      data=json.dumps(message),
                                      headers={'Content-type': 'application/json',
                                               'Accept': 'text/plain'}
                        )
                    time.sleep(3)
                else:
                    logging.warning("FAIL " + r.text)
            except Exception as ex:
                logging.error(ex)
    except KeyboardInterrupt:
        exit(0)