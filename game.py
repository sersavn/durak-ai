from game_mechanics import *
from durak_ai import AiPlayerDumb
from player import HumanPlayer

p1 = HumanPlayer('Antoha')
#p1 = AiPlayerDumb('VALL E')
p2 = AiPlayerDumb('EVA')
players_list = [p1, p2]
deck = Deck(36)
g = Game(players_list, deck)
ptr = Pointer(players_list)
g.play()
