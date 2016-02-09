'''
Created on 22.01.2016

@author: Philip Schoemig
'''
import utils.backup
import utils.profile
import utils.userinteraction


class Processor(object):
    configurator = None
    args = None

    input_helper = None
    backup_manager = None
    profile_manager = None

    def __init__(self, configurator):
        self.configurator = configurator

    def run(self, args):
        print("== Restore backup ==")
        self.args = args

        self.input_helper = utils.userinteraction.InputHelper()
        self.backup_manager = utils.backup.BackupManager()
        self.profile_manager = utils.profile.ProfileManager()

        profile = self.profile_selection()
        if profile:
            print()  # Newline
            print("Profile: " + profile.name)

            backup = self.backup_selection(profile)
            if backup:
                print()  # Newline
                print("Backup: " + backup.name)

                print("Restoring backup ...")
                self.backup_manager.restore(profile, backup)
                print("Done")
            else:
                print("No backup found")
        else:
            print("No profile found")

    def profile_selection(self):
        profiles = self.profile_manager.list()
        profile = None
        if len(profiles) > 0:
            index = self.input_helper.select(
                "Please select the profile to restore",
                [profile.name for profile in profiles])
            profile = profiles[index]
        return profile

    def backup_selection(self, profile):
        backups = self.backup_manager.list(profile)
        backup = None
        if len(backups) > 0:
            index = self.input_helper.select(
                "Please select the backup to restore",
                [backup.name for backup in backups])
            backup = backups[index]
        return backup

    def register_cl_parser(self, main_parser):
        parser = main_parser.add_parser(
            'restore', help="Restore a savegame backup")

        parser.set_defaults(func=self.run)
        return parser
