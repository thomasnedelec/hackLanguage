# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 21:17:57 2016

@author: dudu
"""

import word2vec

if __name__ == '__main__':
    path = '/home/dudu/hack_cambridge/all.txt'
    out_path = '/home/dudu/hack_cambridge/cambridge/word2vec_model.bin'
    word2vec.word2vec(path, out_path, size=10, verbose=True)