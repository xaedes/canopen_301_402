#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from collections import defaultdict

import can

from canopen_301_402.constants import *
from canopen_301_402.assertions import Assertions
from canopen_301_402.canopen_msgs.msg import CanOpenMessage
from canopen_301_402.canopen_msgs.msgs import *
from canopen_301_402.canopen_301.service import CanOpenServiceBaseClass

from canopen_301_402.signal import Signal

class CanOpenNetworkManagement(CanOpenServiceBaseClass):
    '''
    @summary: for use as cooperative base class in CanOpen
    '''
    def __init__(self, *args, **kwargs):
        super(CanOpenNetworkManagement, self).__init__(*args, **kwargs)

        self.signal_bootup = Signal()
        self.signal_enter_state = dict()
        self.signal_enter_state[Can301State.initialisation] = Signal()
        self.signal_enter_state[Can301State.pre_operational] = Signal()
        self.signal_enter_state[Can301State.operational] = Signal()
        self.signal_enter_state[Can301State.stopped] = Signal()

    def process_msg(self, msg):
        if isinstance(msg, CanOpenMessageNmtBootup):
            # device starts in state initialization
            # boot up message signals end of initialization
            if self.node.state == Can301State.initialisation:
                self.node.state = Can301State.pre_operational

                self.signal_bootup.dispatch()
                self.signal_enter_state[self.node.state].dispatch()
                
        elif isinstance(msg, CanOpenMessageNmtCommand):
            # change state according to nmt command
            if self.node.state in Can301StateTransitions:
                transitions = Can301StateTransitions[self.node.state]
                self.node.state = transitions[msg.command]
                
                self.signal_enter_state[self.node.state].dispatch()

    def start_remote_node(self):
        msg = CanOpenMessageNmtCommand(self.canopen, self.node.node_id, Can301StateCommand.start_remote_node)
        self.canopen.send_msg(msg)
    def enter_pre_operational(self):
        msg = CanOpenMessageNmtCommand(self.canopen, self.node.node_id, Can301StateCommand.enter_pre_operational)
        self.canopen.send_msg(msg)
    def stop_remote_node(self):
        msg = CanOpenMessageNmtCommand(self.canopen, self.node.node_id, Can301StateCommand.stop_remote_node)
        self.canopen.send_msg(msg)
    def reset_node(self):
        msg = CanOpenMessageNmtCommand(self.canopen, self.node.node_id, Can301StateCommand.reset_node)
        self.canopen.send_msg(msg)
    def reset_communication(self):
        msg = CanOpenMessageNmtCommand(self.canopen, self.node.node_id, Can301StateCommand.reset_communication)
        self.canopen.send_msg(msg)
