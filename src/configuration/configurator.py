'''
Created on 07.01.2016

@author: Philip Schoemig
'''

import argparse
import configparser
import os
import sys


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
            help='Available sub-commands')
        self.config = configparser.SafeConfigParser()
        self.root_path = os.path.join(os.path.expanduser('~'), '.savegame')

    def run(self):
        self.init_main_cl_parser()
        args = self.parser.parse_args(sys.argv[1:])

        self.config.read(os.path.join(self.root_path, args.config_file))
        self.dry_run = args.dry_run

        self.backup_path = os.path.join(
            self.root_path, self.config.get('game', 'name'))
        if not os.path.exists(self.backup_path):
            os.mkdir(self.backup_path)

        args.func(args)

    def init_main_cl_parser(self):
        # define global options here
        self.parser.add_argument(
            '-c', '--config-file', required=True,
            help="Path to the configuration file", metavar='FILE')
        self.parser.add_argument(
            '--dry-run', action='store_true',
            help="No changes will be made to the file system")

    def register_subcommand(self, subcommand):
        subcommand.register_cl_parser(self.subparsers)
