'''
Module that describes player behaviour for human player and AI player

-AIPlayerDumb
'''

import random

class Player:
    def __init__(self, nickname):
        self.nickname = nickname
        self.cards = []

    def draw_cards(self, deck_instance):
        n_cards_to_draw = 6 - len(self.cards)
        if n_cards_to_draw < 0:
            n_cards_to_draw = 0
        n_of_cards_left = len(deck_instance.encoded_cards)
        if n_of_cards_left > n_cards_to_draw:
            self.cards += deck_instance.encoded_cards[:n_cards_to_draw]
            deck_instance.update_deck(n_cards_to_draw)
        elif n_of_cards_left <= n_cards_to_draw:
            self.cards += deck_instance.encoded_cards[:]
            deck_instance.update_deck(n_of_cards_left)
        else:
            print('no cards to draw')

    def remove_card(self, card):
        self.cards.remove(card)

    def attacking_options(self):
        return self.cards

    def adding_card_options(self, table):
        table_card_types = [i[0] for i in table.cards]
        potential_cards = [card for card in self.cards if card[0] in table_card_types]
        return potential_cards

    def defending_options(self, table):
        #checking if incoming_card (last card on a table) is trump
        incoming_card = table.cards[-1]
        if incoming_card[1] == 0:
            possible_options = [card for card in self.cards
                                if (card[1] == 0 and card[0] >= incoming_card[0])]
        #checking possible options to beat non trump card
        else:
            non_trump_options = [card for card in self.cards if
                                 (card[1] == incoming_card[1] and card[0] >= incoming_card[0])]
            trump_cards = [card for card in self.cards if card[1] == 0]
            possible_options = non_trump_options + trump_cards
        return possible_options

    def grab_table(self, table):
        self.cards += table.cards
        table.clear()

    def _refresh(self):
        self.cards = []


class HumanPlayer(Player):
    def __init__(self, nickname):
        super().__init__(nickname)

    def attack(self, table):
        #print('n', print(len(self.cards)))
        #print(table.cards)
        print("Your Turn to attack, {}:".format(self.nickname))
        attack_card_num = input('{}\nPick a card number from 0 till {} '
                                .format(self.attacking_options(), len(self.attacking_options())-1))
        attack_card = self.attacking_options()[int(attack_card_num)]
        print('card {} added'.format(attack_card))
        self.remove_card(attack_card)
        table.update_table(attack_card)
        return attack_card

    def defend(self, table):
        print('T: {}'.format(table.show()))
        #print('n', print(len(self.cards)))
        #print(table.cards)
        if self.defending_options(table):
            print("Your Turn to defend, {}:".format(self.nickname))
            def_card_num = input("{}\nPick a card number from 0 till {}\n'g' to grab cards\n't' to check table\n'c' to show cards\n"
                                 .format(self.defending_options(table),
                                         len(self.defending_options(table))-1))
            if def_card_num == 'g':
                self.grab_table(table)
                return None
            elif def_card_num == 't':
                return 'T: {}'.format(self.defend(table))
            elif def_card_num == 'c':
                return self.cards
            defend_card = self.defending_options(table)[int(def_card_num)]
            print('card {} added'.format(defend_card))
            self.remove_card(defend_card)
            table.update_table(defend_card)
            return defend_card
        print(r"you can't defend, {}".format(self.nickname))
        self.grab_table(table)
        return None

    def adding_card(self, table):
        #print('n', print(len(self.cards)))
        if self.adding_card_options(table):
            #print('T: {}'.format(table.show()))
            print("Add card, {}:".format(self.nickname))
            adding_card_num = input("{}\nPick a card number from 0 till {}\n'p' to pass\n"
                                    .format(self.adding_card_options(table),
                                            len(self.adding_card_options(table))-1))
            if adding_card_num == 'p':
                return None
            card_to_add = self.adding_card_options(table)[int(adding_card_num)]
            print('card {} added'.format(card_to_add))
            self.remove_card(card_to_add)
            table.update_table(card_to_add)
            print('T: {}'.format(table.show()))
            return card_to_add
        return None

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
