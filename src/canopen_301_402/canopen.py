#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.can301 import Assertions

class Can301State(Enum):
    initialisation = 0
    pre_operational = 1
    operational = 2
    stopped = 3 # no sdo and bdo access, only nmt to change state

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

class CanOpen(can.Listener):
    """docstring for CanOpen"""
    def __init__(self, bus):
        super(CanOpen, self).__init__()
        self.bus = bus
        self.node_states = defaultdict(lambda:Can301State.initialisation)

        self.notifier = can.Notifier(self.bus,[self])

        self.response_callbacks = dict()

    def start_remote_nodes(self):
        send_nmt(bus, Can301StateCommand.start_remote_node, 0)

    def start_remote_node(self, node_id):
        self.send_nmt(bus, Can301StateCommand.start_remote_node, node_id)


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
        msg = can.Message(arbitration_id=can_id,data=data],extended_id=False)
        self.bus.send(msg)

    def send_nmt(self, command, node_id=0):
        '''
        @summary: send nmt message
        @param command: Can301StateCommand
        @param [node_id=0]: 0 = all nodes
        @result: 
        ''' 

        # nmt message always needs node_id = 0 in CanOpenId.encode 
        # the node_id is specified in second data byte

        can_id = CanOpenId.encode(CanFunctionCode.nmt, 0)
        self.send_can(can_id, [command, node_id])

    def send_sdo_write_request(self, node_id, index, subindex, data, response_callback):
        '''
        @summary: 
        @param node_id:
        @param index:
        @param subindex:
        @param data: byte array, maximum length: 4 bytes
        @param response_callback: function(error), where error is None if sucessful or string containing error description
        @result: 
        '''
        Assertions.assert_node_id(node_id)
        Assertions.assert_index(index)
        Assertions.assert_subindex(subindex)
        Assertions.assert_data(data,maximum_len=4)
        
        can_id = CanOpenId.encode(CanFunctionCode.sdo_rx, node_id)
        len_data = len(data)

        if len_data == 0:
            # Falls keine Angabe der Anzahl Datenbytes erforderlich ist: Byte0 = 0x22
            sdo_download_request = CanData.sdo_download_request_bits - 1
        else:
            sdo_download_request = ((4-len_data)<<2) | CanData.sdo_download_request_bits
        
        data = [sdo_download_request,
                (index & 0xff), 
                (index>>8), 
                subindex] + data

        key = ("sdo_write", node_id, index, subindex)
        self.response_callbacks[key] = response_callback

        self.send_can(can_id, data)


    def send_sdo_read_request(self, node_id, index, subindex, response_callback):
        '''
        @summary: 
        @param node_id:
        @param index:
        @param subindex:
        @param response_callback: function(error,[byte]: data=none), where error is None or string containing error description
        @result: 
        '''
        Assertions.assert_node_id(node_id)
        Assertions.assert_index(index)
        Assertions.assert_subindex(subindex)
        can_id = CanOpenId.encode(CanFunctionCode.sdo_rx, node_id)
        data = [CanData.sdo_upload_request,
                (index & 0xff), 
                (index>>8), 
                subindex]

        key = ("sdo_read", node_id, index, subindex)
        self.response_callbacks[key] = response_callback

        self.send_can(can_id, data)

    def process_nmt_error_control_msg(self, msg, function_code, node_id, len_data):
        # boot up message
        if len_data == 1 and msg.data[0] == 0: 
            # device starts in state initialization
            # boot up message signals end of initialization
            if self.nodes[node_id].state == Can301State.initialisation:
                self.nodes[node_id].state = Can301State.pre_operational

    def process_sdo_tx_msg(self, msg, function_code, node_id, len_data):
        # sdo response
        if len_data == 8:
            index = msg.data[1] | (msg.data[2] << 8)
            subindex = msg.data[3]

            # sdo error
            if msg.data[0] == CanData.sdo_error:
                # error code is in little endian 
                error = msg.data[4] | (msg.data[5]<<8) | (msg.data[6]<<16) | (msg.data[7]<<24)
                if error_msg in CanErrors:
                    error_msg = CanErrors[error]
                else:
                    error_msg = CanErrors.unknown % hex(error)

                # error can happen for both sdo_write and sdo_read
                for _key in ["sdo_write","sdo_read"]:
                    key = (_key, node_id, index, subindex)
                    if key in self.response_callbacks:
                        # call response callback
                        self.response_callbacks[key](error=None)
                        # remove response callback
                        del self.response_callbacks[key]

            # read response
            if (msg.data[0] & CanData.sdo_upload_response) == CanData.sdo_upload_response:
                # len_response_data of sdo object is encoded as this:
                # msg.data[0] == CanData.sdo_upload_response | ((4-len_response_data)<<2)
                len_response_data = 4-(msg.data[0] >> 2) & 0b11
                data = msg.data[4:4+len_response_data]

                key = ("sdo_read", node_id, index, subindex)

                if key in self.response_callbacks:
                    # call response callback
                    self.response_callbacks[key](error=None,data=data)
                    # remove response callback
                    del self.response_callbacks[key]

            # write response: success
            if msg.data[0] == CanData.sdo_download_response: 
                # get index and subindex from msg
                key = ("sdo_write", node_id, index, subindex)
                if key in self.response_callbacks:
                    # call response callback
                    self.response_callbacks[key](error=None)
                    # remove response callback
                    del self.response_callbacks[key]

    def on_message_received(self,msg):
        print msg

        if msg.extended_id:
            # the version of canopen we implement expects 11bit identifiers
            raise NotImplemented

        function_code, node_id = self.decode_can_open_id(msg.arbitration_id)

        len_data = len(msg.data) 
        
        if function_code == CanFunctionCode.nmt_error_control:
            self.process_nmt_error_control_msg(msg, function_code, node_id, len_data)

        elif function_code == CanFunctionCode.sdo_tx:
            self.process_sdo_tx_msg(msg, function_code, node_id, len_data)
