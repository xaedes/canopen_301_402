#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.canopen import CanOpen,eds_config
from canopen_301_402.constants import *
from canopen_301_402.utils import str_to_can_msg, can_msg_to_str
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

def test_str_to_can_msg():
    assert str_to_can_msg("000#R").is_remote_frame == True
    
    m = str_to_can_msg("601#01.02")
    assert m.is_remote_frame == False
    assert m.id_type == False
    assert m.arbitration_id == 0x601
    assert m.data[0] == 0x01
    assert m.data[1] == 0x02

    for s in ["581#0F.0E.0D.0C.0B.0A.09.08","581#0f.0e.0d.0c.0b.0a.09.08"]:
        m = str_to_can_msg(s)
        assert m.is_remote_frame == False
        assert m.id_type == False
        assert m.arbitration_id == 0x581
        assert m.data[0] == 0x0F
        assert m.data[1] == 0x0E
        assert m.data[2] == 0x0D
        assert m.data[3] == 0x0C
        assert m.data[4] == 0x0B
        assert m.data[5] == 0x0A
        assert m.data[6] == 0x09
        assert m.data[7] == 0x08


def test_can_msg_to_str():
    assert "123#R" == can_msg_to_str(can.Message(extended_id=False,is_remote_frame=True,arbitration_id=0x123))
    assert "234#" == can_msg_to_str(can.Message(extended_id=False,arbitration_id=0x234,data=[]))
    assert "345#0A" == can_msg_to_str(can.Message(extended_id=False,arbitration_id=0x345,data=[0x0A]))
    assert "456#0A.0B.0C.0D.0E.0F.00.01" == can_msg_to_str(can.Message(extended_id=False,arbitration_id=0x456,data=[0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x00,0x01]))
