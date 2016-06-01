#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict

class CanOpenObjectDictionary(object):
    """docstring for CanOpenObjectDictionary"""
    def __init__(self):
        super(CanOpenObjectDictionary, self).__init__()
        self.objects = defaultdict(lambda:None)
        
        