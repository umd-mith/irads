#!/usr/bin/env python3

import json
import collections

money = collections.Counter()
clicks = collections.Counter()
impressions = collections.Counter()

for ad in json.load(open('../ads.json')):
    if 'people_who_match' in ad['targeting'] and 'interests' in ad['targeting']['people_who_match']: 
        for s in ad['targeting']['people_who_match']['interests']:
            money[s] += float(ad['spend']['amount'])
            clicks[s] += ad['clicks']
            impressions[s] += ad['impressions']

print("money,clicks,impressions,interest")
for name, amount in money.most_common():
    print('{:.2f},{},{},{}'.format(amount, clicks[name], impressions[name], name))
