#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.canopen_301.eds import *
from canopen_301_402.canopen_301.cob import CanOpenId
from canopen_301_402.canopen_301.msg import CanOpenMessage
from canopen_301_402.canopen_301.datatypes import CanDatatypes
from canopen_301_402.canopen_301.state import Can301State
from canopen_301_402.canopen_301.nmt import CanOpenNetworkManagement
from canopen_301_402.canopen_301.sdo import CanOpenSdoTransfer
from canopen_301_402.canopen_301.pdo import CanOpenPdoTransfer


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

        self.services = dict()
        # todo populate self.services with service for each CanOpenService
        # service should be something that can process CanOpenMessage


    def send_can(self, can_id, data):
        '''
        @summary: send message with data to 11 bit can_id 
        @param bus: can.Bus
        @param can_id: CanID (11bit)
        @param data: [byte] 0 <= len(data) <= 4
        @deprecated: use self.send_msg
        @result: 
        '''
        Assertions.assert_data(data)
        Assertions.assert_can_id(can_id)
        msg = can.Message(arbitration_id=can_id,data=data,extended_id=False)
        self.bus.send(msg)

    def send_msg(self, can_open_msg):
        '''
        @summary: 
        @param can_open_msg: CanOpenMessage
        @result: 
        '''
        self.bus.send(can_open_msg.to_can_msg())


    def on_message_received(self, msg):
        print msg

        msg = CanOpenMessage.from_can_msg(msg)

        # determine service from msg, or service should be part of canopenmessage
        service = CanOpenService.nmt # stub; see line above
        self.services[service].on_message_received(msg)

        len_data = len(msg.data) 
        
        # todo: replace this if construct by some kind of array lookup
        if msg.function_code == CanFunctionCode.nmt_error_control:
            self.process_nmt_error_control_msg(msg, msg.function_code, msg.node_id, len_data)

        elif msg.function_code == CanFunctionCode.sdo_tx:
            self.process_sdo_tx_msg(msg, msg.function_code, msg.node_id, len_data)

        elif msg.function_code in [CanFunctionCode.pdo1_tx, CanFunctionCode.pdo2_tx, CanFunctionCode.pdo3_tx]:
            self.process_pdo_tx_msg(msg, msg.function_code, msg.node_id, len_data)

        elif msg.function_code in [CanFunctionCode.pdo1_rx, CanFunctionCode.pdo2_rx, CanFunctionCode.pdo3_rx]:
            self.process_pdo_rx_msg(msg, msg.function_code, msg.node_id, len_data)

