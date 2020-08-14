player_name = 'AABC'
player_name2 = 'BBAS'

suits = ['♠', '♥', '♦',	'♣']
cards = []

def draw_card(suit, card):
    first_line = '|{} {}|'.format(suit, card)
    second_line = '|   |'
    third_line = '|{} {}|'.format(card, suit)
    combined_lines = first_line + '\n' + second_line + '\n' + third_line
    return combined_lines

def draw_multiple_cards_hidden(cards_with_suits):
    first_line = '   '
    second_line = '   '
    third_line = '   '

    for num, card in enumerate(cards_with_suits):
        first_line += "|- -|" + '   '
        second_line += "|   |" + '   '
        third_line += "|- -|" + '   '

    print(first_line)
    print(second_line)
    print(third_line)

def draw_multiple_cards(cards_with_suits):
    first_line = '   '
    second_line = '   '
    third_line = '   '

    number_line = '   '

    for num, card in enumerate(cards_with_suits):
        card_pic = draw_card(card[0], card[1])
        first_line += card_pic.split('\n')[0] + '   '
        second_line += card_pic.split('\n')[1] + '   '
        third_line += card_pic.split('\n')[2] + '   '

        number_line += '  {} '.format(num) + '    '

    #print(len(first_line))
    print(first_line)
    print(second_line)
    print(third_line)
    print('\n')
    print('Use numbers below to select card')
    print(number_line)
    #print(len(first_line))
    return True#(len(first_line))

def draw_deck(trump_card):
    space = [' '] * 60
    space = "".join(space)
    #space = '                                     '

    print('{}=====|- -|'.format(space))
    print('{}| {} |   |'.format(space, trump_card))
    print('{}=====|- -|'.format(space))
    pass


print('\n')
draw_multiple_cards_hidden(['9♠', 'K♦', 'J♦'])
print('\n')
draw_deck('9♠')
print('\n')
draw_multiple_cards(['9♠', 'K♦', 'J♦'])
