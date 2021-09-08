import logging
import os
#from game_mechanics import *
import game_mechanics
from player import AIPlayerDumb
from player import AIPlayerLowestCard
from player import AIPlayerLowestCardDontWastingTrumps
from player import HumanPlayer

p1 = AIPlayerDumb('VALL E')
p2 = AIPlayerDumb('EVA')
p3 = AIPlayerLowestCard('EVA')
p4 = AIPlayerLowestCardDontWastingTrumps('EVA2')

players_list = [p1, p2]

if os.path.isfile('game.log'):
    os.remove('game.log')

logger = logging.getLogger('logging_games')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('game.log')
logger.addHandler(fh)

def play_game(list_of_players, logger=None):
    deck = game_mechanics.Deck(36)
    g = game_mechanics.GameProcess(list_of_players, deck, logger)
    #ptr = game_mechanics.Pointer(list_of_players)
    return g.play()

def play_n_games(n_games, list_of_players, logger=None):
    for i in range(n_games):
        logger.info({'Game' : i})
        play_game(list_of_players=list_of_players, logger=logger)
    return 'Done'

play_n_games(1000, players_list, logger=logger)
