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

api = requests.Session()
logging.basicConfig(level=logging.INFO)

def migrate():
    call_command('makemigrations', 'telegramBot')
    # call_command('sqlmigrate', 'loader', "0001_initial")
    call_command('migrate')


def shell():
    embed()


def send_reply(response):
    logging.info('Sending: %s' % response)
    if 'text' in response:
        request = api.post(settings.API_URL + "sendMessage", data=response)
        if not request.status_code == 200:
            return False
        return request.json()['ok']
    return False


def puller():
    last, create = models.LastUpdate.objects.get_or_create(pk=1, defaults={"update_id": 0})
    while True:
        try:
            data = {'offset': last.update_id + 1, 'limit': 5, 'timeout': 0}

            try:
                request = requests.post(settings.API_URL + 'getUpdates', data=data)
            except Exception as ex:
                logging.error("%s\t%s with data %s" % (ex, settings.API_URL + 'getUpdates', data))
                continue

            if not request.status_code == 200:
                logging.error('FAIL ' + request.text)
                continue
            if not request.json()['ok']:
                logging.error('FAIL ' + request.text)
                continue

            for update in request.json()["result"]:
                last.update_id = int(update["update_id"])

                if not 'message' in update or not 'text' in update['message']:
                    logging.error('Unknown update: %s' % update)
                    continue
                from_id = update['message']['chat']['id']
                name = update['message']['chat']['username']
                if from_id <> settings.BOT_ADMIN_ID:
                    send_reply({'chat_id': from_id, 'text': "You're not autorized to use me!"})
                    logging.info('Unautorized: %s' % update)
                    continue
                #TODO
                try:
                    logging.info('Message (id%s) from %s (id%s): %s' % (last.update_id, name, from_id, update['message']['text']))
                    requests.post(
                        "http://%s:%d/" % (settings.BOT_HOST, settings.BOT_PORT),
                        data=json.dumps(update),
                        headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
                    )
                except Exception as ex:
                    logging.error("%s\t%s with data %s" % (ex, "http://%s:%d/" % (settings.BOT_HOST, settings.BOT_PORT), update))
                    continue

        except KeyboardInterrupt:
            logging.info('Прервано пользователем..')
            break
        time.sleep(settings.BOT_INTERVAL)

    # try:
    #     last, create = models.LastUpdate.objects.get_or_create(pk=1, update_id=0)
    #     while True:
    #         try:
    #             r = requests.get(settings.API_URL + 'getUpdates' + '?offset=%d' % (last.update_id + 1))
    #             if r.status_code == 200:
    #                 for message in r.json()["result"]:
    #                     last.update_id = int(message["update_id"])
    #                     requests.post("http://%s:%d/" % (settings.BOT_HOST, settings.BOT_PORT),
    #                                   data=json.dumps(message),
    #                                   headers={'Content-type': 'application/json',
    #                                            'Accept': 'text/plain'}
    #                     )
    #                 time.sleep(1)
    #             else:
    #                 logging.warning("FAIL " + r.text)
    #         except Exception as ex:
    #             logging.error("%s\t%s" % (ex, settings.settings.API_URL + 'getUpdates' + '?offset=%d' % (last.update_id + 1)))
    # except KeyboardInterrupt:
    #     exit(0)