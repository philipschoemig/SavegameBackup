"""
Created on 07.01.2016

@author: Philip Schoemig
"""

from datetime import datetime
import os
import re
import shutil
import tarfile

# from singleton.singleton import Singleton

import utils.userinteraction


FILENAME_EXTENSION = '.tar.bz2'
TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'
TIMESTAMP_REGEXP = r'\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}(?=' + \
                                                     FILENAME_EXTENSION + r')'


class Backup(object):
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
    input_helper = utils.userinteraction.InputHelper()

    # Cache variables
    backups = None

    def __init__(self, configurator, profile):
        self.configurator = configurator
        self.profile = profile

    def cleanup(self):
        backups = self.list(True)
        count = len(backups) - self.profile.game.max_backups

        old_backups = []
        if count > 0:
            old_backups = backups[0:count]
            for backup in old_backups:
                if not self.configurator.dry_run:
                    os.remove(backup.path)
        self.backups = None  # Reset stored backup list
        return old_backups

    def create(self):
        timestamp = self.profile.get_time().strftime(TIMESTAMP_FORMAT)
        filename = f"{self.profile.name}_{timestamp}{FILENAME_EXTENSION}"
        path = os.path.join(self.profile.game.backup_path, filename)
        if os.path.exists(path):
            raise IOError(f"Backup file already exists: {filename}")
        if not self.configurator.dry_run:
            cwd = os.getcwd()
            try:
                dirname, basename = os.path.split(self.profile.path)
                os.chdir(dirname)
                with tarfile.open(path, 'w:bz2') as tar:
                    tar.add(basename)
            finally:
                os.chdir(cwd)
        self.backups = None  # Reset stored backup list
        return filename

    def delete(self, backup):
        if self.input_helper.confirm(f"Delete backup '{backup.path}'?"):
            if not self.configurator.dry_run:
                os.remove(backup.path)

    def list(self, filter_profile=False):
        backups = self.backups
        if not backups:
            backups = []
            for entry in os.listdir(self.profile.game.backup_path):
                path = os.path.join(self.profile.game.backup_path, entry)
                if os.path.isfile(path) and tarfile.is_tarfile(path):
                    backups.append(Backup(entry, path))
            backups.sort(key=lambda backup: backup.name)
            self.backups = backups
        if filter_profile:
            backups = [backup for backup in backups if re.match(
                fr"{self.profile.name}_", backup.name)]
        return backups

    def restore(self, backup):
        if os.path.isdir(self.profile.path) and \
           self.input_helper.confirm(
               f"Overwrite profile '{self.profile.path}'?"):
            if not self.configurator.dry_run:
                shutil.rmtree(self.profile.path)

        if not self.configurator.dry_run:
            cwd = os.getcwd()
            try:
                dirname, basename = os.path.split(self.profile.path)
                os.chdir(dirname)
                with tarfile.open(backup.path, 'r:bz2') as tar:
                    def is_within_directory(directory, target):
                        
                        abs_directory = os.path.abspath(directory)
                        abs_target = os.path.abspath(target)
                    
                        prefix = os.path.commonprefix([abs_directory, abs_target])
                        
                        return prefix == abs_directory
                    
                    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                    
                        for member in tar.getmembers():
                            member_path = os.path.join(path, member.name)
                            if not is_within_directory(path, member_path):
                                raise Exception("Attempted Path Traversal in Tar File")
                    
                        tar.extractall(path, members, numeric_owner=numeric_owner) 
                        
                    
                    safe_extract(tar)
            finally:
                os.chdir(cwd)

    def select(self):
        backups = self.list(True)
        backup = None
        if len(backups) > 0:
            index = self.input_helper.select(
                "Please select the backup",
                [backup.name for backup in backups])
            backup = backups[index]
        else:
            print("No backup found")
        return backup
