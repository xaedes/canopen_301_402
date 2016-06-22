#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.async_operation import AsyncOperation

from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoWriteRequest
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoWriteResponse
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoError

class SdoWrite(AsyncOperation):
    """docstring for SdoWrite"""
    def __init__(self, node, index, subindex, data, *args, **kwargs):
        self.index = index
        self.subindex = subindex
        self.data = data

        if "timeout" not in kwargs:
            kwargs["timeout"] = node.atomic_timeout

        super(SdoWrite, self).__init__(node, *args, **kwargs)
        
    def do(self):
        self.canopen.send(CanOpenMessageSdoWriteRequest(self.canopen, self.node.node_id, self.index, self.subindex, self.data))


    def process_msg(self, msg):
        if ((type(msg) == CanOpenMessageSdoWriteResponse)
             and (msg.index == self.index)
             and (msg.subindex == self.subindex)):

            self.on_success()
            return True
            
        elif ((type(msg) == CanOpenMessageSdoError)
             and (msg.index == self.index)
             and (msg.subindex == self.subindex)):

            self.on_fault()
            return True
