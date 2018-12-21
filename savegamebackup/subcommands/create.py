'''
Created on 07.01.2016

@author: Philip Schoemig
'''
import datetime

import utils.game


class Processor(object):
    def __init__(self, configurator):
        self.configurator = configurator

    def run(self, args):
        print("== Create backup ==")
        self.args = args

        self.game_manager = utils.game.GameManager()

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
        game = self.game_manager.select()
        profile = game.profiles.select()
        selection = [profile]
        return selection

    def automatic_profile_selection(self):
        selection = []
        games = self.game_manager.list()
        for game in games:
            profiles = game.profiles.list()
            for profile in profiles:
                profile_time = profile.get_time().replace(microsecond=0)
                backups = profile.backups.list(True)
                if len(backups) > 0:
                    backup_time = backups[-1].get_time()
                else:
                    backup_time = profile_time - datetime.timedelta(1)
                if profile_time > backup_time:
                    selection.append(profile)
        return selection

    def backup_profiles(self, profiles):
        for profile in profiles:
            print()  # Newline
            print("Game: " + profile.game.name)
            print("Profile: " + profile.name)
            print("Creating backup ...")
            filename = profile.backups.create()
            print("- " + filename)

            print("Cleaning up old backups ...")
            old_backups = profile.backups.cleanup()
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
