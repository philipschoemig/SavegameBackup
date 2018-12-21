'''
Created on 22.09.2016

@author: Philip Schoemig
'''
import utils.game


class Processor(object):
    def __init__(self, configurator):
        self.configurator = configurator

    def run(self, args):
        print("== Delete backup ==")
        self.args = args

        self.game_manager = utils.game.GameManager()

        game = self.game_manager.select()
        if game:
            profile = game.profiles.select(True)
            if profile:
                print()  # Newline
                print("Profile: " + profile.name)

                backup = profile.backups.select()
                if backup:
                    print()  # Newline
                    print("Backup: " + backup.name)

                    print("Deleting backup ...")
                    profile.backups.delete(backup)
                    print("Done")

    def register_cl_parser(self, main_parser):
        parser = main_parser.add_parser(
            'delete', help="Delete a savegame backup")

        parser.set_defaults(func=self.run)
        return parser
