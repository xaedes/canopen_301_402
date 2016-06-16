#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.canopen import CanOpen,eds_config
from canopen_301_402.constants import *
from canopen_301_402.operations import Operations
from canopen_301_402.canopen_msgs.msgs import *

import mock

def test_status_word_402state():
    callback = mock.MagicMock()

    bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
    canopen=CanOpen(bus,eds_config)
    node_id = 1
    node = canopen.get_node(node_id)

    assert node.can402.state == Can402State.switch_on_disabled
    
    node.can402.statusword.signal_value_updated.register(callback)

    for state,bits in Can402StatuswordStateBits.iteritems():

        req = CanOpenMessageSdoReadRequest(canopen, node_id, Can402Objects.statusword[0],Can402Objects.statusword[1])
        res = CanOpenMessageSdoReadResponse(canopen, node_id, Can402Objects.statusword[0],Can402Objects.statusword[1],
                            data=[bits & 0xff,0x00])


        canopen.on_message_received(req)
        canopen.on_message_received(res)

        callback.assert_called()

        node.can402.state == state
