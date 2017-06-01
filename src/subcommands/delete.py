'''
Created on 22.09.2016

@author: Philip Schoemig
'''
import utils.backup
import utils.profile


class Processor(object):
    configurator = None
    args = None

    backup_manager = None
    profile_manager = None

    def __init__(self, configurator):
        self.configurator = configurator

    def run(self, args):
        print("== Delete backup ==")
        self.args = args

        self.backup_manager = utils.backup.BackupManager()
        self.profile_manager = utils.profile.ProfileManager()

        profile = self.profile_manager.select()
        if profile:
            print()  # Newline
            print("Profile: " + profile.name)

            backup = self.backup_manager.select(profile)
            if backup:
                print()  # Newline
                print("Backup: " + backup.name)

                print("Deleting backup ...")
                self.backup_manager.delete(profile, backup)
                print("Done")

    def register_cl_parser(self, main_parser):
        parser = main_parser.add_parser(
            'restore', help="Delete a savegame backup")

        parser.set_defaults(func=self.run)
        return parser
