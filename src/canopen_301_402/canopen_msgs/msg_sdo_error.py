#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_301.cob import CanOpenId
from canopen_301_402.assertions import Assertions

class CanOpenMessageSdoError(CanOpenMessage):
    """docstring for CanOpenMessageSdoError"""
    def __init__(self, canopen, node_id, index, subindex, error_code):
        Assertions.assert_node_id(node_id)
        Assertions.assert_index(index)
        Assertions.assert_subindex(subindex)

        self.canopen = canopen

        self.connection_set = self.canopen.get_connection_set(node_id)
        service = CanOpenService.sdo_tx
        function_code = self.connection_set.determine_function_code(service)

        data = [CanData.sdo_error]
        self._error_code = error_code

        # initialize CanOpenMessage
        super(CanOpenMessageSdoError, self).__init__(function_code, node_id, service, data)
        
        # set sdo write request message fields
        self._index = index
        self._subindex = subindex

    @property
    def error_code(self):
        return self._error_code

    @property
    def error_msg(self):
        if self.error_code in CanErrors:
            return CanErrors[self.error_code]
        else:
            return CanErrors.unknown % hex(self.error_code)
        return self._error_code

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
        @param cls: CanOpenMessageSdoError
        @param msg: CanOpenMessage
        @param canopen: CanOpen
        @result: None, if not possible, CanOpenMessageSdoError instance
        '''

        if ((msg.service == CanOpenService.sdo_rx) and
            (msg.node_id > 0) and 
            (len(msg.data) >= 8) and 
            (msg.data[0] == CanData.sdo_error)):

            index = msg.data[1] + (msg.data[2] << 8)
            subindex = msg.data[3]

            error_code = msg.data[4] | (msg.data[5]<<8) | (msg.data[6]<<16) | (msg.data[7]<<24)


            return CanOpenMessageSdoError(canopen, msg.node_id, index, subindex, error_code)
            
        else:
            return None

