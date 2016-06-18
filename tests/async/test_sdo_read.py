#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.sdo_read import SdoRead
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoReadRequest
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoReadResponse
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoError

from time import sleep
import mock

evt_done_timeout = 2.0

TRACE = True

if TRACE:
    import hunter
    hunter.trace(module_contains="canopen_301_402")

def test_sdo_read_success():
    global evt_done_timeout

    node = mock.MagicMock()
    index,subindex = 1,2
    
    data = [3,4]
    
    read = SdoRead(node,index,subindex)
    read.start()

    assert node.canopen.send.called

    msg, = node.canopen.send.call_args[0]
    assert type(msg) == CanOpenMessageSdoReadRequest
    response = CanOpenMessageSdoReadResponse(node.canopen, node.node_id, index, subindex, data)

    read.process_msg(response)

    read.evt_done.wait(evt_done_timeout)

    assert read.evt_success.isSet()
    assert not read.evt_fault.isSet()
    assert not read.evt_timeout.isSet()

    assert read.result == data

def test_sdo_read_fault():
    global evt_done_timeout

    node = mock.MagicMock()
    index,subindex = 1,2
    data = [3,4]
    
    read = SdoRead(node,index,subindex)
    read.start()

    assert node.canopen.send.called

    msg, = node.canopen.send.call_args[0]
    assert type(msg) == CanOpenMessageSdoReadRequest
    response = CanOpenMessageSdoError(node.canopen, node.node_id, index, subindex, 0)

    read.process_msg(response)

    read.evt_done.wait(evt_done_timeout)

    assert read.evt_fault.isSet()
    assert not read.evt_success.isSet()
    assert not read.evt_timeout.isSet()
