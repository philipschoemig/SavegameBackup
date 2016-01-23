'''
Created on 07.01.2016

@author: Philip Schoemig
'''
import utils.backup
import utils.profile
import utils.ui


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
        print("== Create backup ==")
        self.backup_manager.load_config()
        self.profile_manager.load_config()
        self.args = args

        profiles = []
        if self.args.manual:
            profiles = self.manual_profile_selection()
        else:
            profiles = self.automatic_profile_selection()

        if len(profiles) > 0:
            self.backup_profiles(profiles)
            print("Done")
        else:
            print("No profiles selected")

    def manual_profile_selection(self):
        profiles = self.profile_manager.list()
        index = utils.ui.UserInteraction.select(
            "Please select the profile to backup",
            [profile.name for profile in profiles])
        selection = [profiles[index]]
        return selection

    def automatic_profile_selection(self):
        profiles = self.profile_manager.list()
        selection = []
        for profile in profiles:
            profile_time = profile.get_time().replace(microsecond=0)
            backups = self.backup_manager.list(profile)
            backup_time = backups[-1].get_time()
            if profile_time > backup_time:
                selection.append(profile)
        return selection

    def backup_profiles(self, profiles):
        for profile in profiles:
            print()  # Newline
            print("Profile: " + profile.name)
            print("Creating backup ...")
            filename = self.backup_manager.create(profile)
            print("- " + filename)

            print("Cleaning up old backups ...")
            old_backups = self.backup_manager.cleanup(profile)
            for backup in old_backups:
                print("- " + backup.name)

    def register_cl_parser(self, main_parser):
        parser = main_parser.add_parser(
            'create', help="Create a savegame backup")

        parser.add_argument(
            '--manual', action='store_true',
            help="Manually select the profiles to back up (default: false)")

        parser.set_defaults(func=self.run)
        return parser
