#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_msgs.cob import CanOpenId

class CanOpenMessageNmtBootup(CanOpenMessage):
    """docstring for CanOpenMessageNmtBootup"""
    def __init__(self, canopen, node_id, original_can_msg=None):
        self.canopen = canopen

        self.connection_set = self.canopen.connection_set
        service = CanOpenService.nmt_error_control
        function_code = self.connection_set.determine_function_code(service)
        
        data = [0]


        # initialize CanOpenMessage
        super(CanOpenMessageNmtBootup, self).__init__(function_code, node_id, service, data, original_can_msg = original_can_msg)
    
    
    @classmethod
    def try_from_canopen_msg(cls, msg, canopen):
        '''
        @summary: try to convert from canopen msg
        @param cls: CanOpenMessageNmtBootup
        @param msg: CanOpenMessage
        @param canopen: CanOpen
        @result: None, if not possible, CanOpenMessageNmtBootup instance
        '''

        if ((msg.service == CanOpenService.nmt_error_control) and
            (msg.node_id > 0) and 
            (len(msg.data) >= 1) and 
            (msg.data[0] == 0)):

            return CanOpenMessageNmtBootup(canopen, msg.node_id, original_can_msg = msg)
        else:
            return None

