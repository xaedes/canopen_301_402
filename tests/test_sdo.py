#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import can

from canopen_301_402.canopen import CanOpen,eds_config
from canopen_301_402.constants import *
from canopen_301_402.canopen_msgs.msgs import *

import mock

def test_sdo_write_success():
    callback = mock.MagicMock()

    bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
    canopen=CanOpen(bus,eds_config)
    
    node = canopen.get_node(1)

    node.sdo.signal_write_complete[Can402Objects.controlword].register(callback)

    write_data = [0x06, 0x07]
    msg = CanOpenMessageSdoWriteRequest(canopen,1,Can402Objects.controlword[0],Can402Objects.controlword[1],write_data)
    canopen.send_msg(msg)

    msg = CanOpenMessageSdoWriteResponse(canopen,1,Can402Objects.controlword[0],Can402Objects.controlword[1])
    canopen.send_msg(msg)

    callback.assert_called()

def test_sdo_write_error():
    callback = mock.MagicMock()

    bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
    canopen=CanOpen(bus,eds_config)
    
    node = canopen.get_node(1)

    node.sdo.signal_error[Can402Objects.controlword].register(callback)

    write_data = [0x06, 0x07]
    msg = CanOpenMessageSdoWriteRequest(canopen,1,Can402Objects.controlword[0],Can402Objects.controlword[1],write_data)
    canopen.send_msg(msg)

    error_code = CanErrors.keys()[0]
    msg = CanOpenMessageSdoError(canopen,1,Can402Objects.controlword[0],Can402Objects.controlword[1], error_code)
    canopen.send_msg(msg)

    callback.assert_called()

def test_sdo_read_success():
    callback = mock.MagicMock()

    bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
    canopen=CanOpen(bus,eds_config)
    
    node = canopen.get_node(1)

    node.sdo.signal_write_complete[Can402Objects.controlword].register(callback)

    msg = CanOpenMessageSdoReadRequest(canopen,1,Can402Objects.controlword[0],Can402Objects.controlword[1])
    canopen.send_msg(msg)

    read_data = [0x06, 0x07]
    msg = CanOpenMessageSdoReadResponse(canopen,1,Can402Objects.controlword[0],Can402Objects.controlword[1], read_data)
    canopen.send_msg(msg)

    callback.assert_called()

def test_sdo_read_error():
    callback = mock.MagicMock()

    bus = can.interface.Bus('vcan0', bustype='socketcan_ctypes')
    canopen=CanOpen(bus,eds_config)
    
    node = canopen.get_node(1)

    node.sdo.signal_error[Can402Objects.controlword].register(callback)

    msg = CanOpenMessageSdoReadRequest(canopen,1,Can402Objects.controlword[0],Can402Objects.controlword[1])
    canopen.send_msg(msg)

    error_code = CanErrors.keys()[0]
    msg = CanOpenMessageSdoError(canopen,1,Can402Objects.controlword[0],Can402Objects.controlword[1], error_code)
    canopen.send_msg(msg)

    callback.assert_called()
