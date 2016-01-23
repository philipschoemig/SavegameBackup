'''
Created on 07.01.2016

@author: Philip Schoemig
'''
import hurry.filesize
import utils.backup


class Processor(object):
    configurator = None
    backup_manager = None
    args = None

    def __init__(self, configurator):
        self.configurator = configurator
        self.backup_manager = utils.backup.BackupManager(configurator)

    def run(self, args):
        print("== List backups ==")
        self.backup_manager.load_config()
        self.args = args

        backups = self.backup_manager.list()
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
