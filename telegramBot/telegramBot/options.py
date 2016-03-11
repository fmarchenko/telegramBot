#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Mar 10, 2016"

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store_true', help="run env shell")
parser.add_argument('-m', action='store_true', help="run migrations")
parser.add_argument('cmd', nargs='?', default="", help="run command")