#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from canopen_301_402.async.async_send_and_await import AsyncSendAndAwait
from time import sleep
import mock

evt_done_timeout = 2.0

TRACE = True

if TRACE:
    import hunter
    hunter.trace(module_contains="canopen_301_402")

def test_send_and_await():
    global evt_done_timeout

    factory = mock.MagicMock()
    node = mock.MagicMock()

    predicate = lambda _: True

    async_send_and_await = AsyncSendAndAwait(node,factory,predicate)
    async_send_and_await.start()

    factory.assert_called_once_with()
    msg = factory.return_value
    node.canopen.send.assert_called_once_with(msg)

    async_send_and_await.process_msg(msg)
    async_send_and_await.evt_done.wait(evt_done_timeout)

    assert async_send_and_await.evt_success.isSet()
    assert not async_send_and_await.evt_fault.isSet()
    assert not async_send_and_await.evt_timeout.isSet()
