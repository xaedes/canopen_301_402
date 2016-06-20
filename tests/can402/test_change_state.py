#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.constants import *
from canopen_301_402.async.async_operation import AsyncOperation
from canopen_301_402.can402.ops.change_controlword import ChangeControlword
from time import sleep
import mock

evt_done_timeout = 2.0

TRACE = False

if TRACE:
    import hunter
    hunter.trace(module_contains="canopen_301_402")

import struct

def test(can402_controlword_bit):
    global evt_done_timeout

    node = mock.MagicMock()

    node.controlword = 0x0000

    op = ChangeControlword(node, updates={
            can402_controlword_bit: True,
        })
    op.start()

    msg = node.canopen.send.call_args[0][0]
    written_controlword, = struct.unpack("<H",bytearray(msg.write_data[:2]))

    assert ((written_controlword >> can402_controlword_bit.value) & 1) == 1

def _test_unset_bit(start_value,can402_controlword_bit):
    global evt_done_timeout

    node = mock.MagicMock()

    node.controlword = start_value

    op = ChangeControlword(node, updates={
            can402_controlword_bit: False,
        })
    op.start()

    msg = node.canopen.send.call_args[0][0]
    written_controlword, = struct.unpack("<H",bytearray(msg.write_data[:2]))

    assert ((written_controlword >> can402_controlword_bit.value) & 1) == 0

def test():
    _test_set_bit(0x0000, Can402ControlwordBits.switch_on)
    _test_set_bit(0x0000, Can402ControlwordBits.enable_voltage)
    _test_set_bit(0x0000, Can402ControlwordBits.quick_stop)
    _test_set_bit(0x0000, Can402ControlwordBits.enable_operation)
    _test_set_bit(0x0000, Can402ControlwordBits.new_set_point)
    _test_set_bit(0x0000, Can402ControlwordBits.change_set_immediately)
    _test_set_bit(0x0000, Can402ControlwordBits.abs_rel)
    _test_set_bit(0x0000, Can402ControlwordBits.fault_reset)
    _test_set_bit(0x0000, Can402ControlwordBits.halt)
    
    _test_set_bit(0xFFFF, Can402ControlwordBits.switch_on)
    _test_set_bit(0xFFFF, Can402ControlwordBits.enable_voltage)
    _test_set_bit(0xFFFF, Can402ControlwordBits.quick_stop)
    _test_set_bit(0xFFFF, Can402ControlwordBits.enable_operation)
    _test_set_bit(0xFFFF, Can402ControlwordBits.new_set_point)
    _test_set_bit(0xFFFF, Can402ControlwordBits.change_set_immediately)
    _test_set_bit(0xFFFF, Can402ControlwordBits.abs_rel)
    _test_set_bit(0xFFFF, Can402ControlwordBits.fault_reset)
    _test_set_bit(0xFFFF, Can402ControlwordBits.halt)
    
    _test_unset_bit(0x0000, Can402ControlwordBits.switch_on)
    _test_unset_bit(0x0000, Can402ControlwordBits.enable_voltage)
    _test_unset_bit(0x0000, Can402ControlwordBits.quick_stop)
    _test_unset_bit(0x0000, Can402ControlwordBits.enable_operation)
    _test_unset_bit(0x0000, Can402ControlwordBits.new_set_point)
    _test_unset_bit(0x0000, Can402ControlwordBits.change_set_immediately)
    _test_unset_bit(0x0000, Can402ControlwordBits.abs_rel)
    _test_unset_bit(0x0000, Can402ControlwordBits.fault_reset)
    _test_unset_bit(0x0000, Can402ControlwordBits.halt)

    _test_unset_bit(0xFFFF, Can402ControlwordBits.switch_on)
    _test_unset_bit(0xFFFF, Can402ControlwordBits.enable_voltage)
    _test_unset_bit(0xFFFF, Can402ControlwordBits.quick_stop)
    _test_unset_bit(0xFFFF, Can402ControlwordBits.enable_operation)
    _test_unset_bit(0xFFFF, Can402ControlwordBits.new_set_point)
    _test_unset_bit(0xFFFF, Can402ControlwordBits.change_set_immediately)
    _test_unset_bit(0xFFFF, Can402ControlwordBits.abs_rel)
    _test_unset_bit(0xFFFF, Can402ControlwordBits.fault_reset)
    _test_unset_bit(0xFFFF, Can402ControlwordBits.halt)
    
