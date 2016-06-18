#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_301.cob import CanOpenId
from canopen_301_402.assertions import Assertions

class CanOpenMessageSdoReadRequest(CanOpenMessage):
    """docstring for CanOpenMessageSdoReadRequest"""
    def __init__(self, canopen, node_id, index, subindex):
        Assertions.assert_node_id(node_id)
        Assertions.assert_index(index)
        Assertions.assert_subindex(subindex)

        self.canopen = canopen

        self.connection_set = self.canopen.get_connection_set(node_id)
        service = CanOpenService.sdo_rx
        function_code = self.connection_set.determine_function_code(service)

        data = [CanData.sdo_upload_request, # specifies, that we want to read value from object dictionary
                (index & 0xff),        # index low byte
                (index >> 8),          # index high byte
                subindex]              # 8 bit subindex


        # initialize CanOpenMessage
        super(CanOpenMessageSdoReadRequest, self).__init__(function_code, node_id, service, data)
        
        # set sdo read request message fields
        self._index = index
        self._subindex = subindex

    @property
    def index(self):
        return self._index
    
    @property
    def subindex(self):
        return self._subindex
    
    
    @classmethod
    def try_from_canopen_msg(cls, msg, canopen):
        '''
        @summary: try to convert from canopen msg
        @param cls: CanOpenMessageSdoReadRequest
        @param msg: CanOpenMessage
        @param canopen: CanOpen
        @result: None, if not possible, CanOpenMessageSdoReadRequest instance
        '''

        if ((msg.service == CanOpenService.sdo_rx) and
            (msg.node_id > 0) and  
            (len(msg.data) >= 4) and
            (msg.data[0] == CanData.sdo_upload_request)):


            print hex(msg.data[0])
            print hex(msg.data[1])
            print hex(msg.data[2])
            print hex(msg.data[3])

            index = msg.data[1] + (msg.data[2] << 8)
            subindex = msg.data[3]

            print hex(index)
            print hex(subindex)

            return CanOpenMessageSdoReadRequest(canopen, msg.node_id, index, subindex)

            
        else:
            return None
