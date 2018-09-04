#!/usr/bin/env python3

import csv
import json

img = 'https://raw.githubusercontent.com/edsu/irads/master/site/images/{}.png'

out = csv.DictWriter(open('ads.csv', 'w'), fieldnames=[
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
    'exclude',
    'language',
    'age',
    'placement'
])

def unpack(item, *keys):
    d = item
    for k in keys:
        if k in d:
            d = d[k]
        else:
            return None
    if type(d) == list:
        return '|'.join(d)
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

for item in json.load(open('ads.json')):
    if not item['text']:
        continue
    out.writerow({
        'id': item['id'],
        'image': img.format(item['id']),
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
        'interest': unpack(item, 'targeting', 'interests'),
        'match': unpack(item, 'targeting', 'people_who_match'),
        'exclude': unpack(item, 'targeting', 'excluded_connections'),
        'age': unpack(item, 'age'),
        'language': unpack(item, 'targeting', 'language'),
        'placement': unpack(item, 'targeting', 'placements'),
    })
