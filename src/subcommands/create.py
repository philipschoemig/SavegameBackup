'''
Created on 07.01.2016

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
        print "== Create backup =="
        self.args = args

        profiles = self.profile_manager.list()
        for index, profile in enumerate(profiles):
            print "{0}. {1}".format(index, profile.name)

        index = raw_input("Please enter the number of the profile to backup: ")
        profile = profiles[int(index)]
        print "Selected profile: '{0}'".format(profile.name)

        print "Creating backup ..."
        filename = self.backup_manager.create(profile)
        print "- " + filename

        print "Cleaning up old backups ..."
        old_backups = self.backup_manager.cleanup(profile)
        for backup in old_backups:
            print "- " + backup.name

        print "Done"

    def register_cl_parser(self, main_parser):
        parser = main_parser.add_parser('create', help="Create a new backup")

        parser.set_defaults(func=self.run)
        return parser
