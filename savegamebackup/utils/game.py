"""
Created on 07.01.2016

@author: Philip Schoemig
"""

import configparser
import itertools
import os

import glob2

import utils.userinteraction


FILENAME_EXTENSION = '.cfg'


class Game(object):
    input_helper = utils.userinteraction.InputHelper()

    discovered = False

    def __init__(self, configurator, config):
        self.configurator = configurator
        self.config = config

        self.name = config.get('game', 'name')
        self.pathname = config.get('game', 'pathname')

        self.path = self.configurator.settings.get(
            self.name, 'path', fallback=None)

        self.backup_path = os.path.join(self.configurator.root_path, self.name)
        if not os.path.exists(self.backup_path):
            os.mkdir(self.backup_path)

        self.max_backups = self.configurator.settings.getint(
            self.name, 'max_backups', fallback=5)

        self.profiles = utils.profile.ProfileManager(self.configurator, self)
        self.backups = utils.backup.BackupManager(
            self.configurator, self.profiles.default_profile)

    def __repr__(self):
        return repr((self.name))

    def exists(self):
        if self.path:
            return True
        return False

    @classmethod
    def from_config_file(cls, configurator, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        if not config.has_section('game') or \
           not config.has_option('game', 'name'):
            raise RuntimeError(
                f"Invalid game config file: {config_file}")
        return cls(configurator, config)


class GameManager(object):
    search_paths = [
        os.path.expanduser('~/**'),
        os.path.expanduser('~/.*/**'),
        os.path.expandvars('%ProgramFiles%/**'),
        os.path.expandvars('%ProgramFiles(x86)%/**'),
        os.path.expandvars('%ProgramW6432%/**'),
    ]
    input_helper = utils.userinteraction.InputHelper()

    configurator = None

    # Cache variables
    games = None

    def __new__(cls, *p, **k):
        # Ensure the instance is only created once (Singleton)
        if '_the_instance' not in cls.__dict__:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance

    def initialize(self, configurator):
        self.configurator = configurator

    def list(self, discover=False):
        games = self.games
        config_path = os.path.join(self.configurator.root_path, '.config')
        if not games:
            games = []
            for entry in os.listdir(config_path):
                path = os.path.join(config_path, entry)
                if os.path.isfile(path) and \
                   os.path.splitext(path)[1] == FILENAME_EXTENSION:
                    game = Game.from_config_file(self.configurator, path)
                    if discover and not game.exists():
                        game.path = self._lookup_savegame_path(
                            game.name, game.pathname)
                        if game.path:
                            game.discovered = True
                    if game.exists():
                        games.append(game)
            self.games = games
        return games

    def select(self):
        games = self.list()
        game = None
        if len(games) > 0:
            game_names = {game.name: game for game in games}
            name = self.input_helper.input('Please enter the game', game_names.keys())
            game = game_names[name]
        else:
            print("No game found")
        return game

    def _lookup_savegame_path(self, name, pathname):
        path = self.configurator.settings.get(name, 'path', fallback=None)
        if not path or not os.path.exists(path):
            path = os.path.normpath(
                os.path.expandvars(
                    os.path.expanduser(pathname)))
            if not os.path.isabs(path):
                for search_path in self.search_paths:
                    glob_pattern = os.path.join(
                        os.path.normpath(search_path), path)
                    glob_path = list(itertools.islice(
                        glob2.iglob(glob_pattern), 1))
                    if glob_path:
                        path = glob_path[0]
                        break

            if os.path.exists(path):
                if not self.configurator.settings.has_section(name):
                    self.configurator.settings.add_section(name)
                self.configurator.settings.set(name, 'path', path)
                self.configurator.save_settings_file()
            else:
                path = None
                # TODO logging
                # raise RuntimeError(
                #     f"Savegame path could not be found: {pathname}")

        return path
