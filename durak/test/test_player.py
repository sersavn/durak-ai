import sys
import unittest
sys.path.append("..")

from player import Player
from game_mechanics import Deck
from game_mechanics import Table
print('done')

class TestPlayer(unittest.TestCase):

    def test_name(self):
        self.player = Player('Aleksei')
        self.assertEqual(self.player.nickname, 'Aleksei')

        self.player = Player('Петух')
        self.assertEqual(self.player.nickname, 'Петух')

    def test_draw_card_ability(self):
        self.deck = Deck(52)
        self.player = Player('Aleksei')
        self.player.draw_cards(self.deck)
        self.assertEqual(len(self.player.cards), 6)

    def test_remove_card_ability(self):
        self.deck = Deck(36)
        self.player = Player('Aleksei')
        self.player.draw_cards(self.deck)
        self.player.remove_card(self.player.cards[0])
        self.assertEqual(len(self.player.cards), 5)

    def test_attacking_options(self):
        self.deck = Deck(36)
        self.player = Player('Aleksei')
        self.player.draw_cards(self.deck)
        self.player.remove_card(self.player.cards[0])
        self.assertEqual(len(self.player.attacking_options()), 5)

    def test_defending_options(self):
        self.deck = Deck(36)
        self.player = Player('Aleksei')
        self.player.draw_cards(self.deck)
        self.table = Table()
        for i in self.player.cards:
            self.table.update_table(i)
        self.assertIsNotNone(self.player.defending_options(self.table))

    def test_grab_table(self):
        self.deck = Deck(36)
        self.player = Player('Aleksei')
        self.player.draw_cards(self.deck)
        self.table = Table()
        for i in self.player.cards:
            self.table.update_table(i)
        self.player.grab_table(self.table)
        self.assertEqual(len(self.player.cards), 12)

if __name__ == '__main__':
    unittest.main()
