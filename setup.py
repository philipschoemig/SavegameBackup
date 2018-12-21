#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='SavegameBackup',
    version='1.7.0',
    description='A software for backing up save files of computer games',
    license='BSD',
    author='Philip Schömig',
    author_email='philip.schoemig@posteo.de',
    url='https://github.com/philipschoemig/SavegameBackup/',
    packages=[
        'savegamebackup',
        'savegamebackup.configuration',
        'savegamebackup.subcommands',
        'savegamebackup.utils'
    ],
)
