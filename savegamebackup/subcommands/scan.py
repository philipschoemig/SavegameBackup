'''
Created on 06.12.2018

@author: Philip Schoemig
'''
import utils.game


class Processor(object):
    def __init__(self, configurator):
        self.configurator = configurator

    def run(self, args):
        print("== Scan games ==")
        self.args = args

        self.game_manager = utils.game.GameManager()

        games = self.game_manager.list(True)
        new_games = []
        for game in games:
            if game.discovered:
                new_games.append(game)

        if new_games:
            print("New games:")
            for game in new_games:
                print(f"- {game.name}: {game.path}")
            print()  # Newline

        if games:
            print("All games:")
            for game in games:
                print(f"- {game.name}: {game.path}")
        else:
            print("No games found")

    def register_cl_parser(self, main_parser):
        parser = main_parser.add_parser(
            'scan', help="Scan for installed games")

        parser.set_defaults(func=self.run)
        return parser
