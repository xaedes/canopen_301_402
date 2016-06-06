#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_301.cob import CanOpenId

class CanOpenMessageNmtRequest(CanOpenMessage):
    """docstring for CanOpenMessageNmtRequest"""
    def __init__(self, canopen):
        self.canopen = canopen

        # nmt message always uses default connection set (hence 0)
        self.connection_set = self.canopen.get_connection_set(0)
        service = CanOpenService.nmt
        function_code = self.connection_set.determine_function_code(service)
        node_id = 0

        data = [] # i thought [] as data would be request, but it wont work

        # todo: this does not seem to create a proper remote request
        # candump vcan0
        #   vcan0  000   [0]  remote request    # it should look like this
        #   vcan0  000   [0]                    # this is the current output

        # initialize CanOpenMessage
        super(CanOpenMessageNmtRequest, self).__init__(function_code, node_id, service, data)
    
    def to_can_msg(self):
        '''
        @summary: convert to can.Message
        @result: 
        '''

        # node_id must always be zero for nmt messages
        arbitration_id = CanOpenId.encode(self.function_code, 0)
            
        return can.Message(arbitration_id=arbitration_id,data=self.data,extended_id=False)

    @classmethod
    def try_from_canopen_msg(cls, msg, canopen):
        '''
        @summary: try to convert from canopen msg
        @param cls: CanOpenMessageNmtRequest
        @param msg: CanOpenMessage
        @param canopen: CanOpen
        @result: None, if not possible, CanOpenMessageNmtRequest instance
        '''

        if ((msg.service == CanOpenService.nmt) and
            (msg.node_id == 0) and 
            (len(msg.data) == 0)): # todo add proper check for request

            return CanOpenMessageNmtRequest(canopen)

            
        else:
            return None
