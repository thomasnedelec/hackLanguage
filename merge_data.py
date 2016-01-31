# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 21:07:15 2016

@author: dudu
"""

import json

if __name__ == '__main__':
    path = '/home/dudu/hack_cambridge/wikitalk/data/wiki_talk/data.json.txt.details'
    f = open(path, 'r')
    data_json = json.load(f)
    print 'dataset loaded'
    f.close()
    
    out = open('all.txt', 'w')
    for c in data_json:
        text = c[1]
        out.write(c[1].encode('utf8'))
        out.write('\n')
    out.close()
    