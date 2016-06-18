#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class CanOpenServiceBaseClass(object):
    def __init__(self, node):
        super(CanOpenServiceBaseClass, self).__init__()
        self.node = node
        self.canopen = node.canopen
        
    def process_msg(self, msg):
        pass
    
    def process_sent_msg(self, msg):
        pass
        