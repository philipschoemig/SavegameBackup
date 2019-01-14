'''
Created on 07.01.2016

@author: Philip Schoemig
'''
import hurry.filesize
import utils.game


class Processor(object):
    def __init__(self, configurator):
        self.configurator = configurator
        self.args = None
        self.game_manager = None

    def run(self, args):
        print("== List backups ==")
        self.args = args

        self.game_manager = utils.game.GameManager()

        game = self.game_manager.select()
        if game:
            backups = game.profiles.default_profile.backups.list()
            for backup in backups:
                print(self.print_backup_info(backup))
        if not backups:
            print("No backups created yet")

    def print_backup_info(self, backup):
        size = hurry.filesize.size(backup.get_size())
        timestamp = backup.get_time().ctime()
        return "- {0} - Size: {1}, Time: {2}".format(
            backup.name, size, timestamp)

    def register_cl_parser(self, main_parser):
        parser = main_parser.add_parser(
            'list', help="List the available backups")

        parser.set_defaults(func=self.run)
        return parser
