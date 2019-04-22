'''
Idea is to parse data every second and save data here.
'''

import requests
import sys
import json
import time

class ParseData:
    def getting_data():
        start_time = time.time()
        try:
            r = requests.get('https://logic-games.spb.ru/fool/' ,verify=False)
        except requests.exceptions.RequestException as e:
            print('\n', e)
            sys.exit(1)
        reply = r.text
        with open("last_reply.txt", "w", errors = 'ignore') as text_file:
            text_file.write(reply)
        finish_time = time.time()
        print('\n', r.request.headers)
        print('\n', finish_time - start_time)


parse = ParseData.getting_data()
