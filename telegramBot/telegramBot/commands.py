#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Mar 10, 2016"

from django.core.management import call_command
from IPython import embed

def migrate():
    call_command('makemigrations', 'loader')
    # call_command('sqlmigrate', 'loader', "0001_initial")
    call_command('migrate')


def shell():
    embed()