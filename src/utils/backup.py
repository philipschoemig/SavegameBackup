'''
Created on 07.01.2016

@author: Philip Schoemig
'''
from datetime import datetime
import os
import re
import shutil
import tarfile

import utils.ui


TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'
TIMESTAMP_REGEXP = r'\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}'


class Backup(object):
    name = None
    path = None

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def get_time(self):
        match = re.search(TIMESTAMP_REGEXP, self.name)
        return datetime.strptime(match.group(0), TIMESTAMP_FORMAT)

    def get_size(self):
        return os.path.getsize(self.path)

    def __repr__(self):
        return repr((self.name, self.path))


class BackupManager(object):
    configurator = None
    backups = None

    # Configuration options
    max_backups = None

    def __init__(self, configurator):
        self.configurator = configurator

    def load_config(self):
        self.max_backups = self.configurator.config.getint(
            'backups', 'max_count')

    def list(self, profile=None):
        backups = self.backups
        if not backups:
            backups = []
            for entry in os.listdir(self.configurator.backup_path):
                path = os.path.join(self.configurator.backup_path, entry)
                if os.path.isfile(path) and tarfile.is_tarfile(path):
                    backups.append(Backup(entry, path))
            backups.sort(key=lambda backup: backup.name)
            self.backups = backups
        if profile:
            backups = [backup for backup in backups if re.match(
                r'{0}_'.format(profile.name), backup.name)]
        return backups

    def create(self, profile):
        timestamp = profile.get_time().strftime(TIMESTAMP_FORMAT)
        filename = '{0}_{1}.tar.bz2'.format(profile.name, timestamp)
        path = os.path.join(self.configurator.backup_path, filename)
        if os.path.exists(path):
            raise IOError('Backup file already exists: ' + filename)
        if not self.configurator.dry_run:
            cwd = os.getcwd()
            try:
                os.chdir(os.path.dirname(profile.path))
                with tarfile.open(path, 'w:bz2') as tar:
                    tar.add(profile.name)
            finally:
                os.chdir(cwd)
        self.backups = None  # Reset stored backup list
        return filename

    def restore(self, profile, backup):
        target_path = os.path.dirname(profile.path)
        if utils.ui.UserInteraction.confirm(
           'Overwrite profile \'{0}\'?'.format(profile.path)):
            if not self.configurator.dry_run:
                cwd = os.getcwd()
                try:
                    os.chdir(target_path)
                    shutil.rmtree(profile.name)
                    with tarfile.open(backup.path, 'r:bz2') as tar:
                        tar.extractall()
                finally:
                    os.chdir(cwd)

    def cleanup(self, profile):
        backups = self.list(profile)
        count = len(backups) - self.max_backups

        old_backups = []
        if count > 0:
            old_backups = backups[0:count]
            for backup in old_backups:
                if not self.configurator.dry_run:
                    os.remove(backup.path)
        self.backups = None  # Reset stored backup list
        return old_backups
