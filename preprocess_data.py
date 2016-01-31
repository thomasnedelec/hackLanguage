# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 14:31:50 2016

@author: dudu
"""

import json
from nltk.tokenize import word_tokenize

def load_data(path):
    f = open(path, 'r')
    data_json = json.load(f)
    f.close()
    print 'length of table: ' + str(len(data_json))
    langs = {}
    count = 0
    for c in data_json:
        assert(len(c) >= 8)
        count += 1
        info = {}
        native = c[2]
        if langs.has_key(native) == False:
            langs[native] = []
        info['text'] = word_tokenize(c[1])
        info['level'] = c[7]
        langs[native].append(info)
        if count % 10000 == 0:
            print count
    return langs
    
if __name__ == '__main__':
    data = load_data('wikitalk/data/wiki_talk/data.json.txt.details')
    for native in data:
        print 'language: {}, size: {}'.format(native, len(data[native]))
        out = open('{}.json'.format(native), 'w')
        json.dump(data[native], out)
        out.close()
        
        