'''
Created on 07.01.2016

@author: Philip Schoemig
'''
import configparser
from datetime import datetime
import itertools
import os
import re
import platform

import glob2
from singleton.singleton import Singleton

import utils.userinteraction


class Profile(object):
    name = None
    path = None

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def get_time(self):
        mtimes = [os.path.getmtime(os.path.join(self.path, entry))
                  for entry in os.listdir(self.path)]
        mtimes.sort(reverse=True)
        return datetime.fromtimestamp(mtimes[0])

    def __repr__(self):
        return repr((self.name, self.path))


class ProfileManager(object):
    configurator = None
    input_helper = None
    cache = None
    cache_file = None
    search_paths = [
        os.path.expanduser('~/**'),
        os.path.expanduser('~/.*/**'),
        os.path.expandvars('%ProgramFiles%/**'),
        os.path.expandvars('%ProgramFiles(x86)%/**'),
        os.path.expandvars('%ProgramW6432%/**'),
        ]

    # Configuration options
    savegame_path = None
    enabled = None
    excludes = None
    includes = None

    # Cache variables
    profiles = None

    def __new__(cls, *p, **k):
        # Ensure the instance is only created once (Singleton)
        if '_the_instance' not in cls.__dict__:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance

    def initialize(self, configurator):
        self.configurator = configurator
        self.input_helper = utils.userinteraction.InputHelper()

        self.cache = configparser.SafeConfigParser()
        self.cache_file = os.path.join(self.configurator.backup_path, 'cache.cfg')
        self.cache.read(self.cache_file)

        # Read configuration options
        self.savegame_path = self._lookup_savegame_path()

        self.enabled = self.configurator.config.getboolean('profiles', 'enabled', fallback=False)

        if self.configurator.config.has_option('profiles', 'excludes'):
            option = self.configurator.config.get('profiles', 'excludes')
            self.excludes = [exclude.strip() for exclude in option.split(',')]

        if self.configurator.config.has_option('profiles', 'includes'):
            option = self.configurator.config.get('profiles', 'includes')
            self.includes = [include.strip() for include in option.split(',')]

    def list(self, include_backups=False):
        profiles = self.profiles
        if not profiles:
            profiles = []
            if self.enabled:
                for entry in os.listdir(self.savegame_path):
                    path = os.path.join(self.savegame_path, entry)
                    include = \
                        (self.excludes is None or entry not in self.excludes) and \
                        (self.includes is None or entry in self.includes)
                    if os.path.isdir(path) and include:
                        profiles.append(Profile(entry, path))

                if include_backups:
                    backup_manager = utils.backup.BackupManager()
                    backup_profiles = [
                        re.split(r'_' + utils.backup.TIMESTAMP_REGEXP, backup.name, 1)[0]
                        for backup in backup_manager.list()]
                    profile_names = [profile.name for profile in profiles]
                    for entry in set(backup_profiles):
                        if entry not in profile_names:
                            path = os.path.join(self.savegame_path, entry)
                            profiles.append(Profile(entry, path))

                profiles.sort(key=lambda profile: profile.name)
            else:
                profiles.append(Profile('Default', self.savegame_path))
            self.profiles = profiles
        return profiles

    def select(self, include_backups=False):
        profiles = self.list(include_backups)
        profile = None
        if len(profiles) > 0:
            index = self.input_helper.select(
                "Please select the profile",
                [profile.name for profile in profiles])
            profile = profiles[index]
        else:
            print("No profile found")
        return profile

    def _lookup_savegame_path(self):
        path = None
        system = platform.system().lower()
        if self.cache.has_section(system) and self.cache.has_option(system, 'lastpath'):
            path = self.cache.get(system, 'lastpath')
        if not path or not os.path.exists(path):
            path = self.configurator.config.get('game', 'path')
            path = os.path.normpath(
                os.path.expandvars(
                os.path.expanduser(path)))
            if not os.path.isabs(path):
                for search_path in self.search_paths:
                    glob_pattern = os.path.join(os.path.normpath(search_path), path)
                    glob_path = list(itertools.islice(glob2.iglob(glob_pattern), 1))
                    if glob_path:
                        path = glob_path[0]
                        break

            if os.path.exists(path) and \
                self.input_helper.confirm('Found the savegame path \'{0}\'. Is this correct?'.format(path)):
                if not self.cache.has_section(system):
                    self.cache.add_section(system)
                self.cache.set(system, 'lastpath', path)
                with open(self.cache_file, 'w') as file:
                    self.cache.write(file)
            else:
                raise RuntimeError('Savegame path could not be found: {0}'.format(path))

        return path
