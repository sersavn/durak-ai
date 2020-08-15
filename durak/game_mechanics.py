import random
import sys
import time

# TODO:
'''
1. Add encoding legend +
2. Add Human player class +
3. Display trumps and cards left in deck in the begining of the round
4. Add ability to pick different Ai playstyles +
5. Encode cards back +
(6. Add way to collect data)
(7. Imporve game visualization)
(8. Make pygame version of a game)
'''

#fix Ai grab option
#fix Player commands during attack\defence

class Deck:
    '''
    | Class Deck is needed to simulate the card Deck.
    | It has following methods:
    | To initialize Deck instance needed to specify size (36 or 52 cards)

    | Attributes:
    | .encoded_cards
    | .suit_encode_legend
    | .trump
    '''
    def __init__(self, size):
        self.size = size
        #self.cards = self.get_deck() # self.cards > self.decoded_cards
        self.encoded_cards = self.get_deck()
        self.trump = self.encoded_cards[-1]

    def get_deck(self):
        '''
        Generates deck
        '''
        def card_range():
            try:
                if self.size == 52:
                    card_numbers = 4*list(range(2, 15))
                elif self.size == 36:
                    card_numbers = 4*list(range(6, 15))
                return card_numbers
            except UnboundLocalError as card_amount_err:
                print("{} Wrong amount of cards".format(card_amount_err))
                sys.exit(1)

        def random_deck():
            cards = card_range()
            suits = int(self.size/4) * [0, 1, 2, 3]
            resulted_deck = [[cards[i], suits[i]] for i in range(self.size)]
            random.shuffle(resulted_deck)
            return resulted_deck
        return random_deck()

    def update_deck(self, num_of_cards):
        self.encoded_cards = self.encoded_cards[num_of_cards:]


class DeckDecoder:
    '''
    Encoding all numerical back to str

    suits_pack = ['♠', '♥', '♦', '♣']
    no need for the class

    '''
    def __init__(self, deck_instance):
        self.deck_instance = deck_instance
        self.card_encode_legend = {'2' : '2',
                                   '3' : '3',
                                   '4' : '4',
                                   '5' : '5',
                                   '6' : '6',
                                   '7' : '7',
                                   '8' : '8',
                                   '9' : '9',
                                   '10' : '10',
                                   '11' : 'J',
                                   '12' : 'Q',
                                   '13' : 'K',
                                   '14' : 'A'}

    def decode(self):
        encode_legend_rev = dict([[v, k] for k, v in self.deck_instance.suit_encode_legend.items()])
        decoded_deck = [self.card_encode_legend[str(i[0])] + '_' + str(encode_legend_rev[i[1]]) \
                            for i in self.deck_instance.encoded_cards]
        self.deck_instance.cards = decoded_deck
        return decoded_deck

    def example(self):
        return('input:\n{}\noutput:\n{}'.format(self.deck_instance.encoded_cards,
                                                self.deck_instance.cards))

class Table:
    def __init__(self):
        self.cards = []

    def update_table(self, card):
        '''adding card to a table'''
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
        self._move_pointer_condition = self._init_move_pointer()
        self.attacker_id = self._move_pointer_condition[0]
        self.defender_id = self._move_pointer_condition[1]
        if self.attacker_id == self.defender_id:
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
    def __init__(self, players_list, pointer, deck, pile, logger=None):
        self.players_list = players_list
        self.pointer = pointer
        self.deck = deck
        self.logger = logger
        self.attacker = players_list[pointer.attacker_id]
        self.defender = players_list[pointer.defender_id]
        self.table = Table()
        self.pile = pile
        self.game_status = None

    def round_type(self):
        if self.check_if_deck_empty():
            print('self.game_status', self.game_status)
            return self.game_status
        if self._first_stage() is True:
            return "first_stage_finish"
        self._second_stage()
        return True

    def check_if_deck_empty(self):
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
                self.game_status = 'Draw'
                if self.logger:
                    self.logger.info({"Winner" : "Draw"})
                return 'DRAW'
            #else:
            self.game_status = winners[0]
            if self.logger:
                self.logger.info({"Winner" : str(self.game_status)})
            return 'WIN'

    def _first_stage(self):
        print('atk', len(self.attacker.cards))
        print('def', len(self.defender.cards))
        print('deck', len(self.deck.encoded_cards))
        self.attacker.attack(self.table)
        if self.logger:
            log_d = {"1_atk" : str(self.table.cards[-1]), "nick" : str(self.attacker.nickname),
                     "hand" : str(self.attacker.cards), "hand_size" : len(self.attacker.cards)}
            self.logger.info(log_d)
        # defender can't defend
        if self.defender.defend(self.table) is None:
            if self.logger:
                log_d = {"grab" : str(self.defender.nickname), "hand" : str(self.defender.cards),
                         "hand_size" : len(self.defender.cards)}
                self.logger.info(log_d)
            print('_first_stage no options for defender')
            self.attacker.draw_cards(self.deck)
            return True
        # defender defended successfully
        if self.logger:
            log_d = {"1_def" : str(self.table.cards[-1]), "nick" : str(self.defender.nickname),
                     "hand" : str(self.defender.cards), "hand_size" : len(self.defender.cards)}
            self.logger.info(log_d)
        return False

    def _second_stage(self):
        cnt = 1
        #while True and cnt < 6:
        while cnt < 6:
            if self.attacker.adding_card(self.table) is not None:
                cnt += 1
                if self.logger:
                    log_d = {"{}_add".format(cnt) : str(self.table.cards[-1]),
                             "nick" : str(self.attacker.nickname),
                             "hand" : str(self.attacker.cards),
                             "hand_size" : len(self.attacker.cards)}
                    self.logger.info(log_d)
                if self.defender.defend(self.table) is not None:
                    if self.logger:
                        log_d = {"{}_def".format(cnt) : str(self.table.cards[-1]),
                                 "nick" : str(self.defender.nickname),
                                 "hand" : str(self.defender.cards),
                                 "hand_size" : len(self.defender.cards)}
                        self.logger.info(log_d)

                else:
                    print('_second_stage no options for defender')
                    self.attacker.draw_cards(self.deck)
                    if self.logger:
                        log_d = {"grab" : str(self.defender.nickname),
                                 "hand" : str(self.defender.cards),
                                 "hand_size" : len(self.defender.cards)}
                        self.logger.info(log_d)
                    return False
            else:
                print('_seсond_stage no options for attacker')
                self.attacker.draw_cards(self.deck)
                self.defender.draw_cards(self.deck)
                self.pile.update(self.table)
                self.table.clear()
                self.attacker, self.defender = self.defender, self.attacker
                return False
        print('second_stage no cards')
        self.attacker.draw_cards(self.deck)
        self.defender.draw_cards(self.deck)
        self.pile.update(self.table)
        self.table.clear()
        self.attacker, self.defender = self.defender, self.attacker
        return False



class GameProcess:
    def __init__(self, players_list, deck, logger=None):
        self.players_list = players_list
        self.deck = deck
        self.logger = logger
        self.get_cards()
        self.pointer = Pointer(players_list)
        self.table = Table()
        self.pile = Pile()

    def _refresh_game(self):
        for player in self.players_list:
            player._refresh()

    def get_cards(self):
        for player in self.players_list:
            player.draw_cards(self.deck)

    def play(self):
        round = Round(self.players_list, self.pointer, self.deck, self.pile, self.logger)
        i = 0
        if self.logger:
            round_dict = {"Round" : i,
                          "pile" : self.pile.show(),
                          "cards_left" : len(self.deck.encoded_cards)}
            self.logger.info(round_dict)

        while round.game_status is None:
            print('\n')
            print("round {}".format(i))
            round.round_type()
            i += 1
            if self.logger:
                round_dict = {"Round" : i,
                              "pile" : self.pile.show(),
                              "cards_left" : len(self.deck.encoded_cards)}
                self.logger.info(round_dict)
        # game completed
        if round.game_status is not None:
            self._refresh_game()
            return round.game_status
            #print('round.game_status', round.game_status) # new line
