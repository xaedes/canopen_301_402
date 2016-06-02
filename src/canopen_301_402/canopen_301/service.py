#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class CanOpenServiceBaseClass(object):
    def __init__(self, canopen):
        super(CanOpenServiceBaseClass, self).__init__()
        self.canopen = canopen
        
    def process_msg(self, msg):
        pass
        