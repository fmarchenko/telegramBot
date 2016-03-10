#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fedor Marchenko"
__email__ = "mfs90@mail.ru"
__date__ = "Mar 10, 2016"

import sys
from telegramBot import settings
from telegramBot.options import parser
from telegramBot.commands import shell, migrate
from telegramBot.application import app

# Main code
def main():
    import django
    django.setup()
    if len(sys.argv) <= 1:
        parser.print_help()
        exit(0)
    else:
        opts = parser.parse_args(sys.argv[1:])

    if opts.s:
        shell()
    if opts.m:
        migrate()
    if opts.cmd == "start":
        app.debug = settings.settings.DEBUG
        app.run(host='localhost', port=8000)


if __name__ == "__main__":
    main()
