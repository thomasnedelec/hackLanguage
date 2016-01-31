# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 01:04:06 2016

@author: dudu
"""

import os
import json

def list_what_necessary():
    path = '/home/dudu/hack_cambridge/jsons'
    
    for p in os.listdir(path):
        print p
        count = 0
        f = open('{}/{}'.format(path, p), 'r')
        data = json.load(f)
        print "all = " + str(len(data))
        for c in data:
            if len(c['text']) <= 30:
               count += 1 
        f.close()
        print count
        
def create_vocab_all():
    vocab = {'_PAD':0, '_GO':1, '_EOS':2, '_OOV':3}
    vocab2 = {}
    counter = 24
    counter2 = 4
    path = '/home/dudu/hack_cambridge/jsons'
    for p in os.listdir(path):
        print p
        vocab2[p] = counter2
        counter2 += 1
        
        f = open('{}/{}'.format(path, p), 'r')
        data = json.load(f)
        f.close()
        for c in data:
            tokens = c['text']
            tokens_counter = 0
            for t in tokens:
                if tokens_counter == 30: break
                tokens_counter += 1
                if vocab.has_key(t) == False:
                    vocab[t] = counter
                    counter += 1
    print 'finished'
    print counter
    out = open('vocab.json', 'w')
    json.dump(vocab, out)
    out.close()
    out = open('vocab_out.json', 'w')
    json.dumps(vocab2, out)
    out.close()
    
def create_vocab():
    vocab = {'_PAD':0, '_GO':1, '_EOS':2, '_OOV':3}
    vocab2 = {'_PAD':0, '_GO':1, '_EOS':2, '_OOV':3}
    counter2 = 4
    count_map = {}
    path = '/home/dudu/hack_cambridge/jsons'
    for p in os.listdir(path):
        print p
        vocab2[p] = counter2
        counter2 += 1
        
        f = open('{}/{}'.format(path, p), 'r')
        data = json.load(f)
        f.close()
        for c in data:
            tokens = c['text']
            tokens_counter = 0
            for t in tokens:
                if tokens_counter == 30: break
                tokens_counter += 1
                if count_map.has_key(t) == False:
                    count_map[t] = 0
                count_map[t] += 1
    print 'finished'
    cs = sorted(count_map.iteritems(), key=lambda x: x[1], reverse=True)
    print cs[:10]
    for i in range(40000):
        vocab[cs[i][0]] = i + 24
    out = open('vocab40k.json', 'w')
    json.dump(vocab, out)
    out.close()
    out = open('vocab_out.json', 'w')
    json.dump(vocab2, out)
    out.close()
    
def create_seq2seq_inputs():
    vocab_out = json.load(open('vocab_out.json', 'r'))
    vocab = json.load(open('vocab40k.json', 'r'))
    path = '/home/dudu/hack_cambridge/jsons'
    for p in os.listdir(path):
        print p
        f = open('{}/{}'.format(path, p), 'r')
        data = json.load(f)
        f.close()
        train_size = int(0.8 * len(data))
        counter = 0
        out = open('train_in_{}'.format(p), 'w')
        for com in data:
            if counter == train_size:
                out.close()
                out = open('dev_in_{}'.format(p), 'w')
            counter += 1
            tokens = com['text']
            size = len(tokens)
            output = []
            if size < 30:
                for i in range(30-size):
                    output.append(0)
            for i in range(min([size,30])):
                if vocab.has_key(tokens[i]):
                    output.append(vocab[tokens[i]])
                else:
                    output.append(3)
            out.write(' '.join([str(w) for w in output]))
            out.write('\n')
        out.close()
        out = open('train_out_{}'.format(p), 'w')
        for i in range(train_size):
            out.write('1 {} 2\n'.format(str(vocab_out[p])))
        out.close()
        out = open('dev_out_{}'.format(p), 'w')
        for i in range(train_size, len(data)):
            out.write('1 {} 2\n'.format(str(vocab_out[p])))
        out.close()
            
    
if __name__ == '__main__':
    #create_vocab()
    create_seq2seq_inputs()
        

        