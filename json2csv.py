#!/usr/bin/env python3

import csv
import json

image_base = 'https://raw.githubusercontent.com/umd-mith/irads/master/site/'

out = csv.DictWriter(open('site/index.csv', 'w'), fieldnames=[
    'id',
    'image',
    'title',
    'description',
    'facebook_url',
    'impressions',
    'clicks',
    'created',
    'ended',
    'cost',
    'currency',
    'location',
    'residence',
    'match',
    'interest',
    'behavior',
    'politics',
    'multicultural_affinity',
    'employer',
    'industry',
    'field_of_study',
    'exclude',
    'language',
    'age',
    'placement'
])


def unpack(item, *keys, none=True):
    '''
    extract data from parsed JSON using the provided keys. It will
    return a string, where multiple values are separated with a pipe
    if the extracted data resolves to a dictionary or any of the
    provided keys do not exist then None will be returned. If the
    none parameter is set to False then an empty string will be returned
    instead of None when there is no match.
    '''
    d = item
    for k in keys:
        if k in d:
            d = d[k]
        else:
            return None if none else ''
    if type(d) == list:
        return '|'.join(d)
    elif type(d) == dict:
        return None if none else ''
    else:
        return d

title_len = 40
def title(s):
    new_s = s.split('\n')[0].strip().replace('"', '')
    if len(new_s) > title_len:
        return new_s[0:title_len] + '…'
    else:
        return new_s

out.writeheader()

for item in json.load(open('site/index.json')):
    if not item['text']:
        continue

    # some ads lacked screenshots
    if item['image']:
        image = image_base + item['image']
    else:
        image = None

    # interests show up in two places in the json
    interest = unpack(item, 'targeting', 'interests', none=False) + '|'
    interest += unpack(item, 'targeting', 'people_who_match', 'interests', none=False)
    interest = interest.strip('|')

    out.writerow({
        'id': item['id'],
        'image': image,
        'title': title(item['text']),
        'description': item['text'].strip(),
        'facebook_url': item['url'],
        'impressions': item['impressions'],
        'clicks': item['clicks'],
        'impressions': item['impressions'],
        'created': item['created'],
        'ended': item['ended'],
        'cost': item['spend']['amount'],
        'currency': item['spend']['currency'],
        'location': unpack(item, 'targeting', 'location', 'united_states'),
        'residence': unpack(item, 'targeting', 'location_living_in', 'united_states'),
        'interest': interest,
        'behavior': unpack(item, 'targeting' 'behavior'),
        'politics': unpack(item, 'targeting', 'politics'),
        'multicultural_affinity': unpack(item, 'targeting', 'multicultural_affinity'),
        'employer': unpack(item, 'targeting', 'employers'),
        'industry': unpack(item, 'targeting', 'industry'),
        'field_of_study': unpack(item, 'targeting', 'field_of_study'),
        'match': unpack(item, 'targeting', 'people_who_match'),
        'exclude': unpack(item, 'targeting', 'excluded_connections'),
        'age': unpack(item, 'targeting', 'age'),
        'language': unpack(item, 'targeting', 'language'),
        'placement': unpack(item, 'targeting', 'placements'),
    })
