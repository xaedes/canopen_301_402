#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.async_operation import AsyncOperation

from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoReadRequest
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoReadResponse
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoError

class SdoRead(AsyncOperation):
    """docstring for SdoWrite"""
    def __init__(self, node, index, subindex, *args, **kwargs):
        self.index = index
        self.subindex = subindex
        self.result = None
        super(SdoRead, self).__init__(node, *args, **kwargs)
        
    def do(self):
        self.canopen.send(CanOpenMessageSdoReadRequest(self.canopen, self.node.node_id, self.index, self.subindex))


    def process_msg(self, msg):
        if ((type(msg) == CanOpenMessageSdoReadResponse)
             and (msg.index == self.index)
             and (msg.subindex == self.subindex)):

            self.result = msg.read_data
            self.on_success()
            return True


        elif ((type(msg) == CanOpenMessageSdoError)
             and (msg.index == self.index)
             and (msg.subindex == self.subindex)):

            self.on_fault()
            return True
