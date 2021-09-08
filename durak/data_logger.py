import logging
import time
import os
from player import AIPlayerDumb
from game_mechanics import GameProcess
from game_mechanics import Deck

if os.path.isfile('game.log'):
    os.remove('game.log')

logger = logging.getLogger('logging_games')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('game.log')

P1 = AIPlayerDumb('VALL E')
P2 = AIPlayerDumb('EVA')
players_list = [P1, P2]
i = 0
t = time.time()
logger.addHandler(fh)
logger.info({'Game' : 0})

deck = Deck(36)
while i != 200:
    GameProcess(players_list, deck, logger)
    print(P1.cards)
    print(P2.cards)
    i += 1
    logger.info({"Game" : i})
    print(i)
    print(time.time() - t)
