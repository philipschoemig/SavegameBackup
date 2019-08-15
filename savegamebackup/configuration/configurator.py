"""
Created on 07.01.2016

@author: Philip Schoemig
"""

import argparse
#import argcomplete # https://argcomplete.readthedocs.io/
import configparser
import logging
import os
import sys

import utils.backup
import utils.game
import utils.profile
import utils.userinteraction


class Configurator(object):
    dry_run = False

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog=sys.argv[0],
            description='Manages backups of savegames')
        self.subparsers = self.parser.add_subparsers(
            help='Available sub-commands',
            dest='subcommand')

        self.root_path = os.path.join(os.path.expanduser('~'), '.savegame')
        self.log_file = os.path.join(self.root_path, 'SavegameBackup.log')
        self.settings_file = os.path.join(self.root_path,
                                          'SavegameBackup.settings')
        self.settings = configparser.ConfigParser()

    def run(self):
        # Initialize command line parser
        self.init_main_cl_parser()
        args = self.parser.parse_args(sys.argv[1:])

        # Initialize dry run mode from command line arguments
        self.dry_run = args.dry_run

        # Initialize logging framework
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)

        # Parse settings file
        self.settings.read(self.settings_file)

        # Initialize input helper
        input_helper = utils.userinteraction.InputHelper()

        # Initialize game manager
        game_manager = utils.game.GameManager()
        game_manager.initialize(self)

        if args.subcommand:
            args.func(args)
        else:
            options = [choice for choice in self.subparsers.choices]
            cmd = '-h'
            while cmd:
                try:
                    cmd_args = self.parser.parse_args(cmd.split())
                    if cmd_args.subcommand:
                        cmd_args.func(cmd_args)
                except SystemExit:
                    pass
                cmd = input_helper.input('$', options, False)

    def save_settings_file(self):
        with open(self.settings_file, 'w') as file:
            self.settings.write(file)

    def init_main_cl_parser(self):
        # define global options here
        self.parser.add_argument(
            '--dry-run', action='store_true',
            help="No changes will be made to the file system")

    def register_subcommand(self, subcommand):
        subcommand.register_cl_parser(self.subparsers)
