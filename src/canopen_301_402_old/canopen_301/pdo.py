#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.canopen_301.service import CanOpenServiceBaseClass

class CanOpenPdoTransfer(CanOpenServiceBaseClass):
    '''
    @summary: for use as cooperative base class in CanOpen
    '''
    def __init__(self, *args, **kwargs):
        super(CanOpenPdoTransfer, self).__init__(*args, **kwargs)

        # callbacks that will be called when new pdo msgs arrive
        self.pdo_callbacks = dict({1:None,2:None,3:None,4:None})

        # these datatypes are used to decode the can message data
        self.pdo_datatypes = dict({1:0x0006,2:0x0006,3:0x0006,4:0x0006})

    def setup_pdo_from_eds(self):
        # todo: use eds info to populate self.pdo_datatypes
        pass

    def setup_pdo_from_object_dictionary(self):
        # todo: use sdo access to object dictionary to populate self.pdo_datatypes
        pass

    def process_msg(self, msg):
        # todo
        pass

    def process_pdo_tx_msg(self, msg, function_code, node_id, len_data):
        # message coming from remote device (tx is named from the devices perspective)
        if function_code == CanFunctionCode.pdo1_tx:
            pdo_number = 1
        elif function_code == CanFunctionCode.pdo2_tx:
            pdo_number = 2
        elif function_code == CanFunctionCode.pdo3_tx:
            pdo_number = 3
        else:
            return

        value = self.datatypes.datatypes[self.pdo_datatypes[pdo_number]].decode(msg.data)
        
        if self.pdo_callbacks[pdo_number] is not None:
            self.pdo_callbacks[pdo_number](value)

    def process_pdo_rx_msg(self, msg, function_code, node_id, len_data):
        if function_code == CanFunctionCode.pdo1_rx:
            pdo_number = 1
        elif function_code == CanFunctionCode.pdo2_rx:
            pdo_number = 2
        elif function_code == CanFunctionCode.pdo3_rx:
            pdo_number = 3
        else:
            return

        pass