#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Mar 10, 2016"

import os

# Setup for Django Project
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, '..')
BOT_INTERVAL = 3
BOT_ADMIN_ID = None
BOT_TOKEN = ''
BOT_PORT = 8000
BOT_HOST = 'localhost'
try:
    from settings_local import *
except:
    pass
API_URL="https://api.telegram.org/bot%s/" % BOT_TOKEN

settings.configure(
    SECRET_KEY='n)u5keagpdbl@o3xo+^&8jr)@e1j)b*5xdswoon(e9&xd5arfi',
    DEBUG=True,
    INSTALLED_APPS=['telegramBot'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3')}},
)