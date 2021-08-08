import json
import os

with open('weiming_fatal_jobs.json', 'r') as fp:
    a = json.load(fp)
    a_l = [i['name'] for i in a]
    a_l = [i.split('_') if '_' in i else i.split('-') for i in a_l]
    a_l = [i[2] if i[0] == 'us' else i[0] for i in a_l]
    a_l = set(a_l)
    print('\n'.join(a_l))
    # print(a_l)