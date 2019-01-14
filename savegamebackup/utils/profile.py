'''
Created on 07.01.2016

@author: Philip Schoemig
'''
from datetime import datetime
import os
import re

import utils.userinteraction


class Profile(object):
    def __init__(self, configurator, game, name, path):
        self.configurator = configurator
        self.game = game
        self.name = name
        self.path = path

        self.backups = utils.backup.BackupManager(self.configurator, self)

    def get_time(self):
        mtimes = []
        for entry in os.listdir(self.path):
            if entry != "remotecache.vdf":
                filename = os.path.join(self.path, entry)
                mtimes.append(os.path.getmtime(filename))
        mtimes.sort(reverse=True)
        mtime = mtimes[0]
        return datetime.fromtimestamp(mtime)

    def __repr__(self):
        return repr((self.name, self.path))


class ProfileManager(object):
    input_helper = utils.userinteraction.InputHelper()

    # Cache variables
    profiles = None

    def __init__(self, configurator, game):
        self.configurator = configurator
        self.game = game

        self.default_profile = Profile(
            self.configurator, self.game, 'Default', self.game.path)

        # Read configuration options
        self.enabled = self.game.config.getboolean(
            'profiles', 'enabled', fallback=False)

        self.excludes = None
        if self.game.config.has_option('profiles', 'excludes'):
            option = self.game.config.get('profiles', 'excludes')
            self.excludes = [exclude.strip() for exclude in option.split(',')]

        self.includes = None
        if self.game.config.has_option('profiles', 'includes'):
            option = self.game.config.get('profiles', 'includes')
            self.includes = [include.strip() for include in option.split(',')]

    def list(self, include_backups=False):
        profiles = self.profiles
        if not profiles:
            profiles = []
            if self.enabled:
                for entry in os.listdir(self.game.path):
                    path = os.path.join(self.game.path, entry)
                    include = \
                        (self.excludes is None or entry not in self.excludes) and \
                        (self.includes is None or entry in self.includes)
                    if os.path.isdir(path) and include:
                        profiles.append(
                            Profile(self.configurator, self.game, entry, path))

                if include_backups:
                    backup_manager = utils.backup.BackupManager()
                    backup_profiles = [
                        re.split(r'_' + utils.backup.TIMESTAMP_REGEXP,
                                 backup.name, 1)[0]
                        for backup in backup_manager.list()]
                    profile_names = [profile.name for profile in profiles]
                    for entry in set(backup_profiles):
                        if entry not in profile_names:
                            path = os.path.join(self.game.path, entry)
                            profiles.append(
                                Profile(self.configurator,
                                        self.game, entry, path))

                profiles.sort(key=lambda profile: profile.name)
            else:
                profiles.append(self.default_profile)
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
