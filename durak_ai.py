import random
import sys
import time

# TODO:
'''
1. Add encoding legend +
2. Add Human player class +
3. Display trumps and cards left in deck in the begining of the round
4. Add ability to pick different Ai playstyles
5. Encode cards back +
(6. Add way to collect data)
(7. Imporve game visualization)
(8. Make pygame version of a game)
'''

#fix Ai grab option
#fix Player commands during attack\defence

class Deck:
    '''
    Class Deck is needed to simulate the card Deck.
    It has following methods:
    To initialize Deck instance needed to specify size (36 or 52 cards)
    '''
    def __init__(self, size):
        self.size = size
        self.cards = self.get_deck()
        self.encoded_cards = DeckEncoder(self).encode()
        self.encode_legend = DeckEncoder(self).suit_encode()

    def get_deck(self):
        '''
        Generates deck
        '''
        def card_range():
            try:
                if self.size == 52:
                    card_numbers = [i for i in range(2, 15)]
                elif self.size == 36:
                    card_numbers = [i for i in range(6, 15)]
                return card_numbers
            except UnboundLocalError as card_amount_err:
                print("{} Wrong amount of cards".format(card_amount_err))
                sys.exit(1)

        def suits():
            suits_pack_ = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
            return suits_pack_

        def random_deck():
            cards = []
            for number in card_range():
                for suit in suits():
                    cards.append(str(number) + '_' + str(suit))
                    random.shuffle(cards)
            return cards
        return random_deck()

    def update_deck(self, num_of_cards):
        self.encoded_cards = self.encoded_cards[num_of_cards:]

    def show_last_card(self):
        return self.encoded_cards[-1]


class DeckEncoder:
    '''
    Encoding all str to numerical
    deck_instance == instance of the class Deck
    '''
    def __init__(self, deck_instance):
        self.deck_instance = deck_instance
        self.encode_legend = self.suit_encode()

    def suit_encode(self):
        suits = [(i.split('_')[1]) for i in self.deck_instance.cards]
        trump = suits[-1]
        suits_except_trump = list(set(suits))
        suits_except_trump.remove(trump)
        encode_dict = {trump : 0}
        encode_dict.update(dict([(val, num +1) for num, val in enumerate(suits_except_trump)]))
        #self.deck_instance.encode_legend = encode_dict
        return encode_dict

    def encode(self):
        splitted_deck = [(i.split('_')) for i in self.deck_instance.cards]
        for num, card in enumerate(splitted_deck):
            splitted_deck[num][0] = int(splitted_deck[num][0])
            splitted_deck[num][1] = self.encode_legend[card[1]]
        #self.deck_instance.encoded_cards = splitted_deck
        return splitted_deck


class DeckDecoder:
    '''
    Encoding all numerical back to str
    '''
    def __init__(self, deck_instance):
        self.deck_instance = deck_instance

    def decode(self):
        encode_legend_rev = dict([[v, k] for k, v in self.deck_instance.encode_legend.items()])
        decoded_deck = [str(i[0]) + '_' + str(encode_legend_rev[i[1]]) \
                        for i in self.deck_instance.encoded_cards]
        self.deck_instance.cards = decoded_deck

    def example(self):
        return('input:\n{}\noutput:\n{}'.format(self.deck_instance.encoded_cards, self.deck_instance.cards))


class Player:
    def __init__(self, nickname):
        self.nickname = nickname
        self.cards = []

    def draw_cards(self, deck_instance):
        n_cards_to_draw = 6 - len(self.cards)
        n_of_cards_left = len(deck_instance.encoded_cards)
        if n_of_cards_left > n_cards_to_draw:
            self.cards += deck_instance.encoded_cards[:n_cards_to_draw]
            deck_instance.update_deck(n_cards_to_draw)
        elif n_of_cards_left != 0:
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


class HumanPlayer(Player):
    def __init__(self, nickname):
        super().__init__(nickname)

    def attack(self, table):
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


class Table:
    def __init__(self):
        self.cards = []

    def update_table(self, card):
        self.cards += [card]

    def move_to_pile(self):
        pass

    def show(self):
        return self.cards

    def clear(self):
        self.cards = []

class Pile:

    def __init__(self):
        self.pile = []

    def update(self, table_instance):
        self.pile += table_instance.cards

    def clear_pile(self):
        self.pile = []

    def show(self):
        return self.pile

class Pointer:
    def __init__(self, list_of_player_instances):
        self.list_of_player_instances = list_of_player_instances
        self.attacker_id = self._init_move_pointer()[0]
        self.defender_id = self._init_move_pointer()[1]
        if self.attacker_id == self.defender_id:
            #fixme
            print(self.attacker_id, self.defender_id)
            print(list_of_player_instances[0].cards)
            print(list_of_player_instances[1].cards)
            sys.exit('wrong attacker/defender ids')

    def _init_move_pointer(self):
        start_dict = {}
        for the_player in self.list_of_player_instances:
            try:
                start_dict[the_player] = min([i[0] for i in the_player.cards if i[1] == 0])
            except ValueError:
                print(ValueError)
        try:
            attacker = min(start_dict, key=start_dict.get)
        except ValueError: #no trumps for all players
            attacker = (random.choice(self.list_of_player_instances))

        # determination of attacker and defender
        attacker_index = self.list_of_player_instances.index(attacker)
        if len(self.list_of_player_instances) - 1 == attacker_index:
            defender_index = 0
            return(attacker_index, defender_index)
        defender_index = attacker_index + 1
        return(attacker_index, defender_index)

    def switch(self): # useless?
        self.attacker_id = (self.attacker_id + 1) % 2
        self.defender_id = (self.defender_id + 1) % 2

    def show(self):
        return (self.attacker_id, self.defender_id)


class Round:
    def __init__(self, players_list, pointer, deck):
        self.players_list = players_list
        self.pointer = pointer
        self.deck = deck
        self.attacker = players_list[pointer.attacker_id]
        self.defender = players_list[pointer.defender_id]
        self.table = Table()
        self.pile = Pile()
        self.status = None

    def round(self):
        if self.check_cards():
            print(self.status)
            return self.status
        if self._first_stage() == True:
            return "first_stage_finish"
        self._second_stage()

    def check_cards(self):
        if self.deck.encoded_cards:
            pass
        else:
            return self.check_winner()

    def check_winner(self):
        winners = []
        if not self.attacker.cards:
            winners.append(self.attacker.nickname)
        if not self.defender.cards:
            winners.append(self.defender.nickname)
        if winners:
            if len(winners) == 2:
                self.status = 'Draw'
                return 'DRAW'
            else:
                self.status = winners[0]
                return 'WIN'

    def _first_stage(self):
        self.attacker.attack(self.table)
        if self.defender.defend(self.table) is None:
            print('_first_stage no options for defender')
            self.attacker.draw_cards(self.deck)
            return True
        return False

    def _second_stage(self):
        while True:
            if self.attacker.adding_card(self.table) is not None:
                if self.defender.defend(self.table) is not None:
                    pass

                else:
                    print('_second_stage no options for defender')
                    self.attacker.draw_cards(self.deck)
                    return False
            else:
                print('_seсond_stage no options for attacker')

                self.attacker.draw_cards(self.deck)
                self.defender.draw_cards(self.deck)
                self.pile.update(self.table)
                self.table.clear()
                print('1', self.pointer)
                self.attacker, self.defender = self.defender, self.attacker
                #self.pointer.switch()
                print('2', self.pointer)
                return False
        print('second_stage no cards')


class Game:
    def __init__(self, players_list, deck):
        self.players_list = players_list
        self.deck = deck
        self.get_cards()
        self.pointer = Pointer(players_list)
        self.table = Table()

    def get_cards(self):
        for player in self.players_list:
            player.draw_cards(self.deck)

    def play(self):
        r = Round(players_list, ptr, deck)
        i = 0
        t = time.time()
        while r.status is None:
            print('\n')
            print('round {}'.format(i))
            r.round()
            #time.sleep(0.05)

            i += 1
        print(time.time() - t)
        '''
        print(len(r.pile.show()))
        print(len(r.table.show()))
        print(len(r.attacker.cards))
        print(len(r.defender.cards))
        '''
#p1 = HumanPlayer('ANTOHA')
p1 = AiPlayerDumb('VALL E')
p2 = AiPlayerDumb('EVA')
players_list = [p1, p2]
deck = Deck(36)
g = Game(players_list, deck)
ptr = Pointer(players_list)
g.play()
