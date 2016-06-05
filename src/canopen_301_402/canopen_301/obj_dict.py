#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict

from canopen_301_402.constants import *
from canopen_301_402.canopen_301.obj import CanOpenObject

class CanOpenObjectDictionary(object):
    """docstring for CanOpenObjectDictionary"""
    def __init__(self, canopen):
        super(CanOpenObjectDictionary, self).__init__()
        self.canopen
        self.objects = defaultdict(lambda:None)
        self.populate_with_defaults()
        
    def populate_with_defaults(self):
        # init controlword and statusword
        self.objects[Can402Objects.controlword] = CanOpenObject(self.canopen, *Can402Objects.controlword)
        self.objects[Can402Objects.statusword] = CanOpenObject(self.canopen, *Can402Objects.statusword)
        
        # set datatype of both to uint16
        self.objects[Can402Objects.controlword].datatype_id = CanOpenBasicDatatypes.uint16
        self.objects[Can402Objects.statusword].datatype_id = CanOpenBasicDatatypes.uint16
