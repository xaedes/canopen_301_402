#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_msgs.cob import CanOpenId

class CanOpenMessageSdoWriteResponse(CanOpenMessage):
    """docstring for CanOpenMessageSdoWriteResponse"""
    def __init__(self, canopen, node_id, index, subindex, original_can_msg=None):

        self.canopen = canopen

        self.connection_set = self.canopen.connection_set
        service = CanOpenService.sdo_tx
        function_code = self.connection_set.determine_function_code(service)

        data = [CanData.sdo_download_response,
                (index & 0xff),        # index low byte
                (index >> 8),          # index high byte
                subindex]

        # initialize CanOpenMessage
        super(CanOpenMessageSdoWriteResponse, self).__init__(function_code, node_id, service, data, original_can_msg = original_can_msg)
        
        # set sdo write request message fields
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
        @param cls: CanOpenMessageSdoWriteResponse
        @param msg: CanOpenMessage
        @param canopen: CanOpen
        @result: None, if not possible, CanOpenMessageSdoWriteResponse instance
        '''

        if ((msg.service == CanOpenService.sdo_tx) and
            (msg.node_id > 0) and 
            (len(msg.data) >= 4) and 
            (msg.data[0] == CanData.sdo_download_response)):

            index = msg.data[1] + (msg.data[2] << 8)
            subindex = msg.data[3]

            return CanOpenMessageSdoWriteResponse(canopen, msg.node_id, index, subindex, original_can_msg = msg)
            
        else:
            return None

