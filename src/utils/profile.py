'''
Created on 07.01.2016

@author: Philip Schoemig
'''
from datetime import datetime
import os

from singleton.singleton import Singleton


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
    profiles = None

    # Configuration options
    savegame_path = None
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

        # Read configuration options
        self.savegame_path = self.configurator.config.get('game', 'path')

        if self.configurator.config.has_option('profiles', 'excludes'):
            option = self.configurator.config.get('profiles', 'excludes')
            self.excludes = [exclude.strip() for exclude in option.split(',')]

        if self.configurator.config.has_option('profiles', 'includes'):
            option = self.configurator.config.get('profiles', 'includes')
            self.includes = [include.strip() for include in option.split(',')]

    def list(self):
        profiles = self.profiles
        if not profiles:
            profiles = []
            for entry in os.listdir(self.savegame_path):
                path = os.path.join(self.savegame_path, entry)
                include = \
                    (self.excludes is None or entry not in self.excludes) and \
                    (self.includes is None or entry in self.includes)
                if os.path.isdir(path) and include:
                    profiles.append(Profile(entry, path))
            profiles.sort(key=lambda profile: profile.name)
            self.profiles = profiles
        return profiles
