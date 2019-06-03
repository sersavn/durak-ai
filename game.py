from game_mechanics import *
from durak_ai import AiPlayerDumb
from player import HumanPlayer

#p1 = HumanPlayer('Kropa')
p1 = AiPlayerDumb('VALL E')
p2 = AiPlayerDumb('EVA')
players_list = [p1, p2]

def game_instance(list_of_players, logger=None):
    deck = Deck(36)
    g = GameProcess(players_list, deck, logger)
    ptr = Pointer(players_list)
    g.play()

print(game_instance(players_list))
