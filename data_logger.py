import logging
import time
from durak_ai import AiPlayerDumb
from game import game_instance

logger = logging.getLogger('logging_games')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('game.log')

P1 = AiPlayerDumb('VALL E')
P2 = AiPlayerDumb('EVA')
players_list = [P1, P2]
i = 0
t = time.time()
logger.addHandler(fh)
while i != 100:
    print(game_instance(players_list, logger))
    i += 1
    data_to_log = 'Game-'+str(i)
    logger.info(data_to_log)
    print(i)
    print(time.time() - t)
