import random
import sys
import time

# TODO:
'''
1. Add encoding legend
2. Add Human player class
3. Display trumps and cards left in deck in the begining of the round
4. Add ability to pick different Ai playstyles
5. Encode cards back
(6. Add way to collect data)
(7. Imporve game visualization)

'''

class Deck:
    '''
    Class Deck is needed to simulate the card Deck.
    It has following methods:
    To initialize Deck instance needed to specify deck_size (36 or 52 cards)
    - get_deck
    - update_deck
    - encode_deck
    '''
    def __init__(self, deck_size):
        self.deck_size = deck_size
        self.show_deck = []
        self.encode_legend = {}
        self.show_encoded_deck = []

    def get_deck(self):
        '''
        Generates deck
        '''
        def card_range():
            try:
                if self.deck_size == 52:
                    card_numbers = [i for i in range(2, 15)]
                elif self.deck_size == 36:
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

        self.show_deck = random_deck()

    def update_deck(self, cards_in_player_hand):
        '''
        Function is updating deck by substracting
        all cards taken by player from the ecnoded deck
        '''
        self.show_deck = 'show_deck is outdated. Please, use show_encoded_deck'
        self.show_encoded_deck = [i for i in self.show_encoded_deck
                                  if i not in cards_in_player_hand]

    def encode_deck(self):
        '''
        Hot encoding the deck
        Trump suit is encoded as 0.
        Other suits are encoded randomly
        '''
        def suit_encoding():
            suits = [(i.split('_')[1]) for i in self.show_deck]
            encode_dict = {}
            trump = suits[-1]
            suits_except_trump = list(set(suits))
            suits_except_trump.remove(trump)
            encode_dict[trump] = 0
            for num, val in enumerate(suits_except_trump):
                encode_dict[val] = num + 1
            self.encode_legend = encode_dict
            #print("SELF ENCPODE LEGEND", self.encode_legend)
            #print("!ENCODE_DICT OUTPUT", encode_dict)
            return encode_dict

        def apply_suit_encoding():
            splitted_deck = [(i.split('_')) for i in self.show_deck]
            for num, card in enumerate(splitted_deck):
                splitted_deck[num][0] = int(splitted_deck[num][0])
                splitted_deck[num][1] = suit_encoding()[card[1]]
            return splitted_deck

        self.show_encoded_deck = apply_suit_encoding()
        print("Suit encoding legend {}".format(suit_encoding()))

class Deck_Encoder:
    pass

class Deck_Decoder:
    pass
#    def __init__(self, encoded_deck_instance)

class Ai_Player:

    def __init__(self, nickname):
        self.nickname = nickname
        self.current_cards = []

    def draw_a_card(self, deck_container):
        cards_to_draw = 6 - len(self.current_cards)

        if len(deck_container) < cards_to_draw:
            return 'Deck is empty'
        if len(self.current_cards) < 6:
            self.current_cards += deck_container[:cards_to_draw]
            #self.current_cards = self.current_cards[0]# ?
        else:
            print('{} hand is full'.format(self.nickname))

    def attacking(self):
        card_to_throw = random.choice(self.current_cards)
        self.current_cards.remove(card_to_throw)
        return card_to_throw

    def throwing_a_card(self, table):
        table_card_types = [i[0] for i in table]
        potential_card = [card for card in self.current_cards if
                          card[0] in table_card_types]
        if potential_card:
            potential_card = random.choice(potential_card)
            self.current_cards.remove(potential_card)
            return potential_card
        return None

    def defending(self, incoming_card):
        #checking if incoming_card is trump
        if incoming_card[1] == 0:
            possible_options = [card for card in self.current_cards
                                if (card[1] == 0 and card[0] >= incoming_card[0])]
        #checking possible options to beat non trump card
        else:
            possible_options = [card for card in self.current_cards if
                                (card[1] == incoming_card[1] and card[0] >= incoming_card[0])]
            using_trump_cards = [card for card in self.current_cards if card[1] == 0]
            if using_trump_cards:
                possible_options = possible_options + using_trump_cards
        #checking can I beat incoming_card at all
        if not possible_options:
            return None
        defence_option = random.choice(possible_options)
        self.current_cards.remove(defence_option)
        return defence_option


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



def ai_vs_ai_100_games():
    curr_time = time.time()
    i = 0
    john = Ai_Player('John')
    peter = Ai_Player('Peter')
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

import numpy as np

#print(np.zeros((4,6)))
