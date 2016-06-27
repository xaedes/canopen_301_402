#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_msgs.cob import CanOpenId

class CanOpenMessageSdoReadResponse(CanOpenMessage):
    """docstring for CanOpenMessageSdoReadResponse"""
    def __init__(self, canopen, node_id, index, subindex, data, original_can_msg=None):

        self.canopen = canopen

        self.connection_set = self.canopen.connection_set
        service = CanOpenService.sdo_tx
        function_code = self.connection_set.determine_function_code(service)

        self._read_data = data

        len_read_data = len(self._read_data)

        # encode number of data bytes to be written
        sdo_upload_response = ((4-len_read_data)<<2) | CanData.sdo_upload_response


        data = ([sdo_upload_response, # specifies, that we want to read value from object dictionary
                (index & 0xff),        # index low byte
                (index >> 8),          # index high byte
                subindex] +             # 8 bit subindex
                list(self._read_data))

        # initialize CanOpenMessage
        super(CanOpenMessageSdoReadResponse, self).__init__(function_code, node_id, service, data, original_can_msg = original_can_msg)
        
        # set sdo read request message fields
        self._index = index
        self._subindex = subindex

    @property
    def index(self):
        return self._index
    
    @property
    def subindex(self):
        return self._subindex
    
    @property
    def read_data(self):
        return self._read_data
    
    
    @classmethod
    def try_from_canopen_msg(cls, msg, canopen):
        '''
        @summary: try to convert from canopen msg
        @param cls: CanOpenMessageSdoReadResponse
        @param msg: CanOpenMessage
        @param canopen: CanOpen
        @result: None, if not possible, CanOpenMessageSdoReadResponse instance
        '''

        if ((msg.service == CanOpenService.sdo_tx) and
            (msg.node_id > 0) and  
            (len(msg.data) >= 4) and
            ((msg.data[0] & CanData.sdo_upload_response) == CanData.sdo_upload_response)):

            index = msg.data[1] + (msg.data[2] << 8)
            subindex = msg.data[3]
            len_response_data = 4-((msg.data[0] >> 2) & 0b11)
            data = msg.data[4:4+len_response_data]

            return CanOpenMessageSdoReadResponse(canopen, msg.node_id, index, subindex, data, original_can_msg = msg)

            
        else:
            return None
