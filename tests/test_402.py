#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.canopen import CanOpen,eds_config
from canopen_301_402.constants import *
from canopen_301_402.operations import Operations
from canopen_301_402.canopen_msgs.msgs import *

import mock

def test_402_state():
    callback = mock.MagicMock()

    bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
    canopen=CanOpen(bus,eds_config)
    
    node = canopen.get_node(1)

    assert node.can402.state == Can402State.switch_on_disabled

    def on_complete1():
        assert node.can402.state == Can402State.ready_to_switch_on

        def on_complete2():
            assert node.can402.state == Can402State.switched_on

        node.can402.change_state(Can402StateCommand.switch_on,on_complete2)

    node.can402.change_state(Can402StateCommand.shutdown,on_complete1)

        

def test_402_state2():
    callback = mock.MagicMock()

    bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
    canopen=CanOpen(bus,eds_config)
    
    node = canopen.get_node(1)

    class MyOp(Operations):
        def __init__(self, node):
            super(MyOp, self).__init__()
            self.node = node
        
        def step1(self):
            assert self.node.can402.state == Can402State.switch_on_disabled
            self.node.can402.change_state(Can402StateCommand.shutdown, self.next_operation)

        def step2(self):
            assert self.node.can402.state == Can402State.ready_to_switch_on
            self.node.can402.change_state(Can402StateCommand.switch_on, self.next_operation)

        def done(self):
            assert self.node.can402.state == Can402State.switched_on

    op = MyOp(node)
    op.next_operation()
