'''
Current module contains turn logic for implemented AI players.
Currently implemented:

-AIPlayerDumb
'''

import random
from player import Player

class AIPlayerDumb(Player):
    '''
    AI player with following abilities:
    1. Randomly picking card to start attack with
    2. Randomly picking card to use for defence
    3. Use all options while attacking
    4. Use all options for defence
    '''
    def attack(self, table):
        '''
        Randomly picks card to attack
        '''
        attack_card = random.choice(self.cards)
        self.remove_card(attack_card)
        table.update_table(attack_card)
        print('{} attack with {}'.format(self.nickname, attack_card))
        return attack_card

    def defend(self, table):
        '''
        Randomly picks card to defend based on defending_options
        '''
        if self.defending_options(table):
            defence_card = random.choice(self.defending_options(table))
            self.remove_card(defence_card)
            table.update_table(defence_card)
            print('{} defended with {}'.format(self.nickname, defence_card))
            return defence_card

        print(r"{} can't defend".format(self.nickname))
        print('table:', table.show())
        self.grab_table(table)
        return None

    def adding_card(self, table):
        '''
        Randomly picks card to add based on adding_card_options
        '''
        if self.adding_card_options(table):
            card_to_add = random.choice(self.adding_card_options(table))
            self.remove_card(card_to_add)
            table.update_table(card_to_add)
            print('{} adding card {}'.format(self.nickname, card_to_add))
            return card_to_add
        print('{} no cards to add'.format(self.nickname))
        print('table: {}'.format(table.show()))
        return None

class AIPlayerLowestCard(Player):
    '''
    AI player with following abilities:
    1. Picking lowest card to start attack with
    2. Picking lowest card to use for defence
    3. Use all options while attacking
    4. Use all options for defence
    '''
    def find_lowest_card(self, cards_list):
        '''
        Finding lowest card in the array

        *Non trump array cards always have less value than trump array cards (check the game rules)
        '''
        non_trump_arr = [i for i in cards_list if i[1] != 0]
        trump_arr = [i for i in cards_list if i[1] == 0]

        non_trump_arr = sorted(non_trump_arr, key=lambda x: x[0])
        trump_arr = sorted(trump_arr, key=lambda x: x[0])

        if non_trump_arr:
            return non_trump_arr[0]
        return trump_arr[0]

    def attack(self, table):
        attack_card = self.find_lowest_card(self.cards)

        self.remove_card(attack_card)
        table.update_table(attack_card)
        print('{} attack with {}'.format(self.nickname, attack_card))
        return attack_card

    def defend(self, table):
        if self.defending_options(table):
            defence_card = self.find_lowest_card(self.defending_options(table))

            self.remove_card(defence_card)
            table.update_table(defence_card)
            print('{} defended with {}'.format(self.nickname, defence_card))
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
            return card_to_add
        print('{} no cards to add'.format(self.nickname))
        print('table: {}'.format(table.show()))
        return None

class AIPlayerLowestCardDontWastingTrumps(Player):
    '''
    AI player with following abilities:
    1. Picking lowest card to start attack with
    2. Picking lowest card to use for defence
    3. Uses non-trump options while adding cards, start with smallest
    4. Uses all options for defence
    '''
    def find_lowest_card(self, cards_list):
        '''
        Finding lowest card in the array

        *Non trump array cards always have less value than trump array cards (check the game rules)
        '''
        non_trump_arr = [i for i in cards_list if i[1] != 0]
        trump_arr = [i for i in cards_list if i[1] == 0]

        non_trump_arr = sorted(non_trump_arr, key=lambda x: x[0])
        trump_arr = sorted(trump_arr, key=lambda x: x[0])

        if non_trump_arr:
            return non_trump_arr[0]
        return trump_arr[0]

    def find_non_trump_array(self, cards_list):
        non_trump_arr = [i for i in cards_list if i[1] != 0]
        non_trump_arr = sorted(non_trump_arr, key=lambda x: x[0])
        return non_trump_arr

    def attack(self, table):
        attack_card = self.find_lowest_card(self.cards)

        self.remove_card(attack_card)
        table.update_table(attack_card)
        print('{} attack with {}'.format(self.nickname, attack_card))
        return attack_card

    def defend(self, table):
        if self.defending_options(table):
            defence_card = self.find_lowest_card(self.defending_options(table))

            self.remove_card(defence_card)
            table.update_table(defence_card)
            print('{} defended with {}'.format(self.nickname, defence_card))
            return defence_card

        print(r"{} can't defend".format(self.nickname))
        print('table:', table.show())
        self.grab_table(table)
        return None

    def adding_card(self, table):
        if self.find_non_trump_array(self.adding_card_options(table)):
            card_to_add = self.find_lowest_card(self.find_non_trump_array(self.adding_card_options(table)))
            self.remove_card(card_to_add)
            table.update_table(card_to_add)
            print('{} adding card {}'.format(self.nickname, card_to_add))
            return card_to_add
        print('{} no cards to add'.format(self.nickname))
        print('table: {}'.format(table.show()))
        return None
