'''
Module to wrangle data in a format good for model
'''

import pandas as pd
import json

def beautify_log():
    '''
    Transforms log to a more readable format
    '''
    path='game.log'

    log_data=open(path, 'r')

    dict_list = []

    for l in log_data:
        l = l.replace("'", "\"")
        l = json.loads(l)
        dict_list.append(l)
    df = pd.DataFrame(dict_list)
    df['Game'] = df['Game'].fillna(method='ffill')
    df['Round'] = df['Round'].fillna(method='ffill')
    df['pile'] = df['pile'].fillna(method='ffill')
    df['cards_left'] = df['cards_left'].fillna(method='ffill')
    df['Winner'] = df['Winner'].fillna(method='bfill')

    df = df[df['turn'].notna()]

    df = df.set_index(['Game', 'Round', 'turn'])
    df = df.dropna(thresh=1)
    df['grab'] = df['grab'].fillna(0)
    return df

#beautify_log()
