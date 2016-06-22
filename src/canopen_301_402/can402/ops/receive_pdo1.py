#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.constants import *
from canopen_301_402.async.async_operation import AsyncOperation
from canopen_301_402.canopen_msgs.msgs import CanOpenMessage

import struct

class ReceivePdo1(AsyncOperation):
    """docstring for ReceivePdo1"""
    def __init__(self, node, *args, **kwargs):
        super(ReceivePdo1, self).__init__(node, *args, **kwargs)
        self.node = node
        
    def process_msg(self, msg):
        if ((type(msg) == CanOpenMessage) 
            and (msg.service == CanOpenService.pdo1_tx)):
            
            value, = struct.unpack("<H",msg.data) #uint16
            self.node.statusword = value
