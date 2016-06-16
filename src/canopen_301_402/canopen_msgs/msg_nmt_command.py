#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_301.cob import CanOpenId

class CanOpenMessageNmtCommand(CanOpenMessage):
    """docstring for CanOpenMessageNmtCommand"""
    def __init__(self, canopen, node_id, command):
        '''
        @summary: 
        @param canopen: CanOpen instance
        @param node_id: 7 bit node id
        @param command: Can301StateCommand
        @result: CanOpenMessageNmtCommand
        '''
        self.canopen = canopen

        # nmt message always uses default connection set (hence 0)
        self.connection_set = self.canopen.get_connection_set(0)
        service = CanOpenService.nmt
        function_code = self.connection_set.determine_function_code(service)

        data = [Can301StateCommandBits[command], node_id]

        # initialize CanOpenMessage
        super(CanOpenMessageNmtCommand, self).__init__(function_code, node_id, service, data)
        
        # set nmt message fields
        self._node_id = node_id # this overwrites CanOpenMessage.node_id
        self._command = command

    @property
    def command(self):
        '''
        @summary: Can301StateCommand
        '''
        return self._command
    
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
        @param cls: CanOpenMessageNmtCommand
        @param msg: CanOpenMessage
        @param canopen: CanOpen
        @result: None, if not possible, CanOpenMessageNmtCommand instance
        '''

        if ((msg.service == CanOpenService.nmt) and
            (msg.node_id == 0) and 
            (len(msg.data) >= 2)):

            node_id = msg.data[1] 
            command_bits = msg.data[0]
            command = None
            for _command,bits in Can301StateCommandBits.iteritems():
                if command_bits == bits:
                    command = _command
                    break
            
            if command is None:
                return None

            return CanOpenMessageNmtCommand(canopen,node_id,command)

            
        else:
            return None
