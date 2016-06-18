#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.sdo_write import SdoWrite
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoWriteRequest
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoWriteResponse
from canopen_301_402.canopen_msgs.msgs import CanOpenMessageSdoError

from time import sleep
import mock

evt_done_timeout = 2.0

TRACE = True

if TRACE:
    import hunter
    hunter.trace(module_contains="canopen_301_402")


def test_sdo_write_success():
    global evt_done_timeout

    node = mock.MagicMock()
    index,subindex = 1,2
    data = [3,4]
    
    write = SdoWrite(node,index,subindex,data)
    write.start()

    assert node.canopen.send.called

    msg, = node.canopen.send.call_args[0]
    assert type(msg) == CanOpenMessageSdoWriteRequest

    response = CanOpenMessageSdoWriteResponse(node.canopen, node.node_id, index, subindex)

    write.process_msg(response)

    write.evt_done.wait(evt_done_timeout)

    assert write.evt_success.isSet()
    assert not write.evt_fault.isSet()
    assert not write.evt_timeout.isSet()

def test_sdo_write_fault():
    global evt_done_timeout

    node = mock.MagicMock()
    index,subindex = 1,2
    data = [3,4]
    
    write = SdoWrite(node,index,subindex,data)
    write.start()

    assert node.canopen.send.called

    msg, = node.canopen.send.call_args[0]
    assert type(msg) == CanOpenMessageSdoWriteRequest
    response = CanOpenMessageSdoError(node.canopen, node.node_id, index, subindex, 0)

    write.process_msg(response)

    write.evt_done.wait(evt_done_timeout)

    assert write.evt_fault.isSet()
    assert not write.evt_success.isSet()
    assert not write.evt_timeout.isSet()

