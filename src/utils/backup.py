'''
Created on 07.01.2016

@author: Philip Schoemig
'''
import os
import re
import tarfile
import time


class Backup(object):
    name = None
    path = None

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def get_time(self):
        return time.localtime(os.path.getmtime(self.path))

    def get_size(self):
        return os.path.getsize(self.path)

    def __repr__(self):
        return repr((self.name, self.path))


class BackupManager(object):
    configurator = None
    backups = None

    def __init__(self, configurator):
        self.configurator = configurator

    def list(self, profile=None):
        backups = self.backups
        if not backups:
            backups = []
            for entry in os.listdir(self.configurator.backup_path):
                path = os.path.join(self.configurator.backup_path, entry)
                if tarfile.is_tarfile(path):
                    backups.append(Backup(entry, path))
            backups.sort(key=lambda backup: backup.name)
            self.backups = backups
        if profile:
            backups = [backup for backup in backups if re.match(
                r'{0}_'.format(profile.name), backup.name)]
        return backups

    def create(self, profile):
        timestamp = time.strftime('%Y%m%d_%H%M%S', profile.get_time())
        filename = '{0}_{1}.tar.bz2'.format(profile.name, timestamp)
        path = os.path.join(self.configurator.backup_path, filename)
        if not self.configurator.dry_run:
            if os.path.exists(path):
                raise IOError('Backup file already exists: ' + filename)
            cwd = os.getcwd()
            try:
                os.chdir(os.path.dirname(profile.path))
                with tarfile.open(path, 'w:bz2') as tar:
                    tar.add(profile.name)
            finally:
                os.chdir(cwd)
        self.backups = None  # Reset stored backup list
        return filename

    def cleanup(self, profile):
        max_backups = self.configurator.config.getint('backups', 'max_count')
        backups = self.list(profile)
        count = len(backups) - max_backups

        old_backups = []
        if count > 0:
            old_backups = backups[0:count]
            for backup in old_backups:
                if not self.configurator.dry_run:
                    os.remove(backup.path)
        self.backups = None  # Reset stored backup list
        return old_backups
