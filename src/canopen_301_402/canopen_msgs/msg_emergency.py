#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_msgs.cob import CanOpenId

class CanOpenMessageEmergency(CanOpenMessage):
    """docstring for CanOpenMessageEmergency"""
    def __init__(self, canopen, node_id, error_code, error_register, manufacturer_error=None, original_can_msg=None):
        '''
        @summary: 
        @param canopen: CanOpen instance
        @param node_id: 7 bit node id
        @param error_code: 16 bit error code, lower 8 bit application specific
        @param error_register: 8 bit error register content (can object 0x1001.00)

        @result: CanOpenMessageEmergency
        '''
        self.canopen = canopen
        self.error_code = error_code
        self.error_register = error_register
        self.manufacturer_error = manufacturer_error

        # nmt message always uses default connection set (hence 0)
        self.connection_set = self.canopen.connection_set
        service = CanOpenService.nmt
        function_code = self.connection_set.determine_function_code(service)

        data = [Can301StateCommandBits[command], node_id]

        # initialize CanOpenMessage
        super(CanOpenMessageEmergency, self).__init__(function_code, node_id, service, data, original_can_msg = original_can_msg)
        
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
        @param cls: CanOpenMessageEmergency
        @param msg: CanOpenMessage
        @param canopen: CanOpen
        @result: None, if not possible, CanOpenMessageEmergency instance
        '''

        if (msg.service == CanOpenService.emergency):

            node_id = msg.data[1] 
            command_bits = msg.data[0]
            command = None
            for _command,bits in Can301StateCommandBits.iteritems():
                if command_bits == bits:
                    command = _command
                    break
            
            if command is None:
                return None

            return CanOpenMessageEmergency(canopen, node_id, command, original_can_msg = msg)

            
        else:
            return None
