import logging
import os
#from game_mechanics import *
import game_mechanics
from durak_ai import AIPlayerDumb
from player import HumanPlayer


class Game:
    def __init__(self, players_list):
        players_list = self.players_list

p1 = AIPlayerDumb('VALL E')
p2 = AIPlayerDumb('EVA')
players_list = [p1, p2]

if os.path.isfile('game.log'):
    os.remove('game.log')

logger = logging.getLogger('logging_games')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('game.log')
logger.addHandler(fh)
logger.info({'Game' : 0})

def play_game(list_of_players, logger=None):
    deck = game_mechanics.Deck(36)
    g = game_mechanics.GameProcess(list_of_players, deck, logger)
    ptr = game_mechanics.Pointer(list_of_players)
    # g.play() old
    return g.play()

#print(game_instance(players_list, logger))
