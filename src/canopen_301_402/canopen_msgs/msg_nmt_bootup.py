#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_301.cob import CanOpenId

class CanOpenMessageNmtBootup(CanOpenMessage):
    """docstring for CanOpenMessageNmtBootup"""
    def __init__(self, canopen, node_id):
        self.canopen = canopen

        self.connection_set = self.canopen.get_connection_set(node_id)
        service = CanOpenService.nmt_error_control
        function_code = self.connection_set.determine_function_code(service)
        
        data = [0]


        # initialize CanOpenMessage
        super(CanOpenMessageNmtBootup, self).__init__(function_code, node_id, service, data)
    
    
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
            (len(msg.data) == 1) and 
            (msg.data[0] == 0)):

            return CanOpenMessageNmtBootup(canopen, msg.node_id)
        else:
            return None

