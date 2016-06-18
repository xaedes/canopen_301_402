#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.async_send import AsyncSend
from time import sleep
import mock

evt_done_timeout = 2.0

TRACE = True

if TRACE:
    import hunter
    hunter.trace(module_contains="canopen_301_402")

def test_send():
    global evt_done_timeout
    
    factory = mock.MagicMock()
    node = mock.MagicMock()

    async_send = AsyncSend(node,factory)
    async_send.start()
    async_send.evt_done.wait(evt_done_timeout)

    factory.assert_called_once_with()
    msg = factory.return_value
    node.canopen.send.assert_called_once_with(msg)
