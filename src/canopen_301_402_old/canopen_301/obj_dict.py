#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict

from canopen_301_402.constants import *
from canopen_301_402.canopen_301.obj import CanOpenObject

class CanOpenObjectDictionary(object):
    """docstring for CanOpenObjectDictionary"""
    def __init__(self, node):
        super(CanOpenObjectDictionary, self).__init__()
        self.node = node
        self.canopen = self.node.canopen
        self.objects = defaultdict(lambda:None)
