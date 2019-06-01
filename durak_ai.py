import random
from player import Player

class AiPlayerDumb(Player):
    def __init__(self, nickname):
        super().__init__(nickname)

    def attack(self, table):
        attack_card = random.choice(self.cards)
        self.remove_card(attack_card)
        table.update_table(attack_card)
        print('{} attack with {}'.format(self.nickname, attack_card))
        return attack_card

    def defend(self, table):
        if self.defending_options(table):
            defence_card = random.choice(self.defending_options(table))
            self.remove_card(defence_card)
            table.update_table(defence_card)
            #print('Ai defend table\n{}'.format(table.show()))
            print('{} defended with {}'.format(self.nickname, defence_card))
            #print('T def: {}'.format(table.show()))
            return defence_card
        print(r"{} can't defend".format(self.nickname))
        print('table:', table.show())
        self.grab_table(table)
        return None

    def adding_card(self, table):
        if self.adding_card_options(table):
            card_to_add = random.choice(self.adding_card_options(table))
            self.remove_card(card_to_add)
            table.update_table(card_to_add)
            print('{} adding card {}'.format(self.nickname, card_to_add))
            #print('T add: {}'.format(table.show()))
            return card_to_add
        print('{} no cards to add'.format(self.nickname))
        print('table: {}'.format(table.show()))
        return None
