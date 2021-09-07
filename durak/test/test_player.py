import sys
import unittest
sys.path.append("..")

from player import Player
from player import AIPlayerDumb
from game_mechanics import Deck
from game_mechanics import Table
print('done')

class TestPlayer(unittest.TestCase):

    def test_name(self):
        for i in range(100):
            self.player = Player('Aleksei')
            self.assertEqual(self.player.nickname, 'Aleksei')
            self.player = Player('Петух')
            self.assertEqual(self.player.nickname, 'Петух')

    def test_draw_card_ability(self):
        for i in range(100):
            self.deck = Deck(52)
            self.player = Player('Aleksei')
            self.player.draw_cards(self.deck)
            self.assertEqual(len(self.player.cards), 6)

    def test_remove_card_ability(self):
        for i in range(100):
            self.deck = Deck(36)
            self.player = Player('Aleksei')
            self.player.draw_cards(self.deck)
            self.player.remove_card(self.player.cards[0])
            self.assertEqual(len(self.player.cards), 5)

    def test_attacking_options(self):
        for i in range(100):
            self.deck = Deck(36)
            self.player = Player('Aleksei')
            self.player.draw_cards(self.deck)
            self.player.remove_card(self.player.cards[0])
            self.assertEqual(len(self.player.attacking_options()), 5)

    def test_defending_options(self):
        for i in range(100):
            self.deck = Deck(36)
            self.player = Player('Aleksei')
            self.player.draw_cards(self.deck)
            self.table = Table()
            for i in self.player.cards:
                self.table.update_table(i)
            self.assertIsNotNone(self.player.defending_options(self.table))

    def test_grab_table(self):
        for i in range(100):
            self.deck = Deck(36)
            self.player = Player('Aleksei')
            self.player.draw_cards(self.deck)
            self.table = Table()
            for i in self.player.cards:
                self.table.update_table(i)
            self.player.grab_table(self.table)
            self.assertEqual(len(self.player.cards), 12)

class TestAIPlayerDumb(unittest.TestCase):
    def test_attack_defend_addcard(self):
        for i in range(100):
            self.deck = Deck(36)
            self.player1 = AIPlayerDumb('Aleksei')
            self.player2 = AIPlayerDumb('Loh')

            self.player1.draw_cards(self.deck)
            self.player2.draw_cards(self.deck)

            self.table = Table()

            self.player1.attack(self.table)
            self.assertEqual(len(self.table.show()), 1)
            self.player2.defend(self.table)
            self.assertIn(len(self.table.show()), [0, 1, 2])
            if len(self.table.show()) == 2:
                self.player1.adding_card(self.table)
                self.assertIn(len(self.table.show()), [2, 3])

if __name__ == '__main__':
    unittest.main()
