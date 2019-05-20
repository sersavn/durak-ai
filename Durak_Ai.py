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

'''

class Deck:
    '''
    Class Deck is needed to simulate the card Deck.
    It has following methods:
    To initialize Deck instance needed to specify size (36 or 52 cards)
    '''
    def __init__(self, size):
        self.size = size
        self.deck = self.get_deck()
        self.encoded_deck = []
        self.encode_legend = {}

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
        #self.deck = random_deck()

    def update_deck(self, num_of_cards):
        self.encoded_deck = self.encoded_deck[num_of_cards:]

    def show_last_card(self):
        self.deck[-1]

    #def show_trump(self):

'''
def update_deck(self, cards_in_player_hand):

    #Function is updating deck by substracting
    #all cards taken by player from the ecnoded deck

    self.deck = 'deck is outdated. Please, use show_encoded_deck'
    self.show_encoded_deck = [i for i in self.show_encoded_deck
                              if i not in cards_in_player_hand]
'''

class DeckEncoder:
    '''
    Encoding all str to numerical
    deck_instance == instance of the class Deck
    '''
    def __init__(self, deck_instance):
        self.deck_instance = deck_instance
        self._suit_encode()

    def _suit_encode(self):
        suits = [(i.split('_')[1]) for i in self.deck_instance.deck]
        trump = suits[-1]
        suits_except_trump = list(set(suits))
        suits_except_trump.remove(trump)
        encode_dict = {trump : 0}
        encode_dict.update(dict([(val, num +1) for num, val in enumerate(suits_except_trump)]))
        self.deck_instance.encode_legend = encode_dict

    def encode(self):
        splitted_deck = [(i.split('_')) for i in self.deck_instance.deck]
        for num, card in enumerate(splitted_deck):
            splitted_deck[num][0] = int(splitted_deck[num][0])
            splitted_deck[num][1] = self.deck_instance.encode_legend[card[1]]
        self.deck_instance.encoded_deck = splitted_deck

class DeckDecoder:
    '''
    Encoding all numerical back to str
    '''
    def __init__(self, deck_instance):
        self.deck_instance = deck_instance

    def decode(self):
        encode_legend_rev = dict([[v, k] for k, v in self.deck_instance.encode_legend.items()])
        decoded_deck = [str(i[0]) + '_' + str(encode_legend_rev[i[1]]) \
                        for i in self.deck_instance.encoded_deck]
        self.deck_instance.deck = decoded_deck

class Player:
    def __init__(self, nickname):
        self.nickname = nickname
        self.current_cards = []

    def draw_a_card(self, deck_instance):
        n_cards_to_draw = 6 - len(self.current_cards)
        n_of_cards_left = len(deck_instance.encoded_deck)
        if n_of_cards_left > n_cards_to_draw:
            self.current_cards += deck_instance.encoded_deck[:n_cards_to_draw]
            deck_instance.update_deck(n_cards_to_draw)
        elif n_of_cards_left != 0:
            self.current_cards += deck_instance.encoded_deck[:]
            deck_instance.update_deck(n_of_cards_left)
        else:
            print('no cards to draw')
            pass

    def remove_card(self, card):
        self.current_cards.remove(card)

    def attacking_options(self):
        return self.current_cards

    def adding_card_options(self, table):
        table_card_types = [i[0] for i in table.curr_table]
        potential_cards = [card for card in self.current_cards if
                           card[0] in table_card_types]
        return potential_cards

    def defending_options(self, table):
        #checking if incoming_card (last card on a table) is trump
        incoming_card = table.curr_table[-1]
        if incoming_card[1] == 0:
            possible_options = [card for card in self.current_cards
                                if (card[1] == 0 and card[0] >= incoming_card[0])]
        #checking possible options to beat non trump card
        else:
            non_trump_options = [card for card in self.current_cards if
                                (card[1] == incoming_card[1] and card[0] >= incoming_card[0])]
            trump_cards = [card for card in self.current_cards if card[1] == 0]
            possible_options = non_trump_options + trump_cards
        return possible_options

class HumanPlayer(Player):
    def __init__(self, nickname):
        super().__init__(nickname)

    def attacking(self):
        print("Your Turn to attack, {}!\nHere is your cards:".format(self.nickname))
        attack_card_num = input('{}\n Pick a card number from 0 till {} '
                                .format(self.attacking_options(), len(self.attacking_options())-1))
        attack_card = self.attacking_options()[int(attack_card_num)]
        self.remove_card(attack_card)
        return attack_card

    def defending(self, table):
        print("Your Turn to defend, {}!\nHere are your options: ".format(self.nickname))
        def_card_num = input('{}\n Pick a card number from 0 till {} '
                                .format(self.defending_options(table), len(self.defending_options(table))-1))
        defend_card = self.defending_options(table)[int(attack_card_num)]
        self.remove_card(defend_card)
        return defend_card

    def adding_card(self,table):
        print("Your Turn to add cards, {}!\nHere are your options: ".format(self.nickname))
        adding_card_num = input('{}\n Pick a card number from 0 till {} ')
                                .format(self.adding_card_options(table), len(self.adding_card_options(table))-1))
        card_to_add = self.adding_card_options(table)[int(adding_card_num)]
        self.remove_card(card_to_add)
        return card_to_add

class AiPlayerDumb(Player):
    def __init__(self, nickname):
        super().__init__(nickname)

    def attacking(self):
        attack_card = random.choice(self.current_cards)
        self.remove_card(attack_card)
        return attack_card

    def defending(self, incoming):
        defence_card = random.choice(possible_options)
        self.remove_card(defence_card)
        return defence_card

class Table:
    def __init__(self):
        self.curr_table = curr_table
        pass

    def update_table(self):
        pass

    def move_to_pile(self):
        pass

class Pile:

    def __init__(self):
        self.pile = []

    def update_pile(self, list_of_cards):
        self.pile += list_of_cards

    def clear_pile(self):
        self.pile = []

class Game:
    def __init__(self, list_of_player_instances, deck_instance):
        self.list_of_player_instances = list_of_player_instances
        self.deck_instance = deck_instance
        self.table = []
        self.release_deck = []
        self.round_counter = 0
        self.attacker_index = 101 # a value that wiil be replaced
        self.defender_index = 100
        print('\nGAME STARTS\n')

    def get_first_cards(self):
        self.deck_instance.get_deck()
        self.deck_instance.encode_deck()
        for player in self.list_of_player_instances:
            player.draw_a_card(self.deck_instance.show_encoded_deck)
            self.deck_instance.update_deck(player.current_cards)

    def get_cards(self):
        for player in self.list_of_player_instances:
            player.draw_a_card(self.deck_instance.show_encoded_deck)
            self.deck_instance.update_deck(player.current_cards)

    def init_move_pointer(self):
        '''
        works only for two palyers
        '''
        start_dict = {}
        for the_player in self.list_of_player_instances:
            try:
                start_dict[the_player] = min([i[0] for i in the_player.current_cards if i[1] == 0])
            except ValueError: #no trumps at all case
                return None
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

    def round(self):
        if self.round_counter == 0:
            try:
                self.attacker_index = self.init_move_pointer()[0]
                self.defender_index = self.init_move_pointer()[1]
            except:
                new_ids = [0, 1]
                random.shuffle(new_ids)
                self.attacker_index = new_ids[0]
                self.defender_index = new_ids[1]

        attacker = self.list_of_player_instances[self.attacker_index]
        defender = self.list_of_player_instances[self.defender_index]

        if self.attacker_index == self.defender_index:
            print('same indexes')
            quit()
        print('\nROUND {}\n'.format(self.round_counter))
        def first_phase():
            '''
            attacker is attacking with any card
            defender is trying to defend
            '''
            attacker_card = attacker.attacking()
            self.table.append(attacker_card)
            print('attacking with card', self.table[0])
            defence_card = defender.defending(self.table[-1])
            if defence_card != None:
                self.table.append(defence_card)
                print('defender added card', self.table[-1])
            else:
                defender.current_cards += self.table
                #self.table = []
                print(r"defender can't beat first attacker card")
                return 'first_phase_failed'

        def second_phase():
            '''
            attacker is adding additional cards based on table contents
            defender is trying to defend
            '''
            for i in range(5): # 5 additional_cards possible in 1v1 game
                #time.sleep(0.5)
                attacker_additional_card = attacker.throwing_a_card(self.table)

                if attacker_additional_card != None:
                    self.table.append(attacker_additional_card)
                    print('throwing a', attacker_additional_card)
                else:
                    #try:
                    temp = self.attacker_index
                    self.attacker_index = self.defender_index
                    self.defender_index = temp
                    print('defender successfully defended this round')
                    return 'second_phase ok'
                    #except IndexError:
                        #return('second_phase no cards')


                def beautify_table():
                    '''
                    Used instead of using
                    print('table', self.table)
                    All defender cards is on top part of the table
                    While attacker cards is on bottom part of the table
                    '''
                    defender_cards = [val for num,val in enumerate(self.table) if num%2==1]
                    print('\nCurrent cards on a table:\ndefender cards', defender_cards)
                    attacker_cards = [val for num,val in enumerate(self.table) if num%2==0]
                    print('attacker cards {}\n'.format(attacker_cards))
                beautify_table()
                defence_card = defender.defending(self.table[-1])

                if defence_card != None:
                    print('defending with', defence_card)
                    self.table.append(defence_card)
                    #print('table', self.table)
                else:
                    print('defender cards', defender.current_cards)
                    defender.current_cards += self.table
                    print(r"defender can't defend from additional cards")
                    print('\ndefender collecting cards')
                    return 'second_phase failed'


        #attacker.draw_a_card(self.deck_instance.show_encoded_deck)
        #defender.draw_a_card(self.deck_instance.show_encoded_deck)
        print('attacker_index {}, defender_index {}'
              .format(self.attacker_index, self.defender_index))
        if first_phase() != 'first_phase_failed':
            second_phase()
        self.round_counter += 1
        self.table = []
        print('attacker_index {}, defender_index {}'
              .format(self.attacker_index, self.defender_index))
        print('defender cards', defender.current_cards)
        print('attacker cards', attacker.current_cards)
        return 'switching to round {}'.format(self.round_counter)

j = time.time()
deck = Deck(36)
print(deck.deck)
Deck_Encoder = DeckEncoder(deck)
Deck_Encoder.encode()
print('\n')
Deck_Decoder = DeckDecoder(deck)
Deck_Decoder.decode()
p1 = HumanPlayer('ANTOHA')
p1.draw_a_card(deck)
print(p1.attacking())
#pr
#deck.suit_encoding()
#print(deck.deck)
#print(deck.encode_legend)
#decoded_deck = DeckEncoder(deck)#.decode()
#print(decoded_deck.decode())


'''
def ai_vs_ai_100_games():
    curr_time = time.time()
    i = 0
    john = AiPlayer('John')
    peter = AiPlayer('Peter')
    list_of_players = [john, peter]
    while i != 100:
        print('\n\n', i, '\n\n')
        try:
            game_1.round()
            game_1.get_cards()
            time.sleep(0.001)
        except:
            i += 1
            game_1 = Game(list_of_players, Deck(36))
            game_1.get_first_cards()
            time.sleep(0.001)
    print(time.time() - curr_time)

ai_vs_ai_100_games()
'''

#print(np.zeros((4,6)))
