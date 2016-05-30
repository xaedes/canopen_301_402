#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.constants import *

class Can301State(Enum):
    initialisation = 0
    pre_operational = 1
    operational = 2
    stopped = 3 # no sdo and bdo access, only nmt to change state


class CanOpen(can.Listener):
    """docstring for CanOpen"""
    def __init__(self, bus):
        super(CanOpen, self).__init__()
        self.bus = bus
        self.node_states = defaultdict(lambda:Can301State.initialisation)

        self.notifier = can.Notifier(self.bus,[self])

    def start_remote_nodes(self):
        send_nmt(bus, Can301StateCommand.start_remote_node, 0)

    def start_remote_node(self, node_id):
        self.send_nmt(bus, Can301StateCommand.start_remote_node, node_id)

    def decode_can_open_id(self, can_id):
        # can open interpretation of can id:
        
        # the upper 4 bits of the 11 bit arbitration_id are the function code
        function_code = (msg.arbitration_id >> 7) & 0b1111
        # the lower 7 bits of the 11 bit arbitration_id are the node_id
        node_id = msg.arbitration_id & 0b1111111
        return function_code, node_id

    def send_can(self, can_id, data):
        '''
        @summary: send message with data to 11 bit can_id 
        @param bus: can.Bus
        @param can_id: CanID (11bit)
        @param data: [byte] 0 <= len(data) <= 4
        @result: 
        '''
        assert (can_id >> 11) == 0 # maximum 11 bits
        assert 0 <= len(data) <= 4
        msg = can.Message(arbitration_id=can_id,data=data],extended_id=False)
        self.bus.send(msg)

    def send_nmt(self, command, node_id=0):
        '''
        @summary: send nmt message
        @param command: Can301StateCommand
        @param [node_id=0]: 0 = all nodes
        @result: 
        ''' 
        self.send_can((CanFunctionCode.nmt << 7), [command, node_id])

    def decode_can_open_id(self, can_id):
                
        # can open interpretation of can id:
        
        # the upper 4 bits of the 11 bit arbitration_id are the function code
        function_code = (msg.arbitration_id >> 7) & 0b1111
        # the lower 7 bits of the 11 bit arbitration_id are the node_id
        node_id = msg.arbitration_id & 0b1111111
        return function_code, node_id

    def on_message_received(self,msg):
        print msg

        if msg.extended_id:
            # the version of canopen we implement expects 11bit identifiers
            raise NotImplemented

        function_code, node_id = self.decode_can_open_id(msg.arbitration_id)

        len_data = len(msg.data) 
        
        if function_code == CanFunctionCode.nmt_error_control:
            
            if len_data == 1 and msg.data[0] == 0: # boot up message
                # device starts in state initialization
                # boot up message signals end of initialization
                if self.nodes[node_id].state == Can301State.initialisation:
                    self.nodes[node_id].state = Can301State.pre_operational

