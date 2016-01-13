'''
Created on 07.01.2016

@author: Philip Schoemig
'''
import os
import time


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
        return time.localtime(mtimes[0])

    def __repr__(self):
        return repr((self.name, self.path))


class ProfileManager(object):
    configurator = None
    profiles = None

    def __init__(self, configurator):
        self.configurator = configurator

    def list(self):
        profiles = self.profiles
        if not profiles:
            savegame_path = self.configurator.config.get('game', 'path')
            excludes = []
            if self.configurator.config.has_option('profiles', 'excludes'):
                option = self.configurator.config.get('profiles', 'excludes')
                excludes = [exclude.strip() for exclude in option.split(',')]

            profiles = []
            for entry in os.listdir(savegame_path):
                path = os.path.join(savegame_path, entry)
                if os.path.isdir(path) and entry not in excludes:
                    profiles.append(Profile(entry, path))
            profiles.sort(key=lambda profile: profile.name)
            self.profiles = profiles
        return profiles
