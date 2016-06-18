#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_301.cob import CanOpenId
from canopen_301_402.assertions import Assertions

class CanOpenMessageSdoWriteRequest(CanOpenMessage):
    """docstring for CanOpenMessageSdoWriteRequest"""
    def __init__(self, canopen, node_id, index, subindex, data):
        Assertions.assert_node_id(node_id)
        Assertions.assert_index(index)
        Assertions.assert_subindex(subindex)
        Assertions.assert_data(data,maximum_len=4)

        self.canopen = canopen

        self.connection_set = self.canopen.get_connection_set(node_id)
        service = CanOpenService.sdo_rx
        function_code = self.connection_set.determine_function_code(service)

        # set sdo write request message field
        self._write_data = data

        len_write_data = len(self._write_data)

        if len_write_data == 0:
            # if it is not necessary to specify number of data bytes
            sdo_download_request = CanData.sdo_download_request_bits - 1
        else:
            # encode number of data bytes to be written
            sdo_download_request = ((4-len_write_data)<<2) | CanData.sdo_download_request_bits
        
        data = ([sdo_download_request, # specifies, that we want to write value to object dictionary
                (index & 0xff),       # index low byte
                (index >> 8),           # index high byte
                subindex]             # 8 bit subindex
                + list(self._write_data))           # data to be written


        # initialize CanOpenMessage
        super(CanOpenMessageSdoWriteRequest, self).__init__(function_code, node_id, service, data)
        
        # set sdo write request message fields
        self._index = index
        self._subindex = subindex

    @property
    def index(self):
        return self._index
    
    @property
    def subindex(self):
        return self._subindex
    
    @property
    def write_data(self):
        return self._write_data
    
    
    @classmethod
    def try_from_canopen_msg(cls, msg, canopen):
        '''
        @summary: try to convert from canopen msg
        @param cls: CanOpenMessageSdoWriteRequest
        @param msg: CanOpenMessage
        @param canopen: CanOpen
        @result: None, if not possible, CanOpenMessageSdoWriteRequest instance
        '''

        if ((msg.service == CanOpenService.sdo_rx) and
            (msg.node_id > 0) and 
            (len(msg.data) >= 4)):

            len_write_data = None
            if (msg.data[0] == (CanData.sdo_download_request_bits-1)):
                len_write_data = 0
            elif ((msg.data[0] & CanData.sdo_download_request_bits) == CanData.sdo_download_request_bits):
                len_write_data = 4-((msg.data[0] >> 2) & 0b11)
            else:
                return None

            index = msg.data[1] + (msg.data[2] << 8)
            subindex = msg.data[3]
            write_data = msg.data[4:4+len_write_data]

            if len_write_data != len(write_data):
                return None

            return CanOpenMessageSdoWriteRequest(canopen, msg.node_id, index, subindex, write_data)

            
        else:
            return None

