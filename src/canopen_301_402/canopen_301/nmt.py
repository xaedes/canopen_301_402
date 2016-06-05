#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict

import can

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.canopen_301.state import Can301State
from canopen_301_402.canopen_301.msg import CanOpenMessage
from canopen_301_402.canopen_301.service import CanOpenServiceBaseClass


class CanOpenNetworkManagement(CanOpenServiceBaseClass):
    '''
    @summary: for use as cooperative base class in CanOpen
    '''
    def __init__(self, *args, **kwargs):
        super(CanOpenNetworkManagement, self).__init__(*args, **kwargs)

    def send_nmt(self, command, node_id=0):
        '''
        @summary: send nmt message
        @param command: Can301StateCommand
        @param [node_id=0]: 0 = all nodes
        @result: 
        ''' 

        Assertions.assert_node_id(node_id)
        Assertions.assert_nmt_command(command)

        # update canopen 301 state
        if self.canopen.nodes[node_id].state in Can301StateTransitions:
            transitions = Can301StateTransitions[self.nodes[node_id].state]
            self.canopen.nodes[node_id].state = transitions[command]

        # nmt message always needs node_id = 0 in CanOpenId.encode 
        # the node_id is specified in second data byte
        node_id = 0
        service = CanOpenService.nmt
        function_code = self.canopen.connection_set.determine_function_code(service)
        data = [Can301StateCommandBits[command], node_id]
        msg = CanOpenMessage(function_code, node_id, service, data)

        self.canopen.send_msg(msg)

    def process_msg(self, msg):
        # boot up message
        if msg.service == CanOpenService.nmt_error_control and len(msg.data) == 1 and msg.data[0] == 0: 
            # device starts in state initialization
            # boot up message signals end of initialization
            if self.canopen.nodes[msg.node_id].state == Can301State.initialisation:
                self.canopen.nodes[msg.node_id].state = Can301State.pre_operational

        if msg.msg_type == CanOpenMessageType.nmt_command:
            # change state according to nmt command

            if self.canopen.nodes[msg.node_id].state in Can301StateTransitions:
                transitions = Can301StateTransitions[self.nodes[node_id].state]
                self.canopen.nodes[msg.node_id].state = transitions[command]

