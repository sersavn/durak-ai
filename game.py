import logging
import os
from game_mechanics import *
from durak_ai import AiPlayerDumb
from player import HumanPlayer


class Game:
    def __init__(self, players_list):
        players_list = self.players_list


p1 = AiPlayerDumb('VALL E')
p2 = AiPlayerDumb('EVA')
players_list = [p1, p2]

if os.path.isfile('game.log'):
    os.remove('game.log')


logger = logging.getLogger('logging_games')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('game.log')
logger.addHandler(fh)
logger.info({'Game' : 0})


def game_instance(list_of_players, logger=None):
    deck = Deck(36)
    print(deck)
    g = GameProcess(players_list, deck, logger)
    ptr = Pointer(players_list)
    g.play()

#print(game_instance(players_list, logger))
