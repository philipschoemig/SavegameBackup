'''
Created on 22.01.2016

@author: Philip Schoemig
'''
import utils.backup
import utils.profile


class Processor(object):
    configurator = None
    backup_manager = None
    profile_manager = None
    args = None

    def __init__(self, configurator):
        self.configurator = configurator
        self.backup_manager = utils.backup.BackupManager(configurator)
        self.profile_manager = utils.profile.ProfileManager(configurator)

    def run(self, args):
        print("== Restore backup ==")
        self.backup_manager.load_config()
        self.profile_manager.load_config()
        self.args = args

        profile = self.profile_selection()
        print()  # Newline
        print("Profile: " + profile.name)

        backup = self.backup_selection(profile)
        print()  # Newline
        print("Backup: " + backup.name)

        print("Restoring backup ...")
        self.backup_manager.restore(profile, backup)

        print("Done")

    def profile_selection(self):
        profiles = self.profile_manager.list()
        index = utils.ui.UserInteraction.select(
            "Please select the profile to restore",
            [profile.name for profile in profiles])
        return profiles[index]

    def backup_selection(self, profile):
        backups = self.backup_manager.list(profile)
        index = utils.ui.UserInteraction.select(
            "Please select the backup to restore",
            [backup.name for backup in backups])
        return backups[index]

    def register_cl_parser(self, main_parser):
        parser = main_parser.add_parser(
            'restore', help="Restore a savegame backup")

        parser.set_defaults(func=self.run)
        return parser
