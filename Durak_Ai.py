import itertools
import random
import sys
import time


class Deck:
    def __init__(self, deck_size, show_deck = None, show_encoded_deck = None):
        self.deck_size = deck_size
        if show_deck is None:
            show_deck = []
        self.show_deck = show_deck
        if show_encoded_deck is None:
            show_encoded_deck = []
        self.show_encoded_deck = show_encoded_deck

    def get_deck(self):
        def card_range():

            try:
                if self.deck_size == 52:
                    card_numbers = [i for i in range(2,15)]
                elif self.deck_size == 36:
                    card_numbers = [i for i in range(6,15)]
                return(card_numbers)
            except UnboundLocalError as e:
                print('\n', e)
                print("Wrong amount of cards")
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

        self.show_deck.append(random_deck())
        self.show_deck = self.show_deck[0]

    def update_deck(self, cards_in_player_hand):
        self.show_deck = 'show_deck is outdated. Please, use show_encoded_deck'
        self.show_encoded_deck = [i for i in self.show_encoded_deck if i not in cards_in_player_hand]

    def encode_deck(self):
        '''
        Trump suit is encoded by 0.
        Other suits are encoded randomly
        '''
        def get_encoding():
            suits = [(i.split('_')[1]) for i in self.show_deck]
            encode_dict = {}
            trump = suits[-1]
            suits_except_trump = list(set(suits))
            suits_except_trump.remove(trump)
            encode_dict[trump] = 0
            for num,val in enumerate(suits_except_trump):
                encode_dict[val] = num + 1
            return(encode_dict)

        def apply_encoding():
            splitted_deck = [(i.split('_')) for i in self.show_deck]
            for num, card in enumerate(splitted_deck):
                splitted_deck[num][0] = int(splitted_deck[num][0])
                splitted_deck[num][1] = get_encoding()[card[1]]
            return splitted_deck

        self.show_encoded_deck.append(apply_encoding())
        self.show_encoded_deck = self.show_encoded_deck[0]


class Player:
    def __init__(self, nickname, current_cards = None):
        self.nickname = nickname

        if current_cards is None:
            current_cards = []
        self.current_cards = current_cards
        #https://stackoverflow.com/questions/13564474/calling-a-method-of-a-class-on-one-object-affect-another-object-in-the-same-cl
    def draw_a_card(self, deck_container):
        cards_to_draw = 6 - len(self.current_cards)
        if len(deck_container) < cards_to_draw:
            print('Deck is empty. Stopping')
            #pass
            return 'Deck is empty'

        elif len(self.current_cards) < 6:
            self.current_cards += deck_container[:cards_to_draw]
            #self.current_cards = self.current_cards[0]# ?
        else:
            print('{} hand is full'.format(self.nickname))
            pass

    def attacking(self):
        card_to_throw = random.choice(self.current_cards)
        self.current_cards.remove(card_to_throw)
        return(card_to_throw)

    def throwing_a_card(self, table):
        table_card_types = [i[0] for i in table]
        potential_card = [card for card in self.current_cards if
        card[0] in table_card_types]
        if len(potential_card) != 0:
            potential_card = random.choice(potential_card)
            self.current_cards.remove(potential_card)
            return potential_card
        else:
            return None

    def defending(self, incoming_card):
        #checking if incoming_card is trump
        if incoming_card[1] == 0:
            possible_options = [card for card in self.current_cards if (card[1] == 0 and card[0] >= incoming_card[0])]
        #checking possible options to beat non trump card
        else:
            possible_options = [card for card in self.current_cards if (card[1] == incoming_card[1] and card[0] >= incoming_card[0])]
            print('good until here')
            using_trump_cards = [card for card in self.current_cards if card[1] == 0]
            if len(using_trump_cards) != 0:
                possible_options = possible_options + using_trump_cards
        #checking can I beat incoming_card at all
        if len(possible_options) == 0:
            return(None)
        else:
            defence_option = random.choice(possible_options)
            self.current_cards.remove(defence_option)
            return(defence_option)


class Game:
    def __init__(self, list_of_player_instances, deck_instance,
    table = None, release_deck = None, round_counter = None,
    attacker_index = None, defender_index = None):
        self.list_of_player_instances = list_of_player_instances
        self.deck_instance = deck_instance

        if table is None:
            table = []
        self.table = table

        if release_deck is None:
            release_deck = []
        self.release_deck = release_deck

        if round_counter is None:
            round_counter = 0
        self.round_counter = round_counter

        if attacker_index is None:
            attacker_index = 101 # a value that wiil be replaced
        self.attacker_index = attacker_index

        if defender_index is None:
            defender_index = 100
        self.defender_index = defender_index

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
        for p in self.list_of_player_instances:
            try:
                start_dict[p] = min([i[0] for i in p.current_cards if i[1] == 0])
            except ValueError: #no trumps at all case
                return(None)
        try:

            attacker = min(start_dict, key=start_dict.get)
        except ValueError: #no trumps for all players
            attacker = (random.choice(self.list_of_player_instances))
        # determination of attacker and defender
        attacker_index = self.list_of_player_instances.index(attacker)
        if len(self.list_of_player_instances) - 1 == attacker_index:
            defender_index = 0
            return(attacker_index, defender_index)
        else:
            defender_index = attacker_index + 1
            return(attacker_index, defender_index)

    def round(self):
        if self.round_counter == 0:
            '''
            Thinking that try except is faster than if else.
            Cant call init_move_pointer in case of no Trumps
            because calling function twice cause issues with random
            '''
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
        else:
            print('round non zero')
            pass
        print('\nROUND {}\n'.format(self.round_counter))
        def first_phase():
            '''
            attacker is attacking with any card
            defender is trying to defend
            '''
            attacker_card = attacker.attacking()
            self.table.append(attacker_card)
            print('attacker added card', self.table[0])
            defence_card = defender.defending(self.table[-1])
            if defence_card != None:
                self.table.append(defence_card)
                print('defender added card', self.table[-1])
                print('first_phase ok')
            else:
                defender.current_cards += self.table
                #self.table = []
                print('first_phase_failed')
                return('first_phase_failed')

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
                    print('attacker added additional_card', attacker_additional_card)
                else:
                    #try:
                    temp = self.attacker_index
                    self.attacker_index = self.defender_index
                    self.defender_index = temp
                    print('second_phase ok')
                    return('second_phase ok')
                    #except IndexError:
                        #return('second_phase no cards')

                print('table', self.table)
                defence_card = defender.defending(self.table[-1])

                if defence_card != None:
                    print('defender added additional card', defence_card)
                    self.table.append(defence_card)
                    #print('table', self.table)
                else:
                    print('defender cards', defender.current_cards)
                    defender.current_cards += self.table
                    print('second_phase failed')
                    return('second_phase failed')


        print("\n\nHERE")
        #attacker.draw_a_card(self.deck_instance.show_encoded_deck)
        #defender.draw_a_card(self.deck_instance.show_encoded_deck)
        print('attacker_index {}, defender_index {}'.format(self.attacker_index, self.defender_index))
        if first_phase() != 'first_phase_failed':
            second_phase()
        self.round_counter += 1
        self.table = []
        print('attacker_index {}, defender_index {}'.format(self.attacker_index, self.defender_index))
        print('self.table', self.table)
        print('defender cards', defender.current_cards)
        print('attacker cards', attacker.current_cards)
        return('switching to round {}'.format(self.round_counter))



def test():
    t = time.time()
    i = 0
    john = Player('John')
    peter = Player('Peter')
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
    print(time.time() - t)
test()
    #print('deck_len', len(game_1.deck_instance.show_encoded_deck))
    #print('cc[0]', game_1.list_of_player_instances[0].current_cards)
    #print('cc[1]', game_1.list_of_player_instances[1].current_cards)
