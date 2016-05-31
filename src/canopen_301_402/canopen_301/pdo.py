#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions

class CanOpenPdoTransfer(object):
    '''
    @summary: for use as cooperative base class in CanOpen
    '''
    def __init__(self, *args, **kwargs):
        super(CanOpenPdoTransfer, self).__init__(*args, **kwargs)

        self.pdo_callbacks = dict({1:None,2:None,3:None})
        self.pdo_datatypes = dict({1:0x0006,2:0x0006,3:0x0006})

    def process_pdo_tx_msg(self, msg, function_code, node_id, len_data):
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