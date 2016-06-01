#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.canopen_301.eds import *
from canopen_301_402.canopen_301.datatypes import CanDatatypes
from canopen_301_402.canopen_301.state import Can301State
from canopen_301_402.canopen_301.nmt import CanOpenNetworkManagement
from canopen_301_402.canopen_301.sdo import CanOpenSdoTransfer
from canopen_301_402.canopen_301.pdo import CanOpenPdoTransfer


class CanOpenId():
    '''
    @summary: can open interpretation of can id:
        
        only 11 bit arbitration_id is allowed

        upper 4 bits of the 11 bit arbitration_id are the function code
        lower 7 bits of the 11 bit arbitration_id are the node_id
    '''

    @classmethod
    def decode(cls, can_id):
        '''
        @summary:  split 11 bit can_id in 4 bit function code and 7 bit node_id
        @param cls:
        @param can_id: 11 bit can_id
        @result: tuple of 4 bit function code and 7 bit node_id
        '''
        Assertions.assert_can_id(can_id)

        function_code = (can_id >> 7) & 0b1111
        node_id = can_id & 0b1111111

        return function_code, node_id

    @classmethod
    def encode(cls, function_code, node_id):
        '''
        @summary: build 11 bit can_id from 4 bit function code and 7 bit node_id
        @param cls:
        @param function_code: 4 bit function code
        @param node_id: 7 bit node_id
        @result: 11 bit can_id
        '''
        Assertions.assert_function_code(function_code)
        Assertions.assert_node_id(node_id)

        can_id = (function_code << 7) | node_id

        return can_id        

class CanOpen(CanOpenNetworkManagement,CanOpenSdoTransfer,CanOpenPdoTransfer,can.Listener):
    """docstring for CanOpen"""
    def __init__(self, bus, eds_filename):
        super(CanOpen, self).__init__()
        self.bus = bus

        self.eds = EdsFile()
        self.eds.read(eds_filename)

        self.notifier = can.Notifier(self.bus,[self])

        self.datatypes = CanDatatypes()

        self.response_callbacks = dict()

    def send_can(self, can_id, data):
        '''
        @summary: send message with data to 11 bit can_id 
        @param bus: can.Bus
        @param can_id: CanID (11bit)
        @param data: [byte] 0 <= len(data) <= 4
        @result: 
        '''
        Assertions.assert_data(data)
        Assertions.assert_can_id(can_id)
        msg = can.Message(arbitration_id=can_id,data=data,extended_id=False)
        self.bus.send(msg)


    def on_message_received(self,msg):
        print msg

        if msg.extended_id:
            # canopen 2.a expects 11bit identifiers
            raise NotImplemented

        function_code, node_id = CanOpenId.decode(msg.arbitration_id)

        len_data = len(msg.data) 
        
        if function_code == CanFunctionCode.nmt_error_control:
            self.process_nmt_error_control_msg(msg, function_code, node_id, len_data)

        elif function_code == CanFunctionCode.sdo_tx:
            self.process_sdo_tx_msg(msg, function_code, node_id, len_data)

        elif function_code in [CanFunctionCode.pdo1_tx, CanFunctionCode.pdo2_tx, CanFunctionCode.pdo3_tx]:
            self.process_pdo_tx_msg(msg, function_code, node_id, len_data)
        elif function_code in [CanFunctionCode.pdo1_rx, CanFunctionCode.pdo2_rx, CanFunctionCode.pdo3_rx]:
            self.process_pdo_rx_msg(msg, function_code, node_id, len_data)

