#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_msgs.cob import CanOpenId

class CanOpenMessageNmtRequest(CanOpenMessage):
    """docstring for CanOpenMessageNmtRequest"""
    def __init__(self, canopen):
        self.canopen = canopen

        # nmt message always uses default connection set (hence 0)
        self.connection_set = self.canopen.connection_set
        service = CanOpenService.nmt
        function_code = self.connection_set.determine_function_code(service)
        node_id = 0
        data = [] 

        # initialize CanOpenMessage
        super(CanOpenMessageNmtRequest, self).__init__(function_code, node_id, service, data) 
    
    def to_can_msg(self):
        '''
        @summary: convert to can.Message
        @result: 
        '''

        # node_id must always be zero for nmt messages
        arbitration_id = CanOpenId.encode(self.function_code, 0)
        
        # can request <=> is_remote_frame=True
        return can.Message(arbitration_id=arbitration_id,data=self.data,extended_id=False,is_remote_frame=True)

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
            (msg.request == True)): 

            return CanOpenMessageNmtRequest(canopen)

            
        else:
            return None
