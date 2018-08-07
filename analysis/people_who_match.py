#!/usr/bin/env python3

import json
import collections

money = collections.Counter()
clicks = collections.Counter()
impressions = collections.Counter()

for ad in json.load(open('ads.json')):
    if 'people_who_match' in ad['targeting'] and type(ad['targeting']['people_who_match']) == list:
        for s in ad['targeting']['people_who_match']:
            money[s] += float(ad['spend']['amount'])
            clicks[s] += ad['clicks']
            impressions[s] += ad['impressions']

print("money (RUB),clicks,impressions,people_who_match")
for name, amount in money.most_common():
    print('{:.2f},{},{},{}'.format(amount, clicks[name], impressions[name], name))
