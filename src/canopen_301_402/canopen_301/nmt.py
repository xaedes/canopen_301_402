#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict

import can

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.canopen_301.state import Can301State


class CanOpenNetworkManagement(object):
    '''
    @summary: for use as cooperative base class in CanOpen
    '''
    def __init__(self, *args, **kwargs):
        super(CanOpenNetworkManagement, self).__init__(*args, **kwargs)

        self.node_states = defaultdict(lambda:Can301State.initialisation)

    def start_remote_nodes(self):
        send_nmt(bus, Can301StateCommand.start_remote_node, 0)

    def start_remote_node(self, node_id):
        self.send_nmt(bus, Can301StateCommand.start_remote_node, node_id)

    def send_nmt(self, command, node_id=0):
        '''
        @summary: send nmt message
        @param command: Can301StateCommand
        @param [node_id=0]: 0 = all nodes
        @result: 
        ''' 

        # nmt message always needs node_id = 0 in CanOpenId.encode 
        # the node_id is specified in second data byte
        Assertions.assert_node_id(node_id)
        Assertions.assert_nmt_command(command)

        if self.node_states[node_id] in Can301State.Transitions:
            transitions = Can301State.Transitions[self.nodes[node_id].state]
            self.node_states[node_id] = transitions[command]

        can_id = CanOpenId.encode(CanFunctionCode.nmt, 0)
        self.send_can(can_id, [command, node_id])

    def process_nmt_error_control_msg(self, msg, function_code, node_id, len_data):
        # boot up message
        if len_data == 1 and msg.data[0] == 0: 
            # device starts in state initialization
            # boot up message signals end of initialization
            if self.node_states[node_id] == Can301State.initialisation:
                self.node_states[node_id] = Can301State.pre_operational
            elif self.node_states[node_id] in Can301State.Transitions:
                transitions = Can301State.Transitions[self.nodes[node_id].state]
                # command = 
