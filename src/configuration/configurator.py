'''
Created on 07.01.2016

@author: Philip Schoemig
'''

import argparse
import configparser
import logging
import os
import pathlib
import sys

import utils.backup
import utils.profile
import utils.userinteraction


class Configurator(object):
    parser = None
    subparsers = None
    config = None
    root_path = None

    dry_run = False

    backup_path = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog=sys.argv[0],
            description='Manages backups of savegames')
        self.subparsers = self.parser.add_subparsers(
            help='Available sub-commands',
            dest='subcommand')
        self.config = configparser.SafeConfigParser(os.environ)
        self.root_path = os.path.join(os.path.expanduser('~'), '.savegame')
        self.log_file = os.path.join(self.root_path, 'SavegameBackup.log')

    def run(self):
        # Initialize command line parser
        self.init_main_cl_parser()
        args = self.parser.parse_args(sys.argv[1:])

        # Initialize dry run mode from command line arguments
        self.dry_run = args.dry_run

        # Initialize logging framework
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)

        # Initialize input helper
        input_helper = utils.userinteraction.InputHelper()

        # Parse configuration file
        config_file = self.get_config_file(args, input_helper)
        self.config.read(os.path.join(self.root_path, config_file))

        # Create backup path in case it doesn't exist
        self.backup_path = os.path.join(
            self.root_path, self.config.get('game', 'name'))
        if not os.path.exists(self.backup_path):
            os.mkdir(self.backup_path)

        # Initialize backup manager
        backup_manager = utils.backup.BackupManager()
        backup_manager.initialize(self)

        # Initialize profile manager
        profile_manager = utils.profile.ProfileManager()
        profile_manager.initialize(self)

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

    def get_config_file(self, args, input_helper):
        if args.config_file:
            return args.config_file
        else:
            path = pathlib.Path(self.root_path)
            options = [entry.name for entry in path.glob('*.cfg')]
            return input_helper.input(
                'Enter the configuration file name', options)

    def init_main_cl_parser(self):
        # define global options here
        self.parser.add_argument(
            '-c', '--config-file',
            help="Path to the configuration file", metavar='FILE')
        self.parser.add_argument(
            '--dry-run', action='store_true',
            help="No changes will be made to the file system")

    def register_subcommand(self, subcommand):
        subcommand.register_cl_parser(self.subparsers)
