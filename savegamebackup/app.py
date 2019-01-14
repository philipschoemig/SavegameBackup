#!/usr/bin/env python3
'''
SavegameBackup - Manages backups of savegame files
Version 2.0.1
'''
import sys

import configuration.configurator
import subcommands.create
import subcommands.delete
import subcommands.list
import subcommands.restore
import subcommands.scan


def main():
    # create configurator
    configurator = configuration.configurator.Configurator()

    # register subcommands
    subcommand_create = subcommands.create.Processor(configurator)
    configurator.register_subcommand(subcommand_create)

    subcommand_delete = subcommands.delete.Processor(configurator)
    configurator.register_subcommand(subcommand_delete)

    subcommand_list = subcommands.list.Processor(configurator)
    configurator.register_subcommand(subcommand_list)

    subcommand_restore = subcommands.restore.Processor(configurator)
    configurator.register_subcommand(subcommand_restore)

    subcommand_scan = subcommands.scan.Processor(configurator)
    configurator.register_subcommand(subcommand_scan)

    # start processing
    configurator.run()
    return 0


if __name__ == "__main__":
    # Execute the following lines only when this script is called directly.
    # When it is included from another script they are ignored.
    status = main()
    sys.exit(status)
