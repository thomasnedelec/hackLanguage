# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 11:40:42 2016

@author: dudu
"""

class MLModel(object):
    def __init__(self):
        self.first_run = True
        self.weights = None
        self.language_dist = None